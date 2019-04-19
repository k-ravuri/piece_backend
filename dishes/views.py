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
from  .models import  get_dishes, register_dish, delete_dish

@csrf_exempt 
@api_view(['GET', 'POST', 'DELETE']) 
def dishes(request, format=None):
    if request.method == 'POST': #register nonprofit
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        cursor = connection.cursor()
        cursor.execute('INSERT INTO dishes_dish ("restaurant_email", "restaurant_name", "name", "price", "servings") VALUES( %s, %s, %s, %s, %s)' , [ body["restaurant_email"],  body["restaurant_name"], body["name"], body["price"], body["servings"] ])
        
        return JsonResponse({
            'message': "SUCCESS"
        })
    elif request.method == 'DELETE': #delete a dish by name and restaurant email
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        cursor = connection.cursor()
        cursor.execute("DELETE FROM dishes_dish WHERE name = %s AND restaurant_email = %s", [body["name"], body["restaurant_email"]])
        
        return JsonResponse({
            'message': "SUCCESS"
        })
    else: #get a dish based off of restaurant email
        restaurant_email = request.GET.get('restaurant_email', '')

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM dishes_dish WHERE restaurant_email = %s", [restaurant_email])
        dish = cursor.fetchall()

        if len(dish) == 0:
            return JsonResponse({
                'message': "NOT FOUND",
                'result': None
            })
        else:
            return JsonResponse({
                'message': "SUCCESS",
                'result': dish
            })


@api_view(['GET']) 
def dishes_price(request, format=None):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    return get_price(body["time"], body["price"])

@api_view(['GET']) 
def dishes_rec_price(request, format=None):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    return make_model(body["price"], body["zipcode"], body["servings"])

def make_model(price, zipcode, servings):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM dishes NATURAL JOIN (SELECT name, phone_number, address, city, state, zip_code FROM restaurants WHERE restaurants.zip_code = %s) AS r ", [zipcode])

    # ON dishes.restaurant_email = r.email
    listings = cursor.fetchall()

    serving_mu=0
    serving_mu_squared=0
    price_mu=0
    price_serving_mu=0
    num=0

    for listing in listings:
        price_mu+= listing['price']
        serving_mu+= listing['servings']
        serving_mu_squared += listing['servings'] * listing['servings']
        price_serving_mu += listing['price'] * listing['servings']
        num += 1

    if(num == 0 | price_mu ==0 | serving_mu == 0):
        return JsonResponse({
                'message': "INSUFFCIENT DATA",
                'result': None
            })
    m = ((num*price_serving_mu)-(price_mu*serving_mu))/((num * serving_mu_squared)- (serving_mu*serving_mu))
    b = ((serving_mu_squared*price_mu) - (price_mu * serving_mu))/((num*serving_mu_squared)-(serving_mu*serving_mu))

    return JsonResponse(str((serving*m)+b), safe=False)


def get_price(time, price):
    # print(request)
    e = time
    p = price
    currPrice = float('0' + p)
    print(e.split(':'))
    split = e.split(':')
    hour = int('0' + datetime.datetime.now().strftime('%H')) * 60  #  Time like '23:12:05'
    minute = int('0' + datetime.datetime.now().strftime('%M'))  #  Time like '23:12:05'
    total_min = hour + minute
    given_hour = int('0' + split[0]) * 60
    print(split[0])
    given_min = int('0' + split[1])
    print(split[1])
    decrement = ((total_min - (given_hour+given_min))/60) * (currPrice*.05)
    if((decrement > 0) | (currPrice < decrement)):
        return JsonResponse({
                'message': "DELETE ITEM",
                'result': None
            })

    print(decrement)
    currPrice += decrement

    return JsonResponse(str(currPrice), safe=False)
