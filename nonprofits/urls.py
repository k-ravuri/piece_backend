from django.urls import path
from . import views
from . import models
urlpatterns = [
    path('api/nonprofits/', views.nonprofits ),
    path('api/nonprofits/email/', views.get_data_by_email ),
    path('api/nonprofits/password/', views.change_password ),
    path('api/nonprofits/overbudget_rests_near/', views.overbudget_rests_near ),
    path('api/nonprofits/underbudget_rests_near/', views.underbudget_rests_near ),
    path('api/nonprofits/accept_req_email_to_np/', views.accept_req_email_to_np ),
    path('api/nonprofits/reject_req_email_to_np/', views.reject_req_email_to_np )
]