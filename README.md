# hue5

## Query

    curl -X POST http://localhost:8000/query/ --data 'snippet={"statement":"SELECT 1000, 1001"}'  | jq

## Auth

    curl -X POST -d "username=hue&password=hue" http://localhost:8000/api-token-auth/

    curl -X POST http://localhost:8000/query/ --data 'snippet={"statement":"SELECT 1000, 1001, \"hello\""}' -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6Imh1ZSIsImV4cCI6MTYxMjkxMDk1NiwiZW1haWwiOiJodWVAZ2V0aHVlLmNvbSIsIm9yaWdfaWF0IjoxNjEyODI0NTU2fQ.cOMtrXt9AwIhr0P70mCZiqVph9fueX2UI5b14cbjhWg"
    | jq

# Dev

    ./install.sh

    source python_env/bin/activate


    curl -X POST http://localhost:8000/notebook/api/execute/mysql --data 'snippet={"statement":"SELECT 1000, 1001"}'  | jq
