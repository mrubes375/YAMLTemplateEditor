import sys
import os
from datetime import datetime
import copy
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from YAMLEditor.yaml_config import get_yaml
from re import search

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
        self.yaml = None
    def get_template(self, context):
        self.old_context = context
        self.yaml = get_yaml()
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
