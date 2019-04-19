from django.db import models
from django.db import connection
import psycopg2
import pprint
from django.http import HttpResponseRedirect

class NonProfit(models.Model):
    email = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100)
    name = models.CharField(max_length = 100)
    address = models.CharField(max_length = 100)
    city = models.CharField(max_length = 100)
    state = models.CharField(max_length = 100)
    zip_code = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    phone_number = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    def getEmail(self):
        return self.email
    def getName(self):
        return self.name
    def getAddress(self):
        return [self.address, self.state, self.city, self.zip_code]
    def getphoneNumber(self):
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
    def setphoneNumber(phone_number):
         self.phone_number = phone_number
