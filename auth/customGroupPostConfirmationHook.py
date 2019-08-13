import boto3
import json
from os import getenv
from auth.constants import CUSTOM_GROUP

REGION = getenv('REGION', 'ap-southeast-2')

def main(event, context):
    pool_id = event.get('userPoolId')
    username = event.get('username')
    req = json.loads(event['request'])
    attr = req.get('userAttributes')
    sub = attr.get('sub')
    
    session = boto3.Session()
    client = boto3.client('cognito-idp', region_name=REGION)

    if None in (pool_id, username, sub):
        raise ValueError('could not parse pool, username or sub')

    try:
        response = client.admin_add_user_to_group(UserPoolId=pool_id, Username=username, GroupName=CUSTOM_GROUP)
    except Exception:
        raise ValueError(f'Failed to add {username} to {CUSTOM_GROUP}')


if __name__ == '__main__':
    main('','')