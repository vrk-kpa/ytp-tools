
# API of Avoindata.fi

This directory includes documentation and example code on how to use the CKAN API of Avoindata.fi/Yhteentoimivuuspalvelut. The web service uses CKAN to provide a catalog of open datasets. Through the API, an organization can add their datasets into the service.

In the CKAN data model, *users* and *datasets* belong to *organizations*. Organizations own datasets and mandate permissions. Datasets describe a single, logical set of open data and can hold *resources* which are files or external links.

The following code examples are provided here:

* **ckan_api_example_ckanapi_library.py:** A Python example that uses the [ckanapi][ckanapilib] library in making the HTTP requests. If you are using Python, it is advisable to use this library.
* **ckan_api_example_raw_http.py:** A low-level Python example that uses the [requests][requests] library in making forming pure HTTP requests. If you need to form the HTTP requests by yourself for some reason, this example gives you some basic pointers.

## Getting started

First you need to acquire a user account and an API key:

1. Register to [beta.avoindata.fi](https://beta.avoindata.fi) (or try the direct link https://beta.avoindata.fi/fi/user/register ).
2. Login and go to your user profile via your name in the top bar.
3. Copy-paste your private API key from the user profile.

Then you can install the prequisites for the code examples:

    sudo apt-get install python-virtualenv
    virtualenv avoindata_api_env
    source avoindata_api_env/bin/activate
    pip install requests
    pip install ckanapi

To try out the examples, run the scripts using your API key:

    wget https://raw.github.com/yhteentoimivuuspalvelut/ytp-tools/master/api_ckan/ckan_api_example_ckanapi_library.py
    python ckan_api_example_ckanapi_library.py https://beta.opendata.fi/data 12345678-90ab-f000-f000-f0d9e8c7b6aa

    wget https://raw.github.com/yhteentoimivuuspalvelut/ytp-tools/master/api_ckan/ckan_api_example_http.py
    python ckan_api_example_http.py https://beta.opendata.fi/data 12345678-90ab-f000-f000-f0d9e8c7b6aa

### Name vs. id vs. title

CKAN has three different name-like variables for organizations and datasets. An *id* is a random uuid4 that is used to point to a specific object in the database. A *title* is the human-readable name of the dataset or organization. A *name* is a developer-friendly id for an organization or dataset and must consist of alphanumeric character, dashes and underscores. A name must be unique, and when using the web interface, the name is automatically derived from the title.

Many API functions take an *id* as a parameter, but most of the time this actually (and a bit confusingly) means *id-or-name*. Thus unless you really specifically want to, you can use the *name* attribute and pass it to functions like organization_show.

### Required attributes of a new dataset

As our service is constantly developing, we may make changes to the data schema and new required attributes may arise. If you are having trouble creating a new dataset via the API, you can first create a new dataset in the web interface by hand, and then fetch its details from the API with package_show to see which attributes it has.

## Known issues

* Deleting an organization or dataset (organization_delete and package_delete) in CKAN does not actually delete the organization or dataset, but merely changes their state to deleted. Successive creations using the same names will fail, complaining that there is already an entity with that name. Deleting them from the Web interface seem to delete them completely.
* Some methods may falsely return a 405 Not Allowed, for example when requesting for the details of a dataset that does not exist.

## Disclaimer

As this is a development version of the service, any data you import/create in the service can be lost without notice at any time. Furthermore, new software is deployed daily (sometimes several times per day) to the servers from the master branch, so it is excepted that the server is sometimes down and things will break. However, the API should be much more stable and less buggy than the web interface.

## Help and support

If you want a more mature and stable, but more generic CKAN playground, you can also try using the [API](http://demo.ckan.org/api) of the [CKAN demo instance](http://demo.ckan.org). If you are having trouble with our API, create an [issue at Github](https://github.com/yhteentoimivuuspalvelut/ytp/issues) or join the discussion at [avoindata.net](http://avoindata.net/questions/suomen-avoimen-datan-portaalin-rakentaminen).

## Further reading

* [CKAN API documentation][ckanapidocs]
* [CKAN API client library and CLI][ckanapilib]
* [CKAN API client libraries in other languages (old docs, possibly obsolete)][otherclients]

[ckanapidocs]: http://docs.ckan.org/en/latest/api/index.html
[ckanapilib]: https://github.com/okfn/ckanapi
[requests]: http://requests.readthedocs.org/en/latest/
[otherclients]: http://docs.ckan.org/en/ckan-1.7.1/api.html#clients
