# Serverless Boilerplate with Python

Boilerplate includes:

- Cognito Custom Auth (JWTs)
    - bearer auth
    - group auth
    - post confirmation hook and adding user to group
- Logging
- Common API responses
- A Websocket example

# Requirements

- [Serverless Framework](https://serverless.com)
- Python 3.7+, I recommend using [Pipenv](https://github.com/pypa/pipenv)
- NPM and Node
- AWS Account
- Docker

## Running in Linux/Non-Linux

This framework uses the `serverless-python-requirements` plugin which will use docker to package our application. If using a Mac or Windows edit the `customs.yml` file:

```yaml
pythonRequirements:
  dockerizePip: non-linux # Change this if running in linux
```
Comment out that line if running in a linux OS.

# Unit Tests
Use https://nose.readthedocs.io/en/latest/ as the runner
```bash
pipenv install nose --dev
nosetests
```

# ENVIRONMENT Variables

Environment variables are passed through the lambda functions via `serverless.yml` and `customs.yml` depending on the stage set. Override them in these two yaml files.

|Variable|Description|Default|
|---|---|---|
|REGION|AWS region|ap-southeast-2|
|STAGE|One of: local, dev, test, stage, prod|dev|
|USER_POOL_ID|Cognito user pool ID, will be in the terraform output| - |
|APP_CLIENT_ID|User pool client id in the terraform output| - |
|LOG_LEVEL| The logging level| `local`, `dev`, `test` have logging set to `DEBUG`. `stage` and `prod` set to `WARNING`

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
- optionally provision a Cognito user pool if enabled -- see [Cognito Pools](#cognito-pools) below

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

# Websockets

You can test the websocket connection with this sample payload:

*action* is the route, everything else is in the `event.body`
```json
{"action": "echo", "sampleItem": "Hello World!"}
```

Connect using wscat:
```bash
npm i wscat
wscat -c <MyEndpoint>
```

The endpoint is different depending if you used a custom domain or not. Check the output of serverless deploy for the URL.

**Note**: At the time of writing AWS was using an outdated version of botocore which is why we fixed a working version in the Pipfile. If this doesn't work for you, generate a requirements.txt to fix the versions of what you need. We will revisit and remove that at a later date.

Check out this [stackoverflow post](https://stackoverflow.com/questions/55295305/aws-boto3-unknownserviceerror-unknown-service-apigatewaymanagementapi)

# Cognito Pools

## Default Domain

You can override the default variable `enable_cognito_user_pool` to `true` if choosing to create a pool. It will create a user pool with implicit and code oauth flows. Ensure that you change the `oauth_flows` variable as well to include the proper domain.

The outputs will give the Cognito endpoint for use in the `/auth` folder functions

## Custom Cognito Domain

By default, `enable_cognito_custom_domain` is set to `false` so you will get an AWS endpoint for the current workspace. Switch this to `true` if you want to attach a custom domain to the user pool. There are a few caveats that come with this option:

1. You need an A record at the root. The root changes if you have multiple dot entries. e.g. dev.auth.mydomain.com, you need an A record for auth.mydomain.com

2. TLS certificates need to sit in `us-east-1` region for legacy reasons as documented by AWS here: https://forums.aws.amazon.com/thread.jspa?messageID=880827

The certificate generated for a custom domain by default has the following name:
`[workspace].auth.[mydomain]`

With the following 3 additional domains:
- `*.[workspace].auth.[mydomain]`
- `.auth.[mydomain]`
- `*.[mydomain]`

*Note
There is an open issue with DNS validation [here](https://github.com/terraform-providers/terraform-provider-aws/issues/8597)
