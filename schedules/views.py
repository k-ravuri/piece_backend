from django.shortcuts import render
from restaurants.models import Restaurant
from restaurants.serializers import RestaurantSerializer
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
@api_view(['GET', 'POST', 'DELETE', 'PUT']) 
def schedules(request, format=None):
    if request.method == 'POST': #register schedule
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO schedules_schedule ("email", "mondaystart", "mondayend", "tuesdaystart", "tuesdayend" , "wednesdaystart" , "wednesdayend" , "thursdaystart" , "thursdayend" , "fridaystart" , "fridayend" , "saturdaystart" , "saturdayend" , "sundaystart" , "sundayend") VALUES(%s, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d)' , 
            [ body["email"], body["mondaystart"], body["mondayend"], body["tuesdaystart"], body["tuesdayend"] , body["wednesdaystart"] , body["wednesdayend"] , body["thursdaystart"] , body["thursdayend"] , body["fridaystart"] , body["fridayend"], body["saturdaystart"] , body["saturdayend"] , body["sundaystart"] , body["sundayend"] ] )
        return JsonResponse({
            'message': "SUCCESS"
        })
    elif request.method == 'DELETE': #unregister restaurant
        email = request.GET.get('email', '')
        cursor = connection.cursor()
        cursor.execute("DELETE FROM schedules_schedule WHERE email = %s", [email])
        return JsonResponse({
            'message': "SUCCESS"
        })
    elif request.method == 'PUT':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        cursor = connection.cursor()
        cursor.execute('UPDATE schedules_schedule SET email = %s, mondaystart = %s, mondayend = %s, tuesdaystart = %s, tuesdayend = %s, wednesdaystart = %s, wednesdayend = %s, thursdaystart = %s, thursdayend = %s, fridaystart = %s, fridayend = %s, saturdaystart = %s, saturdayend = %s, sundaystart = %s,  sundayend= %s', [ body["email"], body["mondaystart"], body["mondayend"], body["tuesdaystart"], body["tuesdayend"] , body["wednesdaystart"] , body["wednesdayend"] , body["thursdaystart"] , body["thursdayend"] , body["fridaystart"] , body["fridayend"], body["saturdaystart"] , body["saturdayend"] , body["sundaystart"] , body["sundayend"]])
        return JsonResponse({
            'message': "SUCCESS"
        })
    else:
        email = request.GET.get('email', '') 
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM schedules_schedule WHERE email = %s', [email] )
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

@csrf_exempt 
@api_view(['POST']) 
def create_schedule_by_email(request, format=None):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    cursor = connection.cursor()
    cursor.execute('INSERT INTO schedules_Schedule ("email") VALUES(%s)' , 
        [ body["email"] ] )
    return JsonResponse({
        'message': "SUCCESS"
    })

@api_view(['GET']) #getting restaurant data by email
def get_data_by_email(request): 
    email = request.GET.get('email', '')
    print(email)
    cursor = connection.cursor()
    cursor.execute("SELECT *  FROM schedules_schedule WHERE email = %s", [email])
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

