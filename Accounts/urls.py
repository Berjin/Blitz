from django.contrib import admin
from django.urls import path,include
from Accounts import views


urlpatterns = [
    path('customerdashboard',views.customer_dashboard, name='customer_dashboard'),
    path('customerlogin', views.customer_login_view,name='customerlogin'),
    path('customer-request',views.customer_request,name='request'),
    path('customersignup',views.customer_signup,name='customersignup'),
    path('customer-profile',views.customer_profile,name='customerprofile')
]