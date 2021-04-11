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

def customer_request(request):
    is_customer=request.COOKIES.get('is_customer')

    print(is_customer)
    if  is_customer=='1':
        
        
        print(is_customer)
        if request.method=='POST':
            cursor=connection.cursor()
            sql1 = "CREATE TABLE IF NOT EXISTS orders(oid int NOT NULL AUTO_INCREMENT PRIMARY KEY,vehicleno varchar(255),modelname varchar(255) NOT NULL,description varchar(255) , price varchar(255) ,datetime varchar(255),location varchar(255),cid int)"
            cursor.execute(sql1)

            cid=int(request.COOKIES.get('cid'))
            vehiclemodel=request.POST['vehiclemodel']
            description=request.POST['description']
            vehicleno=request.POST['vehicleno']
            location=request.POST['location']
            datetime=request.POST['datetime']
            
            
            sql2="INSERT INTO orders(modelname,vehicleno,description,cid,location,datetime) VALUES (%s,%s,%s,%s,%s,%s)"
            val=(vehiclemodel,vehicleno,description,cid,location,datetime)
            cursor.execute(sql2,val)
            return HttpResponse("successfull")

        else:

            return render(request,'customerrequest.html')

    else:
         return HttpResponse("Not authorized")
 