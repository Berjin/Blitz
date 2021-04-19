from django.shortcuts import render,redirect

from django.contrib import messages
from django.db import connection
from django.http import HttpResponse
from django.template import loader

def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def customer_login_view(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        cursor=connection.cursor()
        cursor.execute( "SELECT cpassword,cid FROM customer WHERE cname=%s",[username])
        r=cursor.fetchall()   
        for  p in r:
       
            
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
    cid=int(request.COOKIES.get('cid'))
    if is_customer=='1':
        cursor=connection.cursor()
        cursor.execute("SELECT vehicleno,modelname,description,status FROM orders WHERE cid=%s ",[cid])
        var=dictfetchall(cursor)
        context={'orders':var}
        return render(request,'dashboard.html',context)
    else:
        return redirect('/')

def customer_request(request):
    is_customer=request.COOKIES.get('is_customer')
    print(is_customer)

    if  is_customer=='1':
        print(is_customer)
        if request.method=='POST':
            cursor=connection.cursor()
            sql1 = "CREATE TABLE IF NOT EXISTS orders(oid int NOT NULL AUTO_INCREMENT PRIMARY KEY,vehicleno varchar(255),modelname varchar(255) NOT NULL,description varchar(255) , price varchar(255) ,datetime varchar(255),location varchar(255),status varchar(255) DEFAULT 'Pending',cid int,empid int)"
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
            return render(request,'request.html',{'status':'Request Created Successfully'})
        else:
            return render(request,'request.html',{'status':''})

    else:
         return redirect('/')

def home(request):
    context = {}
    return render(request,'base.html',context)

def logout(request):
    response= redirect('/')
    response.set_cookie('cid',0)
    response.set_cookie('eid',0)
    response.set_cookie('is_customer','0')
    response.set_cookie('is_admin','0')
    return response

def admindashboard(request):
    is_admin=request.COOKIES.get('is_admin')
    eid=int(request.COOKIES.get('eid'))
    if is_admin=='1':
        cursor=connection.cursor()
        if request.method=='POST':
                    cid = 3
                    # if request.POST['cancel']=='cancel':
                    #     cursor.execute("UPDATE orders SET status='Cancelled' WHERE cid=%s ",[cid])
                    #     cursor.fetchall()
                    #     return redirect('/admindashboard')  
                    # elif request.POST['completed']=='completed':
                    #     cursor.execute("UPDATE orders SET status='Completed' WHERE cid=%s ",[cid])
                    #     cursor.fetchall()
                    #     return redirect('/admindashboard')
                    # elif request.POST['addemployee']=='addemployee':
                    #     cursor.execute("UPDATE orders SET empid=1 WHERE cid=%s ",[cid])
                    #     cursor.fetchall()
                    #     return redirect('/admindashboard')
        else:     
            cursor.execute("SELECT cid,vehicleno,modelname,description,status FROM orders")
            var=dictfetchall(cursor)
            context={'orders':var}
            return render(request,'orders.html',context)
    else:
        return HttpResponse("Not authorized")

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


def customer_profile(request):
    is_customer=request.COOKIES.get('is_customer')
    if is_customer=='1':

        if request.method=='POST':
            cursor=connection.cursor()
            cid=int(request.COOKIES.get('cid'))
            username=request.POST['username']
            password=request.POST['password']
            email=request.POST['email']
            #phoneno=request.POST['phoneno']
            vehicleno=request.POST['vehicleno']

            # sql1="UPDATE customer SET cname=%s, cpassword=%s,phoneno=%s,email=%s, vehicleno=%s WHERE cid=%s"
            sql1="UPDATE customer SET cname=%s, cpassword=%s,email=%s, vehicleno=%s WHERE cid=%s"
            # val=(username,password,phoneno,email,vehicleno,cid)
            val=(username,password,email,vehicleno,cid)

            cursor.execute(sql1,val)
            response= redirect('/customer-profile')
            return response

    

        else:
            cid=int(request.COOKIES.get('cid'))
            cursor=connection.cursor()
            # cursor.execute( "SELECT cname,cpassword,email,phoneno,vehicleno FROM customer WHERE cid=%s",[cid])
            cursor.execute( "SELECT cname,cpassword,email,vehicleno FROM customer WHERE cid=%s",[cid])
            r=cursor.fetchall() 
            for  p in r:

                username=p[0]
                password=p[1]
                email=p[2]
                # phoneno=p[3]
                # vehicleno=p[4]
                vehicleno=p[3]
                #
            return render(request,'customer_profile.html',{'username':username,'password':password,'email':email,'vehicleno':vehicleno})

            # return render(request,'customer_profile.html',{'username':username,'password':password,'email':email,'phoneno':phoneno,'vehicleno':vehicleno})
            


    else:


        return HttpResponse("Not authorized")



def employee_login_view(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        cursor=connection.cursor()
        cursor.execute( "SELECT epassword,eid,is_admin FROM employee WHERE ename=%s",[username])
        r=cursor.fetchall()   
        for  p in r:
        
            if p[0]==password:
                print("success")
                if p[2]==1:

                    response= redirect('/admin')
                    response.set_cookie('eid',p[1])
                    response.set_cookie('is_employee','1')
                    response.set_cookie('is_admin','1')
                    return response
                else:

                    response= redirect('/employeedashboard')
                    response.set_cookie('eid',p[1])
                    response.set_cookie('is_employee','1')
                    response.set_cookie('is_admin','0')
                    return response
        return render(request,'employee_login.html')                

    else: 
        return render(request,'employee_login.html')


def employee_dashboard(request):
    is_employee=request.COOKIES.get('is_employee')
    eid=int(request.COOKIES.get('eid'))
    print(eid)
    print(is_employee)
    if is_employee=='1':
        cursor=connection.cursor()
        if request.method=='POST': 
                    cursor.execute("UPDATE orders SET status='Completed' WHERE empid=%s ",[eid])
                    cursor.fetchall()
                    return redirect('/employeedashboard')  
        else:     
            cursor.execute("SELECT cid,vehicleno,modelname,description,status FROM orders WHERE empid=%s ",[eid])
            var=dictfetchall(cursor)
            context={'orders':var}
            print(context)
            return render(request,'employeedashboard.html',context)
      
        
       
    else:
        return HttpResponse("Not authorized")


def admin(request):
    is_admin=request.COOKIES.get('is_admin')
   
    if is_admin=='1':
      
        return render(request,'adminmain.html')
       
    else:
        
        return HttpResponse("Not authorized")

def edit_customers(request):

    cursor=connection.cursor()
    if request.method=='POST':

        

        cid=request.POST['cid']
        
        cursor.execute("DELETE FROM customer WHERE cid=%s",[cid])
        return redirect('/editcustomers')

        

    else:

        cursor.execute("SELECT cid,cname,email,phoneno,vehicleno FROM customer ")
        var=dictfetchall(cursor)
        context={'customers':var}
        
        return render(request,'editcustomers.html',context)
def customer_add(request):
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
        return redirect('/editcustomers')
    else:           
        return redirect('/editcustomers')




        



 