from django.urls import path
from . import views
from . import models
urlpatterns = [
    path('api/restaurants/', views.restaurants ),
    path('api/restaurants/email', views.get_data_by_email ),
    path('api/restaurants/name', views.get_data_by_name ),
    path('api/restaurants/password', views.change_password),
    path('api/restaurants/info', views.get_restaurant_info),
    path('api/restaurants/near_me', views.get_near_me)
]