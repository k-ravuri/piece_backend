from django.shortcuts import render
from restaurants.models import Restaurant
from restaurants.serializers import RestaurantSerializer
from restaurants.yelp_webcrawler import restaurant_info_scraper, multithread_functions
from rest_framework import generics
from rest_framework.decorators import detail_route, list_route, api_view
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import psycopg2
import pprint
import json
import datetime
from django.http import Http404
from django.shortcuts import render

@csrf_exempt 
@api_view(['GET', 'POST', 'DELETE']) 
def restaurants(request, format=None):
    if request.method == 'POST': #register restaurant
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        cursor = connection.cursor()
        cursor.execute('INSERT INTO restaurants_restaurant ("email", "password", "name", "address", "phone_number", "zip_code", "rating", "city", "state") VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s)' , [ body["email"],  body["password"], body["name"], body["address"], body["phone"], body["zip_code"], 0, body["city"], body["state"] ])
        
        return JsonResponse({
            'message': "SUCCESS",
        })
    elif request.method == 'DELETE': #unregister restaurant
        email = request.GET.get('email', '')
        cursor = connection.cursor()
        cursor.execute("DELETE FROM restaurants_restaurant WHERE email = %s", [email])

        return JsonResponse({
            'message': "SUCCESS"
        })
    else:
        email = request.GET.get('email', '') 
        password = request.GET.get('password', '')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM restaurants_restaurant WHERE email = %s AND password = %s', [email, password] )
        restaurant = cursor.fetchall()

        if len(restaurant) == 0:
            return JsonResponse({
                'message': "NOT FOUND",
                'result': None
            })
        else:
            return JsonResponse({
                'message': "SUCCESS",
                'result': restaurant
            })

# @csrf_exempt 
# @api_view(['PUT']) #edit restaurant data
# def restaurants(request, format=None):
#     body_unicode = request.body.decode('utf-8')
#     body = json.loads(body_unicode)

#     cursor = connection.cursor()
#     cursor.execute('UPDATE restaurants SET email = %s, password = %s, name = %s, address = %s, phone_number = %s, zip_code = %s, rating = %s, city = %s, state = %s WHERE email = %s', [body["email"], body["password"], body["name"], body["address"], body["phone"], body["zip_code"], str(0), body["city"], body["state"], body["email"]])
    
#     return JsonResponse({
#         'message': "SUCCESS"
#     })

@api_view(['PUT']) #replace password
def change_password(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    email = body["email"]
    new_password = body["newPassword"]
    cursor = connection.cursor()
    cursor.execute("UPDATE restaurants_restaurant SET password = %s WHERE email = %s", [new_password, email])

    return JsonResponse({
        'message': "SUCCESS"
    })

@api_view(['GET']) #getting restaurant data by email
def get_data_by_email(request): 
    email = request.GET.get('email', '')
    print(email)
    cursor = connection.cursor()
    cursor.execute("SELECT name, phone_number, address, city, state, zip_code  FROM restaurants_restaurant WHERE email = %s", [email])
    restaurant_data = cursor.fetchall()

    if len(restaurant_data) == 0:
        return JsonResponse({
            'message': "NOT FOUND",
            'data': None
        })
    else:
        return JsonResponse({
            'message': "SUCCESS",
            'data': restaurant_data
        })
    return JsonResponse(success, safe=False)

@api_view(['GET']) #getting restaurants data by name
def get_data_by_name(request): 
    name = request.GET.get('name', '')

    cursor = connection.cursor()
    cursor.execute("SELECT name, phone_number, address, city, state, zip_code  FROM restaurants_restaurant WHERE name = %s", [name])
    restaurant_data = cursor.fetchall()

    if len(restaurant_data) == 0:
        return JsonResponse({
            'message': "NOT FOUND",
            'data': None
        })
    else:
        return JsonResponse({
            'message': "SUCCESS",
            'data': restaurant_data
        })
    return JsonResponse(success, safe=False)

@api_view(['GET']) #getting restaurants data by name
def get_near_me(request): 
    name = request.GET.get('zipcode', '')

    cursor = connection.cursor()
    cursor.execute("SELECT name, phone_number, address, city, state, zip_code  FROM restaurants WHERE zipcode = %s", [zipcode])
    restaurant_data = cursor.fetchall()

    if len(restaurant_data) == 0:
        return JsonResponse({
            'message': "NOT FOUND",
            'data': None
        })
    else:
        return JsonResponse({
            'message': "SUCCESS",
            'data': restaurant_data
        })
    return JsonResponse(success, safe=False)

@api_view(['GET']) #getting restaurants data by name
def get_restaurant_info(request): 
    restaurant_name = request.GET.get('restaurant_name', '')
    city = request.GET.get('city', '')
    state = request.GET.get('state', '')

    # cursor = connection.cursor()
    # cursor.execute("SELECT name, phone_number, address, city, state, zip_code  FROM restaurants WHERE name = %s", [name])
    # restaurant_data = cursor.fetchall()
    success = multithread_functions(restaurant_name, city, state)
    # print(success)
    # time = get_times(returant_name, city);

    if len(success) == 0:
        return JsonResponse({
            'message': "NOT FOUND",
            'data': None
        })
    else:
        return JsonResponse({
            'message': "SUCCESS",
            'data': success
        })
    return JsonResponse(success, safe=False)
