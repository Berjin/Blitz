from django.urls import path,include
from Accounts import views


urlpatterns = [
    path('',include('Accounts.urls')),
]
