from django.urls import path
from . import views
from . import models
urlpatterns = [
    path('api/dishes/', views.dishes ),
    path('api/dishes/decrement_price', views.dishes_price ),
    path('api/dishes/rec_price', views.dishes_rec_price),
]