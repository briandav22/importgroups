import requests
import json

class Mapping:
    def __init__(self, authToken):
        self.authToken = authToken
        self.report_object = None
    
    #used to create the groups on the status tab. Whatever is passed in as
    #group name will be what shows up.
    def create_group(self, group_name):
        self.report_object = {
            "rm":"mappingConfiguration",
            "name": group_name,
            "groupType":"flash",
            "action":"mapconfNewGroup",
            "authToken": self.authToken
        }

    def get_all_groups(self):
        self.report_object = {
            "rm":"loadMap",
            "maxRows": "100000",
            "offset": "0",
            "action": "loadTreeGraph",
            "defaultGroupOnTop": "1",
            "authToken": self.authToken
        }


    def map_exporter_id(self):
        print("Finding IDs for each Group")
        self.report_object = {
        "rm": "mappingConfiguration",
        "view": "object_configuration",
        "session_state": json.dumps({"query_limit":{"offset":"0","max_num_rows":"100000"},"hostDisplayType":"ip"}),
        "authToken":self.authToken}

    def find_exporters_site_id(self):
        print("finding all exporters that exhist in Scrutinizer")
        self.report_object  = {
            "rm": "manageExporters",
            "view":"ManageExporters",
            "session_state": json.dumps({"query_limit":{"offset":"0","max_num_rows":"100000"},"hostDisplayType":"ip"}),
            "authToken":self.authToken}




    def add_exporter(self, exporter_list = None, group_id = None):
        self.report_object = {
            "rm": "mappingConfiguration",
            "action": "mapconfSaveGroupMem",
            "json": json.dumps({"added":exporter_list}),
            "mapid": group_id,
            "authToken": self.authToken
        }

#used to make request to Scrutinizer API
class Requester:
    def __init__(self, scrutinizer_host):
        self.scrutinizer_host = scrutinizer_host
    def request_data(self, report_object):
        response = requests.get("{}/fcgi/scrut_fcgi.fcgi?".format(self.scrutinizer_host), params=report_object, verify=False)
        return response.json()

#handles creating the group object that is used to move Exporters into Groups
class GroupObject:
    def __init__(self):
        self.group_data = []


    def create(self, json_data):
        print("creating a object containing all new groups")
        for site in json_data['results']:
            site_info = site['lbl'].split(" -")
            site_name = site_info[0]
            site_id = site_info[1].strip(" ")
            group_id = site['id']
            site_with_id = {
                    "site_name" :site_name,
                    "site_id": site_id,
                    "group_id": group_id,
                    "exporters": [],
                    "ids":[]
            }
            self.group_data.append(site_with_id)

    def map_ids(self, group_object, json_data):
        print("Finding IDs for each exporter")
        for site in group_object:
            for exporter in site['exporters']:
                    for exporter_ip in json_data['rows']:
                            if exporter == exporter_ip[1]['ip']:
                                    site['ids'].append(exporter_ip[1]['id'])
        return group_object      

