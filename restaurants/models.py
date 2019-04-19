from django.db import models
from django.db import connection
import psycopg2
import pprint
from django.http import HttpResponseRedirect

# Create your models here
class Restaurant(models.Model):
    email = models.CharField(max_length = 100, primary_key=True)
    password = models.CharField(max_length = 100)
    name = models.CharField(max_length = 100)
    address = models.CharField(max_length = 100)
    city = models.CharField(max_length = 100)
    state = models.CharField(max_length = 100)
    zip_code = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    phone_number = models.IntegerField(default=0)
    # yelp_url = models.CharField(max_length = 100)
    

    def __str__(self):
        return self.name
    def getEmail(self):
        return self.email
    def getName(self):
        return self.name
    def getAddress(self):
        return self.address
    def getPhoneNumber(self):
        return self.phone_number

    def setEmail(email):
         self.email = email
    def setName(name):
         self.name = name
    def setAddress(address, state, city, zip_code):
         self.address = address
         self.state = state
         self.city = city
         self.zip_code = zip_code
    def setPhoneNumber(phone_number):
         self.phone_number = phone_number
