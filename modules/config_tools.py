import yaml, json
import os, urllib, urllib2
import fnmatch

config_file_type = '*.json'

class Collect_configs ():
    """ empty """


    def collect_config_files(self,search_root='./patterns'):
        result_set = []
        for roots,directories,files in os.walk(search_root):
            for file in files:
                if fnmatch.fnmatch(file, config_file_type):
                    relativeDir=os.path.relpath(roots, search_root)
                    relative_path=os.path.join(relativeDir,file)
                    result_set.append(relative_path)
        return result_set

    """
    def read_yaml(self, file, existing_yaml={}):
        yaml_result = {}
        found_yaml = yaml.load(open(file))
        return found_yaml
    """

    def read_json(self, file):
        found_json = json.load(open(file))
        return found_json


    def split_config(self, config):
        schedule = config['schedule']
        threshold = config
        del threshold['schedule']

        return threshold, schedule


    def replace_schedule(self, target_json, payload_json):
        """ we're looking for 'schedule' """
        target_json['schedule'] = payload_json
        return target_json


    def get_index(self, json):
        return json['input']['search']['request']['indices'][0]

    def get_sensitivity (self, json):
        return json['sensitivity']

    def get_windowsize (self, json):
        return json['window_size']

    def get_indexdoctype (self, json):
        return json['document']

    def replace_queryrange(self, target_json, payload_json):
        """ we're looking for 'query' """
        target_json['input']['search']['request']['body']['query']['range'] = payload_json
        return target_json






