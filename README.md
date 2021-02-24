[![PyPI version](https://badge.fury.io/py/gethue.svg)](https://badge.fury.io/py/gethue)
[![Test Status](https://github.com/gethue/compose/workflows/Python%20CI/badge.svg?branch=master)](https://github.com/gethue/compose/actions?query=Python%20CI)
[![DockerPulls](https://img.shields.io/docker/pulls/gethue/compose.svg)](https://registry.hub.docker.com/u/gethue/compose/)
![GitHub contributors](https://img.shields.io/github/contributors-anon/gethue/compose.svg)
[![Code coverage Status](https://codecov.io/gh/gethue/compose/branch/master/graph/badge.svg)](https://codecov.io/gh/gethue/compose)
[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://pypi.org/project/gethue/)

<kbd><img src="https://raw.githubusercontent.com/gethue/compose/master/docs/images/compose_button.png"/></kbd>

Compose
-------

[Hue Query Editor](http://gethue.com) component.
Compose is a mature open source SQL Assistant for querying any [Databases & Data Warehouses](https://docs.gethue.com/administrator/configuration/connectors/).

Many companies and organizations use Hue to quickly answer questions via self-service querying.

* 1000+ customers
* Top Fortune 500

are executing 1000s of queries daily.

Compose is also ideal for building your own [Cloud SQL Editor](https://docs.gethue.com/developer/components/) and any contributions are welcome.


# Dev

Python style: [black](https://github.com/psf/black)

One time:

    git clone https://github.com/gethue/compose.git; cd compose
    ./install.sh
    pre-commit install

Start API:

    source python_env/bin/activate
    cd compose
    python manage.py runserver

# API

* https://demo.gethue.com/api/api/schema/swagger-ui/
* https://demo.gethue.com/api/api/schema/redoc/

    curl -u hue:hue https://demo.gethue.com/api/v1/editor/query/sqlite --data 'snippet={"statement":"SELECT 1000, 1001"}'

Note: on local host or docker strip one of the `/api` of the URL
