from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Connection, ChatMessage
import boto3
from django.conf import settings
import requests
import os
# Create your views here.

boto3.set_stream_logger('')

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



@csrf_exempt
def disconnect(request):
    body = _parse_body(request.body)
    #remove from database
    connection_id = body['connectionId']
    connect = Connection.objects.filter(connection_id=connection_id).delete()
    return JsonResponse({'message': 'disconnect successfully'}, status=200)

@csrf_exempt
def send_message(request):
    body = _parse_body(request.body)
    newbody = dict(body)
    username = newbody['body']['username']
    message = newbody['body']['message']
    timestamp = newbody['body']['timestamp']
    savemessage = ChatMessage(username=username, messages=message, timestamp=timestamp)
    savemessage.save()
    messages = {
        "username":username,
        "message":message,
        "timestamp":timestamp
    }
    connections = Connection.objects.filter()
    allconnect = list(connections.values('connection_id'))
    data = {'messages': [list(messages)]}
    for eachconnect in allconnect:
        conn = eachconnect['connection_id']
        _send_to_connection(str(conn), data)
    return JsonResponse({'message': 'successfully send'}, status=200)


@csrf_exempt
def _send_to_connection(connection_id, data):
    gatewayapi = boto3.client('apigatewaymanagementapi', region_name='us-east-2', endpoint_url='https://0l90clyplf.execute-api.us-east-2.amazonaws.com/test/',
                              aws_access_key_id=os.getenv('ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('SECRET_KEY'), aws_session_token=os.getenv('SESSION_TOKEN'))
    return gatewayapi.post_to_connection(ConnectionId=connection_id, Data=json.dumps(data).encode('utf-8'))


@csrf_exempt
def getRecentMessages(request):
    body = _parse_body(request.body)
    connection_id = body['connectionId']
    allmessage = ChatMessage.objects.filter()
    result_list = list(allmessage.values('username', 'messages', 'timestamp'))
    data = {'messages': []}
    _send_to_connection(str(connection_id), data)
    return JsonResponse({'message': json.dumps(data)}, status=200)

