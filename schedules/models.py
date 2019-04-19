from django.db import models
from django.db import connection
import psycopg2
import pprint
from django.http import HttpResponseRedirect

# Create your models here
class Schedule(models.Model):
    email = models.CharField(max_length = 100, primary_key=True)
    mondaystart = models.IntegerField(default=0, null=True)
    mondayend = models.IntegerField(default=0, null=True)
    tuesdaystart = models.IntegerField(default=0, null=True)
    tuesdayend = models.IntegerField(default=0, null=True)
    wednesdaystart = models.IntegerField(default=0, null=True)
    wednesdayend = models.IntegerField(default=0, null=True)
    thursdaystart = models.IntegerField(default=0, null=True)
    thursdayend = models.IntegerField(default=0, null=True)
    fridaystart = models.IntegerField(default=0, null=True)
    fridayend = models.IntegerField(default=0, null=True)
    saturdaystart = models.IntegerField(default=0, null=True)
    saturdayend = models.IntegerField(default=0, null=True)
    sundaystart = models.IntegerField(default=0, null=True)
    sundayend = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.name
    def getEmail(self):
        return self.email
    def setEmail(email):
         self.email = email
