[![PyPI version](https://badge.fury.io/py/hue.svg)](https://badge.fury.io/py/hue)
[![Test Status](https://github.com/gethue/compose/workflows/Python%20CI/badge.svg?branch=master)](https://github.com/gethue/compose/actions?query=workflow%3ATest)
[![DockerPulls](https://img.shields.io/docker/pulls/gethue/hue.svg)](https://registry.hub.docker.com/u/gethue/hue/)
![GitHub contributors](https://img.shields.io/github/contributors-anon/cloudera/hue.svg)
[![Code coverage Status](https://codecov.io/gh/gethue/compose/branch/master/graph/badge.svg)](https://codecov.io/gh/gethue/compose)
[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://pypi.org/project/hue/)

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

    ./install.sh
    pre-commit install

Start API:

    source python_env/bin/activate
    cd compose
    python manage.py runserver
