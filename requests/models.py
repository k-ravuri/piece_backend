from django.db import models
from django.db import connection
import psycopg2
import pprint
from django.http import HttpResponseRedirect

class Request(models.Model):
    restaurant_email = models.CharField(max_length = 100)
    nonprofit_email = models.CharField(max_length = 100)
    nonprofit_name = models.CharField(max_length = 100)
    dish =models.CharField(max_length = 100)
    servings = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
    def getRestaurantEmail(self):
        return self.restaurant_email
    def getNonProfitEmail(self):
        return self.nonprofit_email
    def getName(self):
        return self.name
    def getPrice(self):
        return self.address

    def setRestaurantEmail(restaurant_email):
         self.restaurant_email = restaurant_email
    def setRestaurantEmail(nonprofit_email):
        self.nonprofit_email = nonprofit_email    
    def setName(name):
         self.name = name
    def setPrice(price):
         self.price = price
