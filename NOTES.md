# hue == compose

hue5 --> gethue/compose
  hue --> compose
    editor
    connectors
    iam (auth, users, orgs..)
    documents
    scheduler, catalog, storage, ..
    ml
    docs, tools, docker, kubernetes...
  compose-ui

  e.g. Single or multi repo: https://github.com/kubernetes projects (docs, demos, roadmap etc?) Single++

  docker
  docker-compose

  pypi modules full compose
  k8s: analytics, metrics, tracing, logs

  clean license
  overall archi repo and hue integration. same with ref architecture diagram. blog post on all improvements and deep dive in some of the topics: evolving + better practicse/learnings

# API

Clean, skeletons for very modern. Templates to fill-up from Hue 4 code when switching. Hue 4 will pip install the Hue 5 modules.
Keeping Hue 5 as name, but API apps in "new repo" (folder or git, named "compose").
Runs on 8005

## Auth

CORS
No CSRF needed with JWT (no [auto creds](https://security.stackexchange.com/questions/170388/do-i-need-csrf-token-if-im-using-bearer-jwt))

### Ask for JWT token

    curl -X POST -d "username=hue&password=hue" http://localhost:8000/api-token-auth/

    curl -X POST http://localhost:8000/query/ --data 'snippet={"statement":"SELECT 1000, 1001"}' -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6Imh1ZSIsImV4cCI6MTYxMjk3MTc0MywiZW1haWwiOiJodWVAZ2V0aHVlLmNvbSIsIm9yaWdfaWF0IjoxNjEyODg1MzQzfQ._HViX-D9h1ZfcXPAaY4KL0SNkx7MvXCH41T8Upkja3o" | jq

### Basic Auth to avoid token

    curl -u hue:hue

### Demo

    HTML Auth https://drive.google.com/file/d/1XXYZPzHagnIWrOpxtbQcWdjMmTyFXZuQ/view?usp=sharing

## Editor

### Execute sync

    curl -u hue:hue -X POST http://localhost:8000/notebook/api/execute/sqlite --data 'snippet={"statement":"SELECT 1000, 1001"}'

## Dev

    ./install.sh

    source python_env/bin/activate

    curl -u hue:hue -X POST http://localhost:8000/v1/editor/execute/sqlite --data 'snippet={"statement":"SELECT 1000, 1001"}' | jq

## Docker

    docker build hue -t gethue/compose-api:latest -f hue/docker/Dockerfile
    docker push gethue/compose-api:latest

    docker run -it -p 8005:8000 gethue/compose-api:latest

    curl -X POST http://localhost:8000/notebook/api/execute/sqlite --data 'snippet={"statement":"SELECT 1000, 1001"}'  | jq

### Official

    docker run -it -p 8000:8005 gethue/compose-api:latest

    curl -u hue:hue -X POST http://localhost:8000/notebook/api/execute/sqlite --data 'snippet={"statement":"SELECT 1000, 1001"}'

    curl -X POST -d "username=hue&password=hue" http://localhost:8000/api-token-auth/
    curl -X POST http://localhost:8000/query/ --data 'snippet={"statement":"SELECT 1000, 1001, \"hello\""}' -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6Imh1ZSIsImV4cCI6MTYxMjk3MTc0MywiZW1haWwiOiJodWVAZ2V0aHVlLmNvbSIsIm9yaWdfaWF0IjoxNjEyODg1MzQzfQ._HViX-D9h1ZfcXPAaY4KL0SNkx7MvXCH41T8Upkja3o" | jq

MySql

    mysql://hue:hue@127.0.0.1:3306/hue
    docker run -it --network host gethue/compose-api:latest

## CI

Done

    https://pre-commit.com/hooks.html + GH Action
    black hue
    isort --profile django hue

TODO

    pylance?
    mypy?
    coverable
    pytest
    pylint?
    More https://pre-commit.com/hooks.html ?

    [![Join the chat at https://gitter.im/timothycrosley/isort](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/timothycrosley/isort?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
    [![Downloads](https://pepy.tech/badge/isort)](https://pepy.tech/project/isort)
    [![DeepSource](https://static.deepsource.io/deepsource-badge-light-mini.svg)](https://deepsource.io/gh/pycqa/isort/?ref=repository-badge)
______

## Pypi

    https://packaging.python.org/tutorials/packaging-projects/#generating-distribution-archives

    python3 -m pip install --upgrade build

    python3 -m build

    python3 -m twine upload --repository testpypi dist/*
    python3 -m pip install --index-url https://test.pypi.org/simple/ gethue

    https://test.pypi.org/project/gethue/


    python3 -m twine upload dist/*
    python3 -m pip install gethue
    https://pypi.org/project/gethue/


    from compose.editor import execute

    execute('SELECT 1', url="sqlite:///../db.sqlite3")
    execute('SELECT 1', {"url: "", ...})
    execute('SELECT 1', connector_id)

    execute('SELECT 1', {connector}, sync=True)

## API Docs / UI

    request.data not POST

    http://127.0.0.1:8000/api/schema/swagger-ui/#/

    {"snippet":{"statement":"SELECT 1000, 1001"}}


Good:
  https://github.com/tfranzel/drf-spectacular
  redoc better than Swagger http://127.0.0.1:8000/api/schema/redoc/#tag/editor
Dead:
    https://www.django-rest-framework.org/api-guide/requests/
    https://github.com/axnsan12/drf-yasg/
