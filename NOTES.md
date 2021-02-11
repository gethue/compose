# hue

Add mypy, black, coverable ... like spacy
https://github.com/python-poetry/poetry ?
https://pre-commit.com/ black...

    black hue
    isort --profile django hue

## Query

    curl -X POST http://localhost:8000/query/ --data 'snippet={"statement":"SELECT 1000, 1001"}' | jq

## Auth

    curl -X POST -d "username=hue&password=hue" http://localhost:8000/api-token-auth/

    curl -X POST http://localhost:8000/query/ --data 'snippet={"statement":"SELECT 1000, 1001, \"hello\""}' -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6Imh1ZSIsImV4cCI6MTYxMjk3MTc0MywiZW1haWwiOiJodWVAZ2V0aHVlLmNvbSIsIm9yaWdfaWF0IjoxNjEyODg1MzQzfQ._HViX-D9h1ZfcXPAaY4KL0SNkx7MvXCH41T8Upkja3o" | jq

## Dev

    ./install.sh

    source python_env/bin/activate


    curl -X POST http://localhost:8000/notebook/api/execute/mysql --data 'snippet={"statement":"SELECT 1000, 1001"}' | jq


## Docker

    docker build hue -t gethue/compose-api:latest -f hue/docker/Dockerfile

    docker push gethue/compose-api:latest

    docker run -it -p 9003:8000 gethue/compose-api:latest

    curl -X POST http://localhost:9003/notebook/api/execute/mysql --data 'snippet={"statement":"SELECT 1000, 1001"}'  | jq

### Official

    Right now expects a: mysql://hue:hue@127.0.0.1:3306/hue

    docker run -it --network host -p 9003:8000 gethue/compose-api:latest

    curl -X POST http://localhost:8000/notebook/api/execute/mysql --data 'snippet={"statement":"SELECT 1000, 1001"}'

    curl -X POST -d "username=hue&password=hue" http://localhost:9003/api-token-auth/

    curl -X POST http://localhost:8000/query/ --data 'snippet={"statement":"SELECT 1000, 1001, \"hello\""}' -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6Imh1ZSIsImV4cCI6MTYxMjk3MTc0MywiZW1haWwiOiJodWVAZ2V0aHVlLmNvbSIsIm9yaWdfaWF0IjoxNjEyODg1MzQzfQ._HViX-D9h1ZfcXPAaY4KL0SNkx7MvXCH41T8Upkja3o" | jq

    Probably worth quick use of https://www.django-rest-framework.org/topics/api-clients/#installation-with-node (and we fix it as needed).

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


## API Docs / UI

    request.data not POST

    http://127.0.0.1:8000/query/

    {"snippet":{"statement":"SELECT 1000, 1001"}}


    https://www.django-rest-framework.org/api-guide/requests/
    https://github.com/axnsan12/drf-yasg/
