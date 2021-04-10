from django.shortcuts import render,redirect

from django.contrib import messages
from django.db import connection
from django.http import HttpResponse
from django.template import loader
# Create your views here.
def customer_login_view(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        cursor=connection.cursor()
        cursor.execute( "SELECT cpassword,cid FROM customer WHERE cname=%s",[username])
        r=cursor.fetchall()   
        for  p in r:
            print (p)
            print (p[0])
            
            if p[0]==password:
                print("success")
                response= redirect('customerdashboard/')
                response.set_cookie('cid',p[1])
                response.set_cookie('is_customer','1')
                return response
                

        
        return render(request,'customer_login.html')
        
        


    else: 
        return render(request,'customer_login.html')

def customer_dashboard(request):
    is_customer=request.COOKIES.get('is_customer')
    print(is_customer)
    if is_customer=='1':
      
        return render(request,'customerbase.html')
       
    else:
        
        return HttpResponse("Not authorized")