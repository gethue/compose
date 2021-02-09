# hue5



## Query

    curl -X POST http://localhost:8000/query/ --data 'snippet={"statement":"SELECT 1000, 1001"}'  | jq

## Auth

    curl -X POST -d "username=hue&password=hue" http://localhost:8000/api-token-auth/

    curl -X POST http://localhost:8000/query/ --data 'snippet={"statement":"SELECT 1000, 1001, \"hello\""}' -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6Imh1ZSIsImV4cCI6MTYxMjk3MTc0MywiZW1haWwiOiJodWVAZ2V0aHVlLmNvbSIsIm9yaWdfaWF0IjoxNjEyODg1MzQzfQ._HViX-D9h1ZfcXPAaY4KL0SNkx7MvXCH41T8Upkja3o" | jq

## Dev

    ./install.sh

    source python_env/bin/activate


    curl -X POST http://localhost:8000/notebook/api/execute/mysql --data 'snippet={"statement":"SELECT 1000, 1001"}'  | jq


## Docker

    docker build hue5 -t gethue/compose-api:latest -f hue5/docker/Dockerfile

    docker push gethue/compose-api:latest

    docker run -it -p 9003:8000 gethue/compose-api:latest

    curl -X POST http://localhost:9003/notebook/api/execute/mysql --data 'snippet={"statement":"SELECT 1000, 1001"}'  | jq

### Official

    docker run -it --network host -p 9003:8000 gethue/compose-api:latest
    Right now expects a: mysql://hue:hue@127.0.0.1:3306/hue
    curl -X POST http://localhost:8000/notebook/api/execute/mysql --data 'snippet={"statement":"SELECT 1000, 1001"}'


    curl -X POST -d "username=hue&password=hue" http://localhost:9003/api-token-auth/

    curl -X POST http://localhost:8000/query/ --data 'snippet={"statement":"SELECT 1000, 1001, \"hello\""}' -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6Imh1ZSIsImV4cCI6MTYxMjk3MTc0MywiZW1haWwiOiJodWVAZ2V0aHVlLmNvbSIsIm9yaWdfaWF0IjoxNjEyODg1MzQzfQ._HViX-D9h1ZfcXPAaY4KL0SNkx7MvXCH41T8Upkja3o" | jq

    Probably worth quick use of https://www.django-rest-framework.org/topics/api-clients/#installation-with-node (and we fix it as needed).
