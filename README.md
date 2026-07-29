# zero-deposit-fastapi
Fastapi app to meet Zero Deposit's technical task requirements


uv is used to handle project dependencies and python versioning, must be installed globally.

# uv run fastapi dev

the above command will install all dependencies and run the app in development.

# pytest tests/ -v

the above command will run all tests in the tests directory



Framework choices:
-Fastapi: lightweight & easily configurable API. Existing knowledge.
-SQLalchemy: seamless integration with SQL db. Automated mapping of ORMs (object relational models) and automates writing of SQL. again, existing knowledge.
-SQLite: localised file based DB
-pydantic: automated data validation on user data
-pytest: industry standard python testing library


AI use: GitHub Copilot Pro

Advantages:

Disadvantages:
 - overly verbose output, comments and variable names etc unnecessarily bloated, harder to read
 - (possibly a user limitation) hard to control, limited feedback. When building a complex system manually it is a slower and more involved process allowing you to chose correct solutions/fetures. AI handling of large tasks skips this step and makes all the decisions on your behalf without consent, result: unwanted / inefficient solutions.




 To test the individual routes:

(1) create a user:

curl -X 'POST' 'http://127.0.0.1:8000/api/v1/users/signup' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{ "password": "pass1234", "username": "mj_test1"}'

(2) login:

curl -X 'POST' 'http://127.0.0.1:8000/api/v1/users/login' -H 'accept: application/json' -H 'Content-Type: application/json'  -d '{
  "password": "pass1234",
  "username": "mj_test1"
}'

(3) access any route e.g. list properties (using returned JWT)

curl -X 'GET' 'http://127.0.0.1:8000/api/v1/properties' -H 'accept: application/json' -H 'authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtal90ZXN0MSIsImV4cCI6MTc4NTM2NTU1MH0.eyCxYSJE2gBRU5yQrAeUcYRMkHndUrh5zgT4B8nao-o'