from api.responses import generate_error_response, ok_response, generate_response
from http import HTTPStatus
from logs.logging import get_logger
import boto3

log = get_logger('socket_manager_logger')

CONNECT = 'CONNECT'
DISCONNECT = 'DISCONNECT'

def connection_manager(event, context):
    connection_id = event["requestContext"].get("connectionId")
    
    if event["requestContext"]["eventType"] == CONNECT:
        log.info(f'Connect requested with id: {connection_id}')
        return ok_response()
        
    elif event["requestContext"]["eventType"] == DISCONNECT:
        log.info(f'Disconnect requested from {connection_id}')
        return ok_response()
    else:
        log.error(f'Connection manager received unrecognized eventType: {event}')
        return generate_error_response("unrecognized socket action", HTTPStatus.BAD_REQUEST)

def default_message(event, context):
    return generate_error_response("unrecognized socket action", HTTPStatus.BAD_REQUEST)

def echo(event, context):
    connection_id = event["requestContext"].get("connectionId")
    client = boto3.client("apigatewaymanagementapi", endpoint_url = "https://" +
        event["requestContext"]["domainName"] +
        "/" + 
        event["requestContext"]["stage"])
    
    data = json.loads(event.get('body'))
    client.post_to_connection(ConnectionId=connection_id, Data=json.dumps(data).encode('utf-8'))
    return generate_response('done'), HTTPStatus.OK)

if __name__ == '__main__':
    connection_manager(None, None)