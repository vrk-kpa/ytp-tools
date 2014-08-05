#!/usr/bin/env python
#

"""
This is a short demo on using the CKAN API of Avoindata.fi
This code uses the ckanapi library, see https://github.com/ckan/ckanapi
For information regarding the API itself, see http://docs.ckan.org/en/latest/api/index.html
"""

import sys
import ckanapi
import datetime
import pprint


if __name__ == '__main__':

    usage = "\
    Usage: ./ckan_api_example.py API_URL API_KEY\n\
    API_URL: Url to CKAN excluding api directory and without trailing foreward slash,\n\
             e.g. http://alpha.opendata.fi/data\n\
    API_KEY: API key of the authorized user whose permissions are used for the requests,\n\
             e.g. 12345678-90ab-f000-f000-f0d9e8c7b6aa\n"

    if len(sys.argv) != 3:
        print usage
        sys.exit()

    example_id = "apitest-{:%Y%m%d%H%M%S%f}".format(datetime.datetime.utcnow())
    print "All names in these examples are tagged with", example_id

    ckan_api = ckanapi.RemoteCKAN(sys.argv[1],
                                  apikey=sys.argv[2],
                                  user_agent='avoindata_ckanapi_example/1.0 ({0})'.format(example_id))

    print "List all organizations:"
    all_organizations = ckan_api.action.organization_list()
    pprint.pprint(all_organizations)

    print "Get details of a single organization by id:"
    organization_helsinki = ckan_api.action.organization_show(id="helsinki")
    pprint.pprint(organization_helsinki)

    print "List first 10 datasets:"
    datasets = ckan_api.action.package_list(limit=10, offset=0)
    pprint.pprint(datasets)

    print "Create a new organization:"
    my_organization_name = 'z-avoindata-org-' + example_id
    try:
        new_organization = ckan_api.action.organization_create(
            name=my_organization_name,
            title='Z CKAN API ' + example_id)
        pprint.pprint(new_organization)
    except ckanapi.NotAuthorized:
        print 'Not authorized'

    print "Get details of the created organization:"
    my_organization = ckan_api.action.organization_show(id=my_organization_name)
    pprint.pprint(my_organization)

    # You can also create your datasets to the 'private person' Organization and not create your own
    # my_organization_name = 'yksityishenkilo'

    print "Create a new dataset:"
    my_dataset_name = 'z-avoindata-dataset-' + example_id
    try:
        dataset_parameters = {'name': my_dataset_name,
                              'title': 'Z CKAN API dataset ' + example_id,
                              'notes': 'This is a description of the dataset in the source language',
                              'license_id': 'Creative Commons Attribution 4.0',
                              'content_type': 'Paikkatieto,Avoin data,Ohjeet',
                              'collection_type': 'Open Data',
                              'owner_org': my_organization_name}

        new_dataset = ckan_api.action.package_create(**dataset_parameters)
        pprint.pprint(new_dataset)
    except ckanapi.NotAuthorized:
        print 'Not authorized'

    print "Get details of the created dataset:"
    my_dataset = ckan_api.action.dataset_show(id=my_dataset_name)
    pprint.pprint(my_dataset)

    print "Delete created dataset:"
    ckan_api.action.package_delete(id=my_dataset_name)

    print "Get state of the deleted dataset:"
    print ckan_api.action.dataset_show(id=my_dataset_name).get('state')

    print "Delete created organization:"
    if my_organization_name != 'yksityishenkilo':
        ckan_api.action.organization_delete(id=my_organization_name)
    else:
        print "Not even trying to delete the shared organization!"

    print "Get state of the deleted organization:"
    print ckan_api.action.organization_show(id=my_organization_name).get('state')