@api_view(['PUT']) #replace time
def change_mondaystart(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    email = body["email"]
    newtime = body["newtime"]
    cursor = connection.cursor()
    cursor.execute("UPDATE schedules_schedule SET mondaystart = %s WHERE email = %s", [newtime, email])

    return JsonResponse({
        'message': "SUCCESS"
    })

@api_view(['PUT']) #replace time
def change_mondaystart(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    email = body["email"]
    newtime = body["newtime"]
    cursor = connection.cursor()
    cursor.execute("UPDATE schedules_schedule SET mondaystart = %s WHERE email = %s", [newtime, email])

    return JsonResponse({
        'message': "SUCCESS"
    })

@api_view(['PUT']) #replace time
def change_mondayend(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    email = body["email"]
    newtime = body["newtime"]
    cursor = connection.cursor()
    cursor.execute("UPDATE schedules_schedule SET mondayend = %s WHERE email = %s", [newtime, email])

    return JsonResponse({
        'message': "SUCCESS"
    })

@api_view(['PUT']) #replace time
def change_tuesdaystart(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    email = body["email"]
    newtime = body["newtime"]
    cursor = connection.cursor()
    cursor.execute("UPDATE schedules_schedule SET tuesdaystart = %s WHERE email = %s", [newtime, email])

    return JsonResponse({
        'message': "SUCCESS"
    })

@api_view(['PUT']) #replace time
def change_tuesdayend(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    email = body["email"]
    newtime = body["newtime"]
    cursor = connection.cursor()
    cursor.execute("UPDATE schedules_schedule SET tuesdayend = %s WHERE email = %s", [newtime, email])

    return JsonResponse({
        'message': "SUCCESS"
    })

@api_view(['PUT']) #replace time
def change_wednesdaystart(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    email = body["email"]
    newtime = body["newtime"]
    cursor = connection.cursor()
    cursor.execute("UPDATE schedules_schedule SET wednesdaystart = %s WHERE email = %s", [newtime, email])

    return JsonResponse({
        'message': "SUCCESS"
    })

@api_view(['PUT']) #replace time
def change_wednesdayend(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    email = body["email"]
    newtime = body["newtime"]
    cursor = connection.cursor()
    cursor.execute("UPDATE schedules_schedule SET wednesdayend = %s WHERE email = %s", [newtime, email])

    return JsonResponse({
        'message': "SUCCESS"
    })

@api_view(['PUT']) #replace time
def change_thursdaystart(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    email = body["email"]
    newtime = body["newtime"]
    cursor = connection.cursor()
    cursor.execute("UPDATE schedules_schedule SET thursdaystart = %s WHERE email = %s", [newtime, email])

    return JsonResponse({
        'message': "SUCCESS"
    })

@api_view(['PUT']) #replace time
def change_thursdayend(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    email = body["email"]
    newtime = body["newtime"]
    cursor = connection.cursor()
    cursor.execute("UPDATE schedules_schedule SET thursdayend = %s WHERE email = %s", [newtime, email])

    return JsonResponse({
        'message': "SUCCESS"
    })

@api_view(['PUT']) #replace time
def change_fridaystart(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    email = body["email"]
    newtime = body["newtime"]
    cursor = connection.cursor()
    cursor.execute("UPDATE schedules_schedule SET fridaystart = %s WHERE email = %s", [newtime, email])

    return JsonResponse({
        'message': "SUCCESS"
    })

@api_view(['PUT']) #replace time
def change_fridayend(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    email = body["email"]
    newtime = body["newtime"]
    cursor = connection.cursor()
    cursor.execute("UPDATE schedules_schedule SET fridayend = %s WHERE email = %s", [newtime, email])

    return JsonResponse({
        'message': "SUCCESS"
    })

@api_view(['PUT']) #replace time
def change_saturdaystart(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    email = body["email"]
    newtime = body["newtime"]
    cursor = connection.cursor()
    cursor.execute("UPDATE schedules_schedule SET saturdaystart = %s WHERE email = %s", [newtime, email])

    return JsonResponse({
        'message': "SUCCESS"
    })

@api_view(['PUT']) #replace time
def change_saturdayend(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    email = body["email"]
    newtime = body["newtime"]
    cursor = connection.cursor()
    cursor.execute("UPDATE schedules_schedule SET saturdayend = %s WHERE email = %s", [newtime, email])

    return JsonResponse({
        'message': "SUCCESS"
    })

@api_view(['PUT']) #replace time
def change_sundaystart(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    email = body["email"]
    newtime = body["newtime"]
    cursor = connection.cursor()
    cursor.execute("UPDATE schedules_schedule SET sundaystart = %s WHERE email = %s", [newtime, email])

    return JsonResponse({
        'message': "SUCCESS"
    })

@api_view(['PUT']) #replace time
def change_sundayend(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    email = body["email"]
    newtime = body["newtime"]
    cursor = connection.cursor()
    cursor.execute("UPDATE schedules_schedule SET sundayend = %s WHERE email = %s", [newtime, email])

    return JsonResponse({
        'message': "SUCCESS"
    })