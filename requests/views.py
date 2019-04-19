from django.shortcuts import render
from restaurants.models import Restaurant
from restaurants.serializers import RestaurantSerializer
from rest_framework import generics
from rest_framework.decorators import detail_route, list_route, api_view
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import psycopg2
import pprint
import json
import datetime
from django.http import Http404
from django.shortcuts import render

@csrf_exempt 
@api_view(['GET', 'POST', 'DELETE']) 
def requests(request, format=None):
    if request.method == 'POST': #register nonprofit
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        cursor = connection.cursor()
        cursor.execute('INSERT INTO requests_request ("restaurant_email", "nonprofit_email",  "nonprofit_name", "dish", "servings") VALUES( %s, %s, %s, %s, %s)' , [ body["restaurant_email"],  body["nonprofit_email"], body["nonprofit_name"], body["dish"], body["servings"] ])
        
        return JsonResponse({
            'message': "SUCCESS"
        })
    elif request.method == 'DELETE': #delete a dish by name and restaurant email
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        cursor = connection.cursor()
        cursor.execute("DELETE FROM requests_request WHERE dish = %s AND restaurant_email = %s AND nonprofit_email = %s ", [body["dish"], body["restaurant_email"], body["nonprofit_email"]])
        
        return JsonResponse({
            'message': "SUCCESS"
        })
    else: #get a dish based off of restaurant email
        restaurant_email = request.GET.get('restaurant_email', '')

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM requests_request WHERE restaurant_email = %s", [restaurant_email])
        requests = cursor.fetchall()

        if len(requests) == 0:
            return JsonResponse({
                'message': "NOT FOUND",
                'result': None
            })
        else:
            return JsonResponse({
                'message': "SUCCESS",
                'result': requests
            })
