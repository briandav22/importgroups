from create_groups import Mapping, Requester, GroupObject
from handle_files import FileHandler
import requests
import requests.packages.urllib3
import json
import sys


requests.packages.urllib3.disable_warnings()
# add in variables to Script
scrutinizer_url = 'https://your_scrutinizer_here'
scrutinizer_authToken = 'your_auth_token_here'
exporter_sites = 'exporters_sites.txt'
site_codes = 'site_codes.txt'

# initiate classes.
group_maker = Mapping(authToken=scrutinizer_authToken)
file_handler = FileHandler()
scrut_requester = Requester(scrutinizer_url)
group_object = GroupObject()
create_mode = False
try:
    if sys.argv[1] == '-create':
        create_mode = True
except:
    pass

# create groups in Scrutinizer
if create_mode == True:
        site_counter = 1
        file_handler.groups_to_make(site_codes)
        number_of_sites = len(file_handler.sites)
        for site in file_handler.sites:
                print("creating group {} of {}".format(site_counter, number_of_sites))
                group_maker.create_group(site)
                request_result = scrut_requester.request_data(group_maker.report_object)
                try:
                        if request_result['lbl']:
                                print("Created Group {}".format(request_result['lbl']))
                except:
                        pass
                try:
                        if request_result['err']:
                                print(request_result['err'] + ' ' + "Tried to Create {}".format(site))
                except Exception as e:
                        pass
                site_counter += 1

# create group object used for final insert.

group_maker.get_all_groups()
all_groups = scrut_requester.request_data(group_maker.report_object)

group_object.create(all_groups)

# grab all possible exporters, to match against list

group_maker.find_exporters_site_id()
all_exporters = scrut_requester.request_data(group_maker.report_object)

# add exporters to each site in object
dictionary_with_ids = file_handler.find_exporters(
    group_object.group_data, all_exporters, exporter_sites)


# map exporters to exporter_ids
group_maker.map_exporter_id()
exporters_with_ids = scrut_requester.request_data(group_maker.report_object)
groups_with_ids = group_object.map_ids(dictionary_with_ids, exporters_with_ids)


# move exporters into groups, based off IDs
print("Starting to Add Exporters to Groups")
for groups in groups_with_ids:
    group_id = groups['group_id']
    exporter_ids = groups['ids']
    # only worry about moving exporters if there are any.
    if len(exporter_ids) > 0:
        group_maker.add_exporter(exporter_list=exporter_ids, group_id=group_id)
        groups_added = scrut_requester.request_data(group_maker.report_object)
        group_info = groups_added['added'][0]
        print("added {} to group {}".format(
            group_info['lbl'], group_info['parent_gname']))
