#!/usr/bin/env python
#

"""
This organizes organizations as bulk process
"""

import sys
import ckanapi
import datetime
import pprint
from ckan.logic import NotFound
import csv

if __name__ == '__main__':

    usage = "\
    Usage: ./organize_orgs.py API_URL API_KEY ORG_LIST PARENT_ORG\n\
    API_URL:    Url to CKAN excluding api directory and without trailing foreward slash,\n\
                e.g. http://beta.opendata.fi/data\n\
    API_KEY:    API key of the authorized user whose permissions are used for the requests,\n\
                e.g. 12345678-90ab-f000-f000-f0d9e8c7b6aa\n\
    ORG_LIST:   CSV file listing organizations which we want move under different organization\n\
    PARENT_ORG: Organization which will be the new parent organization"



    if len(sys.argv) != 5:
        print usage
        sys.exit()

    example_id = "organize_orgs-{:%Y%m%d%H%M%S%f}".format(datetime.datetime.utcnow())
    print "All names in these examples are tagged with", example_id

    ckan_api = ckanapi.RemoteCKAN(sys.argv[1],
                                  apikey=sys.argv[2],
                                  user_agent='avoindata_ckanapi_organize_orgs/1.0 ({0})'.format(example_id))

    print "Find parent organization:"
    try:
        parent_org = ckan_api.action.organization_show(id=sys.argv[4])
    except NotFound:
        print "Parent org " + sys.argv[4] + " not found."
        sys.exit(1)

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










