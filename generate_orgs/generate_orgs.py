#!/usr/bin/env python
#

"""
This generates deterministically random organizations as bulk process
"""

import sys
import ckanapi
import datetime
import random
import re

def name_generator(seed):
    words = [x.strip() for x in open('/usr/share/dict/words', 'r') if re.match('^[A-Za-z]*$', x)]
    random.seed(seed)
    while True:
        yield "-".join([random.choice(words) for i in range(3)]).lower()

def create_root_organization(api, name):
    print("Creating root organization %s" % name)
    api.call_action('organization_create', {
        'name': name,
        'extras': [{'key': 'public_adminstration_organization', 'value': 'true'}]
    })
    return name

def create_organization(api, name, parent_name):
    print("Creating organization %s" % name)
    org = api.call_action('organization_create', {
        'name': name,
        'extras': [{'key': 'public_adminstration_organization', 'value': 'true'}],
        'groups': [{"capacity": "public", "name": parent_name}]
    })
    return name

if __name__ == '__main__':

    usage = """
    Usage: ./organize_orgs.py API_URL API_KEY NUM_ROOTS NUM_LEVELS NUM_CHILDREN
    API_URL:      Url to CKAN excluding api directory and without trailing forward slash,
                  e.g. http://beta.opendata.fi/data
    API_KEY:      API key of the authorized user whose permissions are used for the requests,
                  e.g. 12345678-90ab-f000-f000-f0d9e8c7b6aa
    NUM_ROOTS:    Number of root organizations
    NUM_LEVELS:   Depth of organization hierarchy
    NUM_CHILDREN: Number of children per level"""



    if len(sys.argv) != 6:
        print usage
        sys.exit()

    binary_name, api_url, api_key, num_roots, num_levels, num_children = sys.argv
    num_roots, num_levels, num_children = int(num_roots), int(num_levels), int(num_children)

    example_id = "generate_orgs-{:%Y%m%d%H%M%S%f}".format(datetime.datetime.utcnow())

    api = ckanapi.RemoteCKAN(api_url,
                                  apikey=api_key,
                                  user_agent='avoindata_ckanapi_organize_orgs/1.0 ({0})'.format(example_id))

    names = name_generator(num_roots * num_levels + num_children)
    root_ids = [create_root_organization(api, next(names)) for i in range(num_roots)]

    def create_children(parent_id):
        return [create_organization(api, next(names), parent_id) for i in range(num_children)]

    def create_level(parent_ids):
        return [x for parent_id in parent_ids for x in create_children(parent_id)]

    level_ids = root_ids
    for level in range(num_levels):
        level_ids = create_level(level_ids)



def old():
    all_organizations = ckan_api.action.organization_list(all_fields=True)
    print "Read organizations from csv file:"
    with open(sys.argv[3], 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            for org in all_organizations:
                csv_org  = row[0].decode('windows-1252')
                if csv_org == org['display_name']:
                    full_org = ckan_api.action.organization_show(id=org['id'], include_datasets=False)
                    extras = full_org.get('extras', [])
                    is_public = 'false'
                    for extra in extras:
                        if extra['key'] == 'public_adminstration_organization':
                            is_public = extra['value']
                    if is_public == 'true':
                        print "Moving org: " + full_org['name'] + " under parent org: " + parent_org['name']
                        del full_org['groups'][:]
                        full_org['groups'].append({"capacity": "public", "name": parent_org['name']})
                        updated_org = ckan_api.call_action('organization_update', full_org)










