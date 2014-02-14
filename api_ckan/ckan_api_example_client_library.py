#!/usr/bin/env python
#

"""
This is a short demo on using the CKAN API of Avoindata.fi
This code uses the ckanclient library, see https://github.com/okfn/ckanclient
For information regarding the API itself, see http://docs.ckan.org/en/latest/api.html
"""

import ckanclient
import sys


if __name__ == '__main__':

    usage = "\
    Usage: ./ckan_api_example.py API_URL API_KEY\n\
    API_URL: Url to CKAN API including api directory without trailing foreward slash,\n\
             e.g. http://alpha.avoindata.fi/data/api\n\
    API_KEY: API key of the authorized user whose permissions are used for the requests,\n\
             e.g. 12345678-90ab-f000-f000-f0d9e8c7b6aa\n"

    if len(sys.argv) != 3:
        #log.error('Wrong number of arguments')
        print usage
        sys.exit()

    ckan = ckanclient.CkanClient(base_location=sys.argv[1], api_key=sys.argv[2])

    # Get the package list.
    package_list = ckan.package_register_get()
    print package_list
    
    # Collect the package metadata.
    package_entity = {
        'name': my_package_name,
        'url': my_package_url,
        'download_url': my_package_download_url,
        'tags': my_package_keywords,
        'notes': my_package_long_description,
    }

    # Register the package.
    ckan.package_register_post(package_entity)

    # Get the details of a package.
    ckan.package_entity_get(package_name)
    package_entity = ckan.last_message
    print package_entity

    # Update the details of a package.
    ckan.package_entity_get(package_name)
    package_entity = ckan.last_message
    package_entity['url'] = new_package_url
    package_entity['notes'] = new_package_notes
    ckan.package_entity_put(package_entity)
