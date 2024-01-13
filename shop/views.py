from django.shortcuts import render,redirect
from django.http import HttpResponse
from . models import *
from  math import ceil
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
import json
import datetime
from .mymiddleware.my_auth_middle import auth_middleware
from django.utils.decorators import method_decorator

# Create your views here.

def index(request):
    if request.method == 'POST':
        myprod = request.POST.get('cartprod')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            qty = cart.get(myprod)
            if qty:
                if remove:
                    if qty<=1:
                        cart.pop(myprod)
                    else:
                        cart[myprod] = qty-1
                else:    
                    cart[myprod] = qty+1
            else:
              cart[myprod]=  1
        else:
            cart={}
            cart[myprod] = 1
        request.session['cart'] = cart
        print(cart)
        return redirect('/') 

    if request.method == 'GET':
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] ={}
        prod = None
        category = Category.objects.all()
        categoryId = request.GET.get('category',"")
        if categoryId:
            prod = Product.objects.filter(category = categoryId)
        else:
            prod = Product.objects.all()
     
        param = {'products':prod,'categories':category}
        # print(request.session.get('email'))
        return render(request, 'index.html',param)


def signUp(request):
    if request.method == 'POST':
        username = request.POST.get('name',"")
        email = request.POST.get('email',"")
        fname = request.POST.get('fname',"")
        lname = request.POST.get('lname',"")
        pass1 = request.POST.get('password1',"")
        pass2 = request.POST.get('password2',"")
        #some check
        if len(username)>15:
            messages.error(request, "Please enter your name under the 15 character!.")
            return redirect('/') # redirect('/') same
        if pass1 != pass2:
            messages.error(request, "Your password does not match Pealse try again!.")
            return redirect('/') # redirect('/') same    
        #create the user
        myuser =  User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your  account has been successfully created")
        return redirect('/') # redirect('/') same
    else:
        return HttpResponse("found error")
    
def handlerlogin(request): 
    if  request.method == "POST":
        name = request.POST.get('name1',"")
        password = request.POST.get('pass',"")
        user = authenticate(username = name , password = password)
        if user is not None:
            request.session.clear()
            login(request,user)
            messages.success(request, "successfully logged in....")
            # user = request.user
            # request.session['user_id'] = user
            # request.session['email'] = request.user.email
            # print(request.session['email'])
            return redirect('/') 
        else:
             messages.error(request, "Invalid credentials .")
    return HttpResponse('404 not found')


def handlerlogout(request):
    logout(request)
    messages.success(request,"logout has been successfully !")
    return redirect("/")

def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method =='POST':      
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        desc = request.POST.get('desc','')
        contact = Contact(name = name, email=email , phone = phone , desc = desc)
        messages.success(request,"contact has been successfully !")
        contact.save()
        return render(request, 'contact.html') 
    return render(request , 'contact.html')


# @auth_middleware
def cart(request):
    if request.method =='GET':
        ids = list(request.session.get('cart').keys())
        prod_item = Product.objects.filter(id__in =ids)
        param = {'product':prod_item}
        return render(request,'cart.html',param)
    


def checkout(request):
    cat_cart = request.session.get('cart').keys()
    prod= Product.objects.filter(id__in = cat_cart)
    product = []
    p =[]
    
    cart_val= request.session.get('cart').values()
    
    for item in prod: 
        p.append(item.name)
    c=0
    for item in cart_val:
        for i in p:
            product.append([p[c],item])
            c = c+1
            break
    myprice = Product.objects.all()
    param = {'products':product,'price':myprice}
            
    if request.method == "POST":
            cat= request.session.get('cart')
            # prodj= Product.objects.filter(id__in=list(cat.keys()))
            # product =   prod
            # user = request.user
           
            address = request.POST.get('address','')
            phone = request.POST.get('phone','')
            for p in prod:
                order = Order(product = p,user = request.user,qty =cat.get(str(p.id)),price = p.price,address = address,phone = phone,date = datetime.datetime.today())
                order.save()
            messages.success(request,f"successfully placed order {order.id}")
            request.session['cart'] = {}
    return render(request,'checkout.html',param)    

def tracker(request):
    param ={}
    msg = ""
    if request.method =="POST":
        orderid = request.POST.get('orderId','')
        print(orderid)
        try:
            order = Order.objects.filter(id = orderid)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id = orderid)
                print(update)
                updates = []
                for item in update:
                    updates.append([item.update_desc,item.timestemp])
                    msg = "success"
                param = {'newupdate':updates,'msg':msg}
                
                messages.success(request,"successfully")
                
            else:
                return redirect('tracker')

        except Exception as e:
           return HttpResponse(e)
#     return render(request,'tracker.html',param)



