
import os
import ruamel.yaml
#
# base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# template_dir = os.path.join(base, 'templates')
# os.chdir(template_dir)
#
# yaml_file = open("master.yaml", 'r')
# contents = yaml_file.read()
#
# code = ruamel.yaml.load(contents, ruamel.yaml.RoundTripLoader)
#

def get_yaml():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_dir = os.path.join(base, 'templates')
    os.chdir(template_dir)
    yaml_file = open("master.yaml", 'r+')
    contents = yaml_file.read()
    return ruamel.yaml.load(contents, ruamel.yaml.RoundTripLoader)
