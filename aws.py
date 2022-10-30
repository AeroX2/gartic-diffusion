import os
import boto3
from pathlib import Path
from datetime import datetime, timedelta

aws_folder = Path.home() / '.aws'
cred_file = aws_folder / 'credentials'
if (not cred_file.exists()):
    print("AWS credential file not found, boto3 will probably fail")
    print("Visit https://us-east-1.console.aws.amazon.com/iam/home, to make one")
    print("Access Key ID: ", end='')
    access_key_id = input()
    print("Secret access key: ", end='')
    secret_access_key_id = input()
    os.mkdir(aws_folder)
    f = open(cred_file, 'w')
    f.write("[default]\naws_access_key_id = {}\naws_secret_access_key = {}".format(access_key_id, secret_access_key_id))
    f.close()

ec2 = boto3.client('ec2', region_name='ap-southeast-2')

key_name = 'gartic-diffusion-key'
response = ec2.describe_key_pairs()
if (key_name not in map(lambda x: x['KeyName'], response['KeyPairs'])):
    print("Key not found")
    print(f"Creating key pair: {key_name}")
    ec2.create_key_pair(KeyName=key_name)

response = ec2.run_instances(
    DryRun=False,
    ImageId='ami-09f032942a8d96feb',
    InstanceType='inf1.xlarge',
    KeyName='gartic-diffusion-key',
    MaxCount=1,
    MinCount=1,
    InstanceInitiatedShutdownBehavior='terminate',
)
print(response)