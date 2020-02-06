from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Connection, ChatMessage

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
    #remember to save it using the connectionmodel task 28
    connection_id = body['connectionId']
    connect = Connection(connection_id=connection_id)
    connect.save()
    return JsonResponse({'message': 'connect successfully'}, status=200)

def disconnect(request):
    body = _parse_body(request.body)
    #remove from database
    connection_id = body['connectionId']
    connect = Connection.objects.get(connection_id=connection_id)
    return JsonResponse({'message': 'disconnect successfully'}, status=200)