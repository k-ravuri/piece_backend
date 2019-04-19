from django.urls import path
from . import views
from . import models
urlpatterns = [
    path('api/schedules/', views.schedules ),
    path('api/schedules/email', views.get_data_by_email ),
    path('api/schedules/create_with_email', views.create_schedule_by_email ),
    path('api/schedules/change_mondaystart', views.change_mondaystart ),
    path('api/schedules/change_mondayend', views.change_mondayend ),
    path('api/schedules/change_tuesdaystart', views.change_tuesdaystart ),
    path('api/schedules/change_tuesdayend', views.change_tuesdayend ),
    path('api/schedules/change_wednesdaystart', views.change_wednesdaystart ),
    path('api/schedules/change_wednesdayend', views.change_wednesdayend ),
    path('api/schedules/change_thursdaystart', views.change_thursdaystart ),
    path('api/schedules/change_thursdayend', views.change_thursdayend ),
    path('api/schedules/change_fridaystart', views.change_fridaystart ),
    path('api/schedules/change_fridayend', views.change_fridayend ),
    path('api/schedules/change_saturdaystart', views.change_saturdaystart ),
    path('api/schedules/change_saturdayend', views.change_saturdayend ),
    path('api/schedules/change_sundaystart', views.change_sundaystart ),
    path('api/schedules/change_sundayend', views.change_sundayend )
]