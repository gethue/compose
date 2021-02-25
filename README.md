[![PyPI version](https://badge.fury.io/py/gethue.svg)](https://badge.fury.io/py/gethue)
[![Test Status](https://github.com/gethue/compose/workflows/Python%20CI/badge.svg?branch=master)](https://github.com/gethue/compose/actions?query=Python%20CI)
[![DockerPulls](https://img.shields.io/docker/pulls/gethue/compose.svg)](https://registry.hub.docker.com/u/gethue/compose/)
![GitHub contributors](https://img.shields.io/github/contributors-anon/gethue/compose.svg)
[![Code coverage Status](https://codecov.io/gh/gethue/compose/branch/master/graph/badge.svg)](https://codecov.io/gh/gethue/compose)
[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://pypi.org/project/gethue/)

<kbd><img src="https://raw.githubusercontent.com/gethue/compose/master/docs/images/compose_button.png"/></kbd>

Compose
-------

[Query Editor component](https://docs.gethue.com/developer/components/scratchpad/)

Compose is the open source module powering the [Hue SQL Assistant](http://gethue.com). It comes as Web service for querying any [Databases & Data Warehouses](https://docs.gethue.com/administrator/configuration/connectors/) or building your own [Cloud SQL Editor](https://docs.gethue.com/developer/components/). Contributions are welcome.

# Dev

One time

    git clone https://github.com/gethue/compose.git; cd compose
    ./install.sh
    pre-commit install

Start API

    source python_env/bin/activate
    cd compose
    python manage.py runserver

# API

Hello World query

    curl -u hue:hue https://api.gethue.com/v1/editor/query/sqlite --data 'snippet={"statement":"SELECT 1000, 1001"}'

Live docs

* https://api.gethue.com/api/schema/swagger-ui/
* https://api.gethue.com/api/schema/redoc/

Docker

    docker run -it -p 8005:8005 gethue/compose:latest
