import sys
import os
from datetime import datetime
import copy
from bs4 import BeautifulSoup
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from YAMLEditor.yaml_config import get_yaml
from re import search, compile, match
from tempfile import NamedTemporaryFile
import ruamel.yaml
from github3 import login

class FileSearcher:
    def __init__(self):
        self.template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates')
        os.chdir(self.template_dir)
        self.files_changed = list()
        self.all_files = list()
        self.time = None
        self.template = None
        self.old_context = None
        self.new_context = None
        self.yaml = get_yaml()
    def get_yaml(self):
        return self.yaml
    def get_all_files(self):
        os.chdir(self.template_dir)
        queue = os.listdir()
        while len(queue)>0:
            checking = queue.pop(0)
            if '.html' in checking:
                self.all_files.append(checking)
            elif '.' in checking:
                pass
            else:
                os.chdir(self.template_dir+'/'+checking)
                for additional_file in os.listdir():
                    queue.append(checking+'/'+additional_file)
        os.chdir(self.template_dir)
    @staticmethod
    def collect_modified_files(file_set, file_dict):
        for html in file_set:
            try:
                file_set = file_set.union(file_dict[html])
            except KeyError:
                file_set.add(html)
        return file_set
    def search(self, template, template_type):
        regex_pattern = r'(?<=' + template_type + '\s")([A-Za-z0-9_\./\\-]*)'
        queue = set(copy.copy(self.all_files))
        matching_files = dict()
        found = set()
        while len(queue)>0:
            searching = queue.pop()
            contents = open(searching, 'r').read()
            if template_type in contents:
                re_match = search(regex_pattern, contents).group()
                queue.add(re_match)
                if re_match in matching_files:
                    matching_files[re_match].add(searching)
                else:
                    matching_files[re_match] = set()
                    matching_files[re_match].add(searching)
            answer = (template in contents)
            if answer:
                found.add(searching)
        return self.collect_modified_files(found, matching_files)
    def search_files(self, template):
        extends = self.search(template, 'extends')
        include = self.search(template, 'include')
        self.files_changed = extends.union(include)
    def get_files_changed(self, tag):
        self.get_all_files()
        self.search_files(tag)
        return self.files_changed

class DataBindingDOM:
    def __init__(self, template_dir, template, template_type=None):
        if template_type is not None:
            self.template_type = template_type
        else:
            self.template_type = 'base'
        self.template_name = template
        self.template_dir = template_dir
        os.chdir(template_dir)
        self.template_location = os.path.join(template_dir, template)
        self.text = open(self.template_location, 'r+').read()
    def bind(self, list_text=None):
        if list_text is None:
            list_text = []
        html = BeautifulSoup(self.text, "lxml")
        find_extends = HTMLTemplate(self.text).tag_search('extends')
        if find_extends is not None:
            extended_temp = find_extends.group(0)
            extended = DataBindingDOM(self.template_dir, extended_temp, 'extend')
            extended_text = extended.bind()
            list_text = list_text + extended_text
        find_include = HTMLTemplate(self.text).tag_search('include')
        if find_include is not None:
            print(find_include.group(0), find_include.group(1))
            i = 0
            group = find_include.group(i)
            while group is not None:
                include_temp = find_include.group(i)
                included = DataBindingDOM(self.template_dir, include_temp, 'include')
                include_text = included.bind()
                list_text = list_text + include_text
                i+=1
                try:
                    group = find_include.group(i)
                except IndexError:
                    group = None
                    break
        for elem in html(text=compile(r'\{{(.*?)\}}')):
            if 'my_yaml' in elem.parent.text:
                element_match = match(r'\{{(.*?)\}}', elem.parent.text)
                if element_match is not None:
                    elem.parent['data'] = element_match.group(1).strip()
        list_text.append([self.template_type, self.template_name, str(html)])
        return list_text

class ChangeYAML:
    def __init__(self, tag, new_context):
        self.tag = tag
        self.new_context = new_context
        self.old_context = None
    def update(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        template_dir = os.path.join(base, 'templates')
        os.chdir(template_dir)
        yaml_file = open("master.yaml", 'r+')
        contents = yaml_file.read()
        yaml_file.close()
        yaml = ruamel.yaml.load(contents, ruamel.yaml.RoundTripLoader)
        access_keys = self.tag.split('.')[1:]
        count = len(access_keys)
        if count>1:
            update = copy.copy(yaml)
            while count!=1:
                key = access_keys.pop(0)
                update = update[key]
                count-=1
            changed_key = access_keys.pop(0)
            old_context = update[changed_key]
            update[changed_key] = self.new_context
        elif count==1:
            changed_key = access_keys.pop(0)
            old_context = yaml[changed_key]
            yaml[changed_key] = self.new_context
        new_contents = ruamel.yaml.dump(yaml, Dumper=ruamel.yaml.RoundTripDumper)
        return (old_context, new_contents)

class GitCommitYaml:
    def __init__(self, username, password, tag, new_contents):
        self.gitsession = login(username, password=password)
        self.repo = self.gitsession.repository(username, 'YAMLTemplateEditor')
        template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates')
        os.chdir(template_dir)
        self.repo.contents('YAMLEditor/templates/master.yaml').update('Updated %s translation' % (tag), new_contents)


class HTMLTemplate:
    def __init__(self, text, template_type=None):
        self.text = text
        if template_type is not None:
            self.template_type = template_type
        else: self.template_type = None
    def tag_stripper(self):
        if self.template_type=='include':
            return self.text.replace("<html>", "", 1).replace("</html>", "", 1).replace("<body>", "", 1).replace("</body>", "", 1)
        elif self.template_type=='base':
            return self.text.replace("<p>", "", 1).replace("</p>", "", 1).replace("<html>", "", 1).replace("</html>", "", 1).replace("<body>", "", 1).replace("</body>", "", 1)
        elif self.template_type=='extend':
            return self.text
    def tag_search(self, tag):
        regex_pattern = r'(?<=' + tag + '\s")([A-Za-z0-9_\./\\-]*)'
        return search(regex_pattern, self.text)

def nested_temp_file_extender(template_list):
    temp_files = []
    template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates')
    while len(template_list)!=0:
        popped_template = template_list.pop()
        if popped_template[0]=='base':
            base_text = HTMLTemplate(popped_template[2], popped_template[0]).tag_stripper()
        rendered_file = NamedTemporaryFile(mode='r+', dir=template_dir, suffix='.html')
        rendered_file.write(HTMLTemplate(popped_template[2], popped_template[0]).tag_stripper())
        file_name = list(rendered_file.name.split('/'))[-1]
        base_text = base_text.replace(popped_template[1], file_name)
        rendered_file.read()
        temp_files.append(rendered_file)
    rendered_file = NamedTemporaryFile(mode='r+', dir=template_dir, suffix='.html')
    rendered_file.write(base_text)
    file_name = list(rendered_file.name.split('/'))[-1]
    rendered_file.read()
    temp_files.append(rendered_file)
    return (file_name, temp_files)
