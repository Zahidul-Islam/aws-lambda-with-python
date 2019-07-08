# Steps

- Create a new directory with a package.json file:

```
$ mkdir serverless-flask && cd serverless-flask
$ npm init -y
```

- Install `serverless-wsgi` and `serverless-python-requirements` plugin

`$ npm install --save-dev serverless-wsgi serverless-python-requirements`

- Create `app.py` with the following contents:

```
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
```

- Create a `serverless.yml` in the working directory:

```
service: serverless-flask

plugins:
  - serverless-python-requirements
  - serverless-wsgi

custom:
  wsgi:
    app: app.app
    packRequirements: false
  pythonRequirements:
    dockerizePip: non-linux
    slim: true

provider:
  name: aws
  runtime: python3.6
  stage: dev
  region: us-east-1

functions:
  app:
    handler: wsgi.handler
    events:
      - http: ANY /
      - http: 'ANY {proxy+}'

```

- create a virtual environment and activate it

```
$ virtualenv venv --python=python3
$ source venv/bin/activate
```

- Install the Flask package with pip, and save your dependencies in requirements.txt:

```
(venv) $ pip install flask
(venv) $ pip freeze > requirements.txt
```

- Deploy the function `$ sls deploy`

- Run locally `sls wsgi serve`
