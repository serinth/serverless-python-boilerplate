import os
from auth.utils import verify_and_get_claims, generate_lambda_invoke_policy, get_known_keys
from auth.constants import CUSTOM_GROUP

region = os.getenv('REGION')
userpool_id = os.getenv('USER_POOL_ID') #'ap-southeast-2_xxxxxxxxx'
app_client_id = os.getenv('APP_CLIENT_ID')
keys = get_known_keys(region, userpool_id)

def main(event, context):
    claims = verify_and_get_claims(event, keys, app_client_id)
    
    if type(claims) is bool and claims is False:
        raise Exception("Unauthorized")

    if CUSTOM_GROUP in claims["cognito:groups"]:
        return generate_lambda_invoke_policy(claims['sub'], "Allow", event['methodArn'])
    
    raise Exception('Unauthorized')    

if __name__ == '__main__':
    event = {'token': ''}
    main(event, None)
