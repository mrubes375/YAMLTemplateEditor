import sys
import os
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from YAMLEditor.yaml_config import get_yaml

class Handler:
    def __init__(self):
        self.template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates')
        self.files_changed = set()
        self.time = None
        self.template = None
        self.old_context = None
        self.new_context = None
    def get_template(self, context):
        self.old_context = context
        yaml = get_yaml()
        return
    def find_files(self, template_tag):
        
x = Handler()
x.get_template('a')
