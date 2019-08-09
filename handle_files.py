import json

class FileHandler:
    def __init__(self):
        self.sites = []
    #convert .txt files, to lists with JSON objects
    def create_json(self, raw_file):
        formated_file = []
        with open(raw_file) as site_file:
            for item in site_file:
                json_string = item.replace("'", "\"")
                site = json.loads(json_string)
                formated_file.append(site)
        return formated_file
            

    #concats the site name with site code for the status tab
    def groups_to_make(self, raw_file):
        sites_with_codes = self.create_json(raw_file)
        for site in sites_with_codes:
            self.sites.append(site['name'] + " - " + site['site_code'])

    #this is the function that will go over the large list
    #and find which of those ips / host names show up in Scrutinizer.
    def find_exporters(self, dictionary_of_ids, json_data, raw_file):
        print("adding exporters to group object")
        exporters_with_sites = self.create_json(raw_file)
        for item in exporters_with_sites:
            exporter_list = []
            exporter_name = item['device_name']
            site_name = item['site_name']            
            for data in json_data['rows']:
                exporter_ip = data[2]['exporterip']
                exporter_dns = data[2]['dns']
                exporter_sys = data[2]['sysname']
                if exporter_name ==  exporter_ip or exporter_name == exporter_dns  or exporter_name == exporter_sys:
                    exporter_list.append(exporter_ip)
                else:
                    pass
            for site_object in dictionary_of_ids:
                if site_name == site_object['site_name']:
                    for ip in exporter_list:
                        site_object['exporters'].append(ip)
        return dictionary_of_ids


            
            


