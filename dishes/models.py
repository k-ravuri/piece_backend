from django.db import models
from django.db import connection
import psycopg2
import pprint
from django.http import HttpResponseRedirect

class Dish(models.Model):
    restaurant_email = models.CharField(max_length = 100)
    restaurant_name = models.CharField(max_length = 100)
    name = models.CharField(max_length = 100)
    price = models.IntegerField(default=0)
    servings = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
    def getRestaurantEmail(self):
        return self.restaurant_email
    def getName(self):
        return self.name
    def getPrice(self):
        return self.address

    def setRestaurantEmail(restaurant_email):
         self.restaurant_email = restaurant_email
    def setName(name):
         self.name = name
    def setPrice(price):
         self.price = price


def get_dishes(restuarant_email, restuarant_name):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM dishes WHERE restuarant_email = %s AND restuarant_name = %s", [restuarant_email, restuarant_name])
    row = cursor.fetchall()
    pprint.pprint(row)
    return row

def register_dish(restuarant_email,restuarant_name,name,price,listTime):
    cursor = connection.cursor()
    cursor.execute('INSERT INTO dishes ("restaurant_email", "restaurant_name", "name", "price", "listing_time") VALUES(%s, %s, %s, %s, %s) ', [restuarant_email, restuarant_name, name, price, listTime])
    # row = cursor.fetchall()
    # pprint.pprint(row)
    return [restuarant_email, restuarant_name, name, price, listTime]

def delete_dish(name, restuarant_email):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM dishes WHERE name = %s AND restuarant_email = %s", [name, restuarant_email])
    return "success"