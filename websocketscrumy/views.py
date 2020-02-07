from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Connection, ChatMessage
import boto3

# Create your views here.



@csrf_exempt
def test(request):
    return JsonResponse({'message': 'hello Daud'}, status=200)


def  _parse_body(body):
    body_unicode = body.decode('utf-8')
    return json.loads(body_unicode)


@csrf_exempt
def connect(request):
    body = _parse_body(request.body)
    connection_id = body['connectionId']
    connect = Connection(connection_id=connection_id)
    connect.save()
    return JsonResponse({'message': 'connect successfully'}, status=200)

def disconnect(request):
    body = _parse_body(request.body)
    #remove from database
    connection_id = body['connectionId']
    # connect = Connection.objects.get(connection_id=connection_id)
    return JsonResponse({'message': 'disconnect successfully'}, status=200)

@csrf_exempt
def send_message(request):
    body = _parse_body(request.body)
    body = dict(body)
    username = body['body']['username']
    message = body['body']['message']
    timestamp = body['body']['timestamp']
    savemessage = ChatMessage(username=username, messages=message, timestamp=timestamp)
    savemessage.save()
    connections = Connection.objects.all()
    data = {'messages': [body]}
    for eachconnect in connections:
        _send_to_connection(str(eachconnect), data)
    return JsonResponse({'message': 'successfully send'}, status=200)



def _send_to_connection(connection_id, data):
    gatewayapi = boto3.client('apigatewaymanagementapi', endpoint_url='https://0l90clyplf.execute-api.us-east-2.amazonaws.com/test/@connections',
                              region_name='us-east-2', aws_access_key_id='AKIAJIIZQFWJ7DM4IZGA', aws_secret_access_key='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')
    response = gatewayapi.post_to_connection(ConnectionId=connection_id, Data=json.dumps(data).encode('utf-8'))
    return response


@csrf_exempt
def getRecentMessages(request):
    print("test - ",request.body)
    body = _parse_body(request.body)
    print("lieer - ",body)
    connection_id = body['connectionId']
    allmessage = ChatMessage.objects.filter()
    result_list = list(allmessage.values('username', 'messages', 'timestamp'))
    result_list.reverse()
    data = {'messages': [result_list]}
    _send_to_connection(connection_id, json.loads(data))
    return JsonResponse({'message': data}, status=200)

