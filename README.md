# Serverless Boilerplate with Python
Boilerplate includes:

- Cognito Custom Auth (JWTs)
    - basic auth
    - group auth
    - post confirmation hook and adding user to group
- Logging
- Common API responses
- DynamoDB Example

# Requirements
- Serverless Framework
- Python 3.7+, I recommend using [Pipenv](https://github.com/pypa/pipenv)
- NPM and Node
- AWS Account

# DynamoDB Locally
By default, the pynamodb classes point to `localhost:8000`. These need to be overwritten when the function runs. Do not specify read and write capacity limits on the classes themselves because that will be handled in the infrastructure code.

```bash
npm install -g dynalite
dynalite --port 8000 --path local.db
```
# ENVIRONMENT Variables
dynamodb.ap-southeast-2.amazonaws.com
# Helper Scripts

## Creating Tables Locally
```bash
pipenv run python -m scripts.createTables
```