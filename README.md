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

Compose is the open source module powering the [Hue SQL Assistant](http://gethue.com). It comes as Web service for querying any [Databases & Data Warehouses](https://docs.gethue.com/administrator/configuration/connectors/) or building your own [Cloud SQL Editor](https://docs.gethue.com/developer/components/). Contributions are welcome and more modules are on the way (Files, Catalog...).


<img src="https://cdn.gethue.com/uploads/2020/02/quick-query-component.jpg" width="450">


# Start

Hello World query

    curl -u hue:hue -X POST http://localhost:8005/editor/v1/query/sqlite --data 'snippet={"statement":"SELECT 1000, 1001"}'

Docker

    docker run -it -p 8005:8005 gethue/compose:latest

Pypi

    pip install gethue

    compose migrate
    compose createsuperuser
    compose start

Live docs

* https://api.gethue.com/api/schema/swagger-ui/
* https://api.gethue.com/api/schema/redoc/


# Dev

One time

    git clone https://github.com/gethue/compose.git; cd compose
    ./install.sh  # If you want a Python virtual-env
    pre-commit install

Start API

    source python_env/bin/activate
    cd compose
    python3 compose/manage.py runserver 0.0.0.0:8005

Config

    compose/conf/local_settings.py

Checks

    pre-commit run --all-files
    pytest
