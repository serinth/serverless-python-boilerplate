# Serverless Boilerplate with Python
Boilerplate includes:

- Cognito Custom Auth (JWTs)
    - basic auth
    - group auth
    - post confirmation hook and adding user to group
- Logging
- Common API responses

# Requirements
- [Serverless Framework](https://serverless.com)
- Python 3.7+, I recommend using [Pipenv](https://github.com/pypa/pipenv)
- NPM and Node
- AWS Account
- Docker

# Unit Tests
Use https://nose.readthedocs.io/en/latest/ as the runner
```bash
pipenv install nose --dev
nosetests
```

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

# Deployment - Default AWS VPC

Ensure the domain is purchased and verified. Then create a wildcard certificate in ACM.
After that is done, run:
```bash
serverless create_domain
```

API Gateway should show a new custom domain. You won't need to run the above command again.

Then run:
```bash
serverless deploy
```

# Deployment Custom Infrastructure

The infrastructure code here is a bit more secure than using defaults. It also allows us to isolate the lambdas in private subnets and additionally provision databases required in the private subnet as well.

## 1. Create Infrastructure with Terraform
Instead of using cloudformation inside of the serverless framework, we opt to handle infrastructure code in Terraform for separation of concerns whereas we leave serverless to do more heavy lifting on CI/CD and code organization.

This example will create:
- a new VPC
- 2x public subnet
- 2x private subnet
- a NAT for outgoing calls for the private subnet lambdas (1 nat per subnet)
- tag all resources
- optionally provision a Cognito user pool if enabled

Initialize Terraform:
```bash
cd infrastructure
terraform init
terraform workspace new <ENVIRONMENT>
terraform plan
terraform apply
```

Replace `<Environment>` with the appropriate value. e.g. dev

Now you will need to grab the VPC security group ids and private subnet details to put into the [function definition yaml](https://serverless.com/framework/docs/providers/aws/guide/functions/) files so serverless knows where to deploy them.

The terraform scripts should output the security group ids for the VPC and subnet ids for the private subnets (where the lambda functions will go).

## 2. Deploy

Uncomment and replace the info in this section of `serverless.yaml`:
```yaml
  vpc:
    securityGroupIds:
    - <VPC security group id>
    subnetIds:
    - <private subnet id 1>
    - <private subnet id 2>
```

Ensure the domain is purchased and verified. Then create a wildcard certificate in ACM much like the Default deployment method.

After that is done, run:
```bash
serverless create_domain
serverless deploy
```
