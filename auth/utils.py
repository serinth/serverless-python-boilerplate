# Copyright 2017-2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file
# except in compliance with the License. A copy of the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is distributed on an "AS IS"
# BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under the License.

# Modified by Tony Truong
# - parse the correct event key
# - added constant time string comparison to protect against timing attacks
# - corrected token location in header
# - corrected urllib import for python 3


import time
import urllib.request as request
import json
from jose import jwk, jwt
from jose.utils import base64url_decode
from hmac import compare_digest


def get_known_keys(region, userpool_id):
    keys_url = f'https://cognito-idp.{region}.amazonaws.com/{userpool_id}/.well-known/jwks.json'
    response = request.urlopen(keys_url)
    return json.loads(response.read())['keys']


def verify_and_get_claims(event, keys, app_client_id):
    token = event['authorizationToken'].split(' ')[1]
    # get the kid from the headers prior to verification
    headers = jwt.get_unverified_headers(token)
    kid = headers['kid']
    # search for the kid in the downloaded public keys
    key_index = -1
    for i in range(len(keys)):
        if kid == keys[i]['kid']:
            key_index = i
            break
    if key_index == -1:
        print('Public key not found in jwks.json')
        return False
    # construct the public key
    public_key = jwk.construct(keys[key_index])
    # get the last two sections of the token,
    # message and signature (encoded in base64)
    message, encoded_signature = str(token).rsplit('.', 1)
    # decode the signature
    decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))
    # verify the signature
    if not public_key.verify(message.encode("utf8"), decoded_signature):
        print('Signature verification failed')
        return False
    print('Signature successfully verified')
    # since we passed the verification, we can now safely
    # use the unverified claims
    claims = jwt.get_unverified_claims(token)
    
    # verify expiration of token
    if time.time() > claims['exp']:
        print('Token is expired')
        return False

    if not compare_digest(claims['client_id'], app_client_id):
        print('Token was not issued for this audience')
        return False

    return claims


# https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
def get_sub(awsRequestEvent: dict):
     return awsRequestEvent.get('requestContext').get('authorizer').get('principalId')


def generate_lambda_invoke_policy(principal_id, effect, resource):
    # TODO: set principal to the preferred_username and update cognito pool, for the pilot we will specifically allow the /gps folder
    return {
        'principalId': principal_id,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": resource
                }
            ]
        }
    }
