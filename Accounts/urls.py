from django.urls import path
from . import views


urlpatterns = [
    path('home/',views.home,name='home'),
    path('', views.customer_login_view,name='customerlogin'),
    path('dashboard/',views.customer_dashboard, name='dashboard'),
    path('request/',views.customer_request,name='request'),
    path('logout/',views.logout,name='logout'),
    path('signup/',views.customer_signup,name='customersignup'),
    path('employeelogin/', views.employee_login_view,name='employeelogin'),
    path('employeedashboard',views.employee_dashboard, name='employee_dashboard'),
    path('customer-profile',views.customer_profile,name='customer_profile'),
    path('admin',views.admin,name='admin'),
    path('editcustomers',views.edit_customers,name='editcustomer'),
     path('addcustomers',views.customer_add,name='addcustomer')

]