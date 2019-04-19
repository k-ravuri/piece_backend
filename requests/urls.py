from django.urls import path
from . import views
from . import models
urlpatterns = [
    path('api/requests/', views.requests ),
]