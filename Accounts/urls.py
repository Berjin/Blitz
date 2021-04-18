from django.urls import path
from . import views


urlpatterns = [
    path('home/',views.home,name='home'),
    path('', views.customer_login_view,name='customerlogin'),
    path('dashboard/',views.customer_dashboard, name='customer_dashboard'),
    path('request/',views.customer_request,name='request'),
    path('logout/',views.logout,name='logout'),
    path('orders/',views.orders,name='orders'),
    path('signup/',views.customer_signup,name='customersignup'),
    path('employeelogin/', views.employee_login_view,name='employeelogin'),
    path('employeedashboard',views.employee_dashboard, name='employee_dashboard')
]