from django.urls import path
from . import views
from . import models
urlpatterns = [
    path('api/restaurant/', views.RestaurantListCreate.as_view() ),
    
    # path('api/get', models.GetRestaurants_raw_sql_query ),
    # path('api/get', models.main_rest ),
    # path('api/get/', models.my_custom_sql ),
    path('api/get/', views.index ),
    path('api/loginRes/', views.loginR ),
    path('api/loginNonP/', views.loginN ),
    path('api/forgotpassRes/', views.forgotpassR ),
    path('api/forgotpassNonP/', views.forgotpassN ),
    path('api/unsubRes/', views.unsubscribeR ),
    path('api/unsubNonP/', views.unsubscribeN ),
    path('api/registerRes/', views.registernewR ),
    path('api/registerNonP/', views.registernewN ),
    path('api/register_dish/', views.registernew_dish ),
    path('api/unsub_dish/', views.unsubscribe_dish ),
    path('api/restaurant/username/', views.find_res ),
    path('api/nonprofit/username/', views.find_nonP ),
    path('api/dishes/atRes/', views.find_dishes),
    path('api/dishes/getPrice/', views.get_price),
    # path('get/', index.html )
    # path('search/', views.showSearch)
]