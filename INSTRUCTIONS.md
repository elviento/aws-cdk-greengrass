# Getting Started Instructions

## Clone this repo

```
git clone git@github.com:elviento/aws-cdk-mygreengrass.git
```

## Install CDK using NPM

```
npm install -g aws-cdk
```

## Setup Python Virtual Environment

*Follow steps in [README](./README.md) and [CDK Getting Started](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html)*

```
python -m venv .env
source .env/bin/activate
```

## Code using your IDE 

* I'm currently using [VSCodium](https://vscodium.com/)

## Run CDK Commands to Deploy to your AWS Acct

```
cdk synth
cdk deploy
```

*You should now have an IoT Thing along with an attached Device Certificate and Policy!!*

## Run into trouble?  Try this AWS CDK/Python Blog Article

[AWS Developer Blog - CDK/Python](https://aws.amazon.com/blogs/developer/getting-started-with-the-aws-cloud-development-kit-and-python/)
