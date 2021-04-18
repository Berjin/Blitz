from django.shortcuts import render,redirect

from django.contrib import messages
from django.db import connection
from django.http import HttpResponse
from django.template import loader

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
                response= redirect('dashboard/')
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
            sql1 = "CREATE TABLE IF NOT EXISTS orders(oid int NOT NULL AUTO_INCREMENT PRIMARY KEY,vehicleno varchar(255),modelname varchar(255) NOT NULL,description varchar(255) , price varchar(255) ,datetime varchar(255),location varchar(255),status varchar(255) DEFAULT 'pending',cid int)"
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
            return render(request,'customerrequest.html',{'status':'Request Created Successfully'})

        else:

            return render(request,'customerrequest.html',{'status':''})

    else:
         return HttpResponse("Not authorized")

def home(request):
    context = {}
    return render(request,'base.html',context)

def customer_signup(request):
    if request.method=='POST':

        username=request.POST['username']
        password=request.POST['password']
        email=request.POST['email']
        phoneno=request.POST['phoneno']
        vehicleno=request.POST['vehicleno']
        cursor=connection.cursor()
        sql1="CREATE TABLE IF NOT EXISTS customer(cid int NOT NULL AUTO_INCREMENT PRIMARY KEY,cname varchar(255) UNIQUE,cpassword varchar(255) NOT NULL,email varchar(255) , phoneno varchar(255) ,vehicleno varchar(255))"
        cursor.execute(sql1)
        sql2=   "INSERT INTO customer(cname ,cpassword,phoneno,email,vehicleno) VALUES (%s,%s,%s,%s,%s)"
        val=(username,password,phoneno,email,vehicleno)
        cursor.execute(sql2,val)
        return render(request,'customer_signup.html',{'status':'your account has been successfully created'})
                

    else:    
        return render(request,'customer_signup.html',{'status':''})


def employee_login_view(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        cursor=connection.cursor()
        cursor.execute( "SELECT epassword,eid FROM employee WHERE ename=%s",[username])
        r=cursor.fetchall()   
        for  p in r:
            print (p)
            print (p[0])
            
            if p[0]==password:
                print("success")
                response= redirect('employeedashboard/')
                response.set_cookie('eid',p[1])
                response.set_cookie('is_employee','1')
                return response
                

        
        return render(request,'employee_login.html')                

    else: 
        return render(request,'employee_login.html')

def employee_dashboard(request):
    is_employee=request.COOKIES.get('is_employee')
    print(is_employee)
    if is_employee=='1':
      
        return render(request,'employeebase.html')
       
    else:
        
        return HttpResponse("Not authorized")
        
        



 