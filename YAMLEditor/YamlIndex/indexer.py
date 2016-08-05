from YAMLEditor.yaml_config import get_yaml

class Indexer:
    def __init__(self):
        self.template_yaml = get_yaml()
        print(self.template_yaml)
