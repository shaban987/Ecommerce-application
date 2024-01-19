from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import product,cart,order
from django.db.models import Q
import random
import razorpay




# Create your views here.



def home(request):
    context={}
    p=product.objects.filter(is_active=True)
    context['products']=p
    # print(p)
    return render(request,'index.html',context)

def pdetails(request,pid):
    p=product.objects.filter(id=pid)
    context={}
    context['products']=p
    return render(request,'product_detail.html',context)

def register(request):
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        
        if uname=="" or upass=="" or ucpass=="":
            context={}
            context['errmsg']="field cannot be empty"
            return render(request,'register.html',context)
        elif upass!=ucpass:
            context={}
            context['errmsg']="Plz check your password"
            return render(request,'register.html',context)
           
        else:
            u=User.objects.create(username=uname,password=upass,email=uname)
            u.set_password(upass)
            u.save()
            context={}
            context['success']="User created successfully!!"
            #return render('data is fetch successfully!!')
            return render(request,'register.html',context)
            context={}
            context['errmsg']="User name already exists"
            return render(request,'register.html',context)


    else:
        return render(request,'register.html')
    

    



def user_login(request):
    if request.method=="POST":
        uname=request.POST["uname"]
        upass=request.POST["upass"]
        # 
        if uname=="" or upass=="":
            context={}
            context['errmsg']="field can not be empty"
            return render(request,'login.html',context)
        
        else:
            u=authenticate(username=uname,password=upass)
            # print(u)
            # login(u)
            if u is not None:
                login(request,u)
                #login
            #return HttpResponse("in else part")
                return redirect('/home')
            
            else:
                context={}
                context['errmsg']="Invalid Username and password"
                return render(request,'login.html',context)

    else:
        return render(request,'login.html')
    

def user_logout(request):
    logout(request)
    return redirect('/home')

# def user_login(request):
#     login(request,u)
#     return redirect("/home")

def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=product.objects.filter(q1&q2)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def sort(request,sv):
    if sv== '0':
        col = 'price' #asc

    else:
        col = '-price' #decending

    p=product.objects.order_by(col)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def range(request):
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p=product.objects.filter(q1 & q2 & q3)
    context={}
    context['products']=p
    return render(request,'index.html',context)
    
    # print(min)
    # print(max)
    # return HttpResponse("value fetched")


def addtocart(request,pid):
   # userid=request.user.id
    u=User.objects.filter(id=request.user.id)
    print(u[0])
    p=product.objects.filter(id=pid)
    # print(p[0])
    q1=Q(uid=u[0])
    q2=Q(pid=p[0])
    c=cart.objects.filter(q1 and q2)
    n=len(c)
    # print(n )
    context={}
    context['products']=p
    if n==1:
        context['msg']='product already exist!!'
    
    else:
        c=cart.objects.create(uid=u[0],pid=p[0])
        c.save()
        context={}
        context['products']=c
        context['success']='Product added successfully in the cart !!!!!!!!!!!!!!'
    
    # print(pid)
    # print(userid)
    # return HttpResponse("id is fetched")
    return render(request,'product_detail.html',context)



       
       


def viewcart(request):
    if request.user.is_authenticated:
       # r=request.user.id
       c=cart.objects.filter(uid=request.user.id)
       np=len(c)
       s=0
       for x in c:
        s=s+x.pid.price*x.qty

        # print(s)
        context={}
        context['products']=c
        context['total']=s
        context['n']=np
        return render(request,'cart.html',context)
    else:
        return render('/login')
  

def remove(request,cid):
    c=cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')

def updateqty(request,qv,cid):
    c=cart.objects.filter(id=cid)
    # print(c)
    # print(c[0])
    # print(c[0].qty)
    if qv == '1':
        t=c[0].qty+1
        c.update(qty=t)

    else:
        if c[0].qty> 1:
            t=c[0].qty-1
            c.update(qty=t)

   
    return redirect('/viewcart')


def placeorder(request):
    userid=request.user.id
    # print(userid)
    c=cart.objects.filter(uid=userid)
    print(c)
    oid=random.randrange(1000,9999)
    print(oid)
    for x in c:
        # print(x)
        # print(x.pid)
        # print(x.qty)
        o=order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save() #shift data into order table
        x.delete()#delete records from cartv table
    # return HttpResponse("in pla
        
    orders=order.objects.filter(uid=userid)
    np=len(orders)
    s=0
    for x in c:
        # print(x.pid.price)
        s=s+x.pid.price*x.qty

        # print(s)
        context={}
        context['products']=c
        context['total']=s
        context['n']=np    

    
        # return HttpResponse("place order successfully")
        return render(request,'placeorder.html',context)


def makepayment(request):
    orders=order.objects.filter(uid=request.user.id)
    s=0
    for x in orders:
        # print(x)
        # print(x.pid.price)
        s=s+x.pid.price*x.qty
        oid=x.order_id
    
    client = razorpay.Client(auth=("rzp_test_ypQfWgA7Q3GLMS", "Usd0VLYFAwpmUirPRTIjuqlE"))


    DATA = {
    "amount": s * 100,
    "currency": "INR",
    "receipt": oid,
    "notes": {
        "key1": "value3",
        "key2": "value2"
         }
    }
    payment=client.order.create(data=DATA)
    print(payment)
    context={}
    context['data']=payment
    client.order.create(data=DATA)
    # return HttpResponse("paymnent section")   
    return render(request,'pay.html',context)


