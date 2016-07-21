import sys
import os
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from YAMLEditor.yaml_config import get_yaml

class Handler:
    def __init__(self, template_dir=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates')):
        if template_dir is None:
            self.template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates')
        else:
            self.template_dir = template_dir
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
        queue = self.all_files
        while len(queue)>0:
            searching = queue.pop(0)
            contents = open(searching, 'r').read()
            answer = (template in contents)
            print(contents)
            if answer:
                self.files_changed.append(searching)
# x = Handler()
# x.get_all_files()
# print(os.getcwd())
# x.search_files('my_yaml.no_access.title')
# print(x.all_files)
# print(x.files_changed)
