import sys
import boto3, botostubs
from botocore.exceptions import ClientError
import json
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


client: botostubs.IoT = boto3.client('iot') # type: botostubs.IOT

# iot thing greengrass core
policyDocument = {
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "iot:Publish",
        "iot:Subscribe",
        "iot:Connect",
        "iot:Receive"
      ],
      "Resource": [
        "*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "iot:GetThingShadow",
        "iot:UpdateThingShadow",
        "iot:DeleteThingShadow"
      ],
      "Resource": [
        "*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "greengrass:*"
      ],
      "Resource": [
        "*"
      ]
    }
  ]
}


# create csr for device certificates
def create_csr(): # ugh! - would like to avoid this but will require a custom resource
    response = client.create_keys_and_certificate(
        setAsActive=True
    )

    # save device certificates
    # write to file and upload to s3 for retrieval

    return response['certificateArn']