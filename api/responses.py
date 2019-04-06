import json
from http import HTTPStatus

cors_headers = { 
    'Access-Control-Allow-Origin': '*',
    'Content-Type': 'application/json',
}

def generate_empty_response(status_code):
    return {
        'headers': cors_headers,
        'statusCode': status_code
    } 

def generate_response(body, status_code):
    response = generate_empty_response(status_code)
    response['body'] = json.dumps(body)
    return response

def generate_message_response(message, status_code):
    return generate_response({'message': message}, status_code)

def generate_error_response(err, status_code):
    return generate_response({'error': str(err)}, status_code)

def invalid_request_response(message='Invalid Request'):
    return generate_error_response(message, HTTPStatus.BAD_REQUEST.value)

def ok_response(body=None):
    if body is None:
        return generate_empty_response(HTTPStatus.OK.value)
    return generate_response(body, HTTPStatus.OK.value)

def internal_error_response(err):
    return generate_error_response(err, HTTPStatus.INTERNAL_SERVER_ERROR.value)

def unauthorized_response():
    return generate_message_response('Unauthorized', HTTPStatus.UNAUTHORIZED.value)

def not_found_response():
    return generate_message_response('Not Found', HTTPStatus.NOT_FOUND.value)