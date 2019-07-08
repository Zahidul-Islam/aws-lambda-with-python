# Introducing AWS Lambda with Python and Serverless Framework

## Introducing to AWS Lambda

- AWS Lambda lets you run code without managing servers.
- You only pay for the compute time your app consume
- There is no charge when code is not running.
- You can run code with zero administration. Just upload your code and Lambda takes care of everything required to run and scale your code with high availability.
- You can set up your code to automatically trigger from other AWS services or call it directly from any web or mobile app

## AWS Lambda Limits 

### Runtime environment limitations:

- The disk space (`/tmp`) is limited to 512 MB
- The deployment package size is 50 MB (zipped, for direct upload)
- Memory range is from 128 MB to 3,008 MB, in 64 MB increments.
- Maximum execution timeout for a function is 900 seconds (15 minutes)
- Function environment variables is limited to 4 KB
- Function can have up to 5 layers

> The total unzipped size of the function and all layers can't exceed the unzipped deployment package size limit of 250 MB.

### Requests limitations by lambda:

- Request and response (synchronous calls) body payload size can be up to to 6 MB
- Event request (asynchronous calls) body can be up to 256 KB

## Serverless Tools

- Serverless Framework
- Apex
- ClaudiaJS
- AWS SAM CLI
- Zappa
- Other

## Getting started with Serverless

- Download the AWS CLI
  `$ pip install awscli --upgrade --user`
- Verify that AWS CLI installed correctly
  `$ aws --version`
- Install serverless framework
  `$ npm install -g serverless`
- Enter IAM keys in the serverless configuration
  `$ serverless config credentials --provider aws --key xxxxxxxxxxxxxx --secret xxxxxxxxxxxxxx`

## Exploring Serverless Framework

Serverless Framework helps you develop and deploy AWS Lambda functions, along with the AWS infrastructure resources.

It is different from other frameworks because:

- It manages code as well as infrastructure
- It supports multiple languages (Node.js, Python, Java, and more)

### Serverless Core Concepts

- **Functions:** It's an independent unit of deployment. Example: AWS Lambda, Google Cloud Function
- **Events:** Anything that triggers a Lambda Function to execute is an Event. Example: HTTP, SNS topic, CloudWatch
- **Resources:** Resources are AWS infrastructure components which a Functions use. Example: Dynamodb, SNS, S3
- **Services:** It's where you define your Functions, the Events that trigger them, and the Resources your Functions use. Example: serverless.yml
- **Plugins:** You can overwrite or extend the functionality of the Framework using Plugins. Example: dynamodb-local, Serverless-offline

## Building serverless REST API with Python

You can create a service (aws lambda function) using serverless python 3 template. Here is the command:
`$ serverless create --template aws-python3 --name preprocess --path preprocess`
Or
`$ sls create -t aws-python3 -p preprocess`

It will create a Serverless Python 3 project at the given path (`preprocess/`) with a service name of `preprocess`.

You should have a folder with two files. The main **config** file `serverless.yml` and `handler.py` file with contain serverless function `hello`.

`$ cd preprocess & tree .`

```
.
├── handler.py
└── serverless.yml

0 directories, 2 files
```

Now create a virtual environment for developing locally.

```
$ virtualenv venv --python=python3
$ source venv/bin/activate
(venv) $
```

Let's set up the function contents of `handler.py` so that it contains the following code:

```
import json
import string

translator =  str.maketrans("", "", string.punctuation)

def  process(event,  context):
    """
	Makes text lower case, strips spaces, and removes punctuation.
	"""
	body = json.loads(event['body'])
	text = body['text']
	text = text.lower().strip().replace("\n", " ").translate(translator)

	response = {
		"statusCode":  200,
		"body": json.dumps(text)
	}

	return response
```

> The `process` function makes text lower case, strips spaces, and removes punctuation.

Now your `process` function is linked with the `handler`. However, there is no way of triggering that function.

Let's add an `event` to the function defined in `serverless.yml` so that we can invoke it. Update it as follows:

```
service: preprocess

provider:
	name: aws
	runtime: python3.7

functions:
	process:
		handler: handler.process
		events:
			- http:
				path: preprocess
				method: post
```

Finally, you can deploy the function using `sls deploy`:

```
$ sls deploy
Serverless: Packaging service...
Serverless: Excluding development dependencies...
Serverless: Uploading CloudFormation file to S3...
Serverless: Uploading artifacts...
Serverless: Uploading service preprocess.zip file to S3 (400 B)...
Serverless: Validating template...
Serverless: Updating Stack...
Serverless: Checking Stack update progress...
..............
Serverless: Stack update finished...
Service Information
service: preprocess
stage: dev
region: us-east-1
stack: preprocess-dev
resources: 10
api keys:
  None
endpoints:
  POST - https://xxxxxx.execute-api.us-east-1.amazonaws.com/dev/preprocess
functions:
  process: preprocess-dev-process
layers:
  None
Serverless Enterprise: Run `serverless login` and deploy again to explore, monitor, secure your serverless project for free.
```

You can grab the endpoint listed in the output, which should be a link like:
`POST - https://xxxxxx.execute-api.us-east-1.amazonaws.com/dev/preprocess`

If you want to know information about the service just run `sls info` to log out endpoints, functions, and more info.

```
$ sls info
Service Information
service: preprocess
stage: dev
region: us-east-1
stack: preprocess-dev
resources: 10
api keys:
  None
endpoints:
  POST - https://xxxxxx.execute-api.us-east-1.amazonaws.com/dev/preprocess
functions:
  process: preprocess-dev-process
layers:
  None
```

Let's hit the service by invoking `CURL` command:

```
curl -H 'Content-Type: application/json' -d '{ "text":"Some\nMore\nText':' some more text"}' https://xxxxxx.execute-api.us-east-1.amazonaws.com/dev/preprocess
```

Output:
`some more text some more text`

## CircleCI config

```
version:  2
jobs:
	build:
		working_directory:  ~/preprocess

		docker:
			- image:  circleci/python:3.7

		steps:
			- checkout

			- restore_cache:
				keys:
					- dependencies-node-{{ checksum "package.json" }}
					- dependencies-node

			- run:
				name:  Install node and npm
				command:  |
					curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
					sudo apt-get install -y nodejs
					node --version && npm -v

			- run:
				name:  Install Serverless CLI and dependencies
				command:  |
					sudo npm i -g serverless
					npm install

			- save_cache:
				paths:
					- node_modules
				key:  dependencies-node-{{ checksum "package.json" }}

			- run:
				name:  Deploy application
				command:  sls deploy -v
```

## Logging and Monitoring

`CloudWatch` provide basic functionality for logging, monitoring and alerts.

Howeverm, there are some great third party tools that can help centralized Logging, monitoring and alert for AWS Lambda. Here are some of them:

- [Dashbird](https://dashbird.io)
- [IOpipe](https://www.iopipe.com/)
- [DATADOG](https://www.datadoghq.com/)
- [Epsagon](https://epsagon.com/)
