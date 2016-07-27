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

# class ExtendedFiles:
#     def __init__(self, name):
#         self.file_name = name
#         self.children = []
#     def __str__(self):
#         return "File: %s, Children: %s" % (self.file_name, self.children)

class Handler:
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
    def search_files(self, template):
        regex_pattern = '(?<=extends\s").*l'
        queue = set(copy.copy(self.all_files))
        extends = dict()
        found = set()
        while len(queue)>0:
            searching = queue.pop()
            contents = open(searching, 'r').read()
            if "extends" in contents:
                match = search(regex_pattern, contents).group()
                queue.add(match)
                if match in extends:
                    extends[match].add(searching)
                else:
                    extends[match] = set()
                    extends[match].add(searching)
            answer = (template in contents)
            if answer:
                found.add(searching)
        for html in found:
            found = found.union(extends[html])
        self.files_changed = found
# x = Handler()
# x.get_all_files()
# x.search_files('my_yaml.navbar.name')
# print(x.all_files)
# print(x.files_changed)
class DataBindingDOM:
    def __init__(self, template_dir, template):
        self.template_dir = template_dir
        os.chdir(template_dir)
        self.template_location = os.path.join(template_dir, template)
        self.text = open(self.template_location, 'r+').read()
    def bind(self):
        html = BeautifulSoup(self.text, "lxml")
        for elem in html(text=compile(r'\{{(.*?)\}}')):
            if 'my_yaml' in elem.parent.text:
                element_match = match(r'\{{(.*?)\}}', elem.parent.text)
                if element_match is not None:
                    elem.parent['data'] = element_match.group(1).strip()
        return str(html)

class ChangeYAML:
    def __init__(self, tag, new_context):
        self.tag = tag
        self.new_context = new_context
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
        update = copy.copy(yaml)
        while count>1:
            key = access_keys.pop(0)
            update = update[key]
            count-=1
        changed_key = access_keys.pop(0)
        update[changed_key] = self.new_context
        new_contents = ruamel.yaml.dump(yaml, Dumper=ruamel.yaml.RoundTripDumper)
        yaml_file = open("master.yaml", 'w+')
        yaml_file.write(new_contents)
        yaml_file.close()
