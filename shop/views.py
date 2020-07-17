from django.shortcuts import render , HttpResponse , redirect
from .models import product ,Contact,Orders,OrderUpdate
from math import ceil
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
import json
from django.views.decorators.csrf import csrf_exempt
# from paytm import Checksum 
from django.http import HttpResponse
MERCHANT_KEY = 'TryzCk02070492746526';   

def index(request):
    allprods= []
    catprods = product.objects.values('category','id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = product.objects.filter(category=cat)
        n = len(prod)
        nslides = n//4 + ceil((n/4)-(n//4))
        allprods.append([prod,range(1,nslides),nslides])
    # params = {'no_of_slides':nslides,'range': range(1,nslides), 'product': products}
  
    params = {'allprods':allprods}
    return render(request,'shop/index.html',params)
 
def about(request):
   return render(request, 'shop/about.html')
   
def contact(request):
   if request.method=='POST':
      name = request.POST.get('name','')
      email = request.POST.get('email','')
      phone = request.POST.get('phone','')
      desc = request.POST.get('desc','')
      # print(name,email,phone,desc)
      Contact(name=name ,email=email, phone=phone , desc=desc).save()      
   return render(request,'shop/contact.html')   

def tracker(request):
   if request.method=="POST":
      orderId = request.POST.get('orderId','')
      email = request.POST.get('email','')
      try:
         order = Orders.objects.filter(order_id=orderId,email=email)
         if len(order)>0:
            update = OrderUpdate.objects.filter(order_id=orderId)
            updates = []
            for item in update:
               updates.append({'text':item.update_desc,'time':item.timestamp})
               response = json.dumps(updates,default=str)
            return HttpResponse(response)      
         else:
            return HttpResponse('{}')
      except Exception as e:
         return HttpResponse('{}')              
   return render(request,'shop/tracker.html')

def search(request):
   return render(request,'shop/search.html')

def prodview(request,myid):
   Product = product.objects.filter(id=myid)
   return render(request,'shop/prodview.html',{'product': Product[0]})

def checkout(request):
   if request.method=='POST':
      items_json = request.POST.get('itemsJson','')
      name = request.POST.get('name','')
      amount = request.POST.get('amount','')
      email = request.POST.get('email','')
      address = request.POST.get('address1','') + " " + request.POST.get('address2','')
      city = request.POST.get('city','')
      state = request.POST.get('state','')
      zip_code = request.POST.get('zip_code','')
      phone = request.POST.get('phone','')
      # print("amount "+amount)
      o=Orders(items_json=items_json,amount=amount,name=name ,email=email, address=address , city=city , state=state, zip_code=zip_code, phone=phone)
      o.save()
      OrderUpdate(order_id=o.order_id,update_desc="the order has been placed").save()
      thank = True
      id = o.order_id
      return render(request,'shop/checkout.html',{'thank':thank,'id':id})
      param_dict = {
         'MID':'TryzCk02070492746526',
         'ORDER_ID':str(order.order_id),
         'TXN_AMOUNT':str(amount),
         'CUST_ID': email,
         'INDUSTRY_TYPE_ID':'Retail',
         'WEBSITE':'WEBSTAGING',
         'CHANNEL_ID':'WEB',
         'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',
      }
      param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict,MERCHANT_KEY)
      return render(request,'shop/paytm.html',{'param_dict': param_dict})
   return render(request,'shop/checkout.html')  

# def login(request):
#    if request.method=="POST":
#       Username = request.POST.get('Username','')
#       Password = request.POST.get('Password','')
#    return render(request,'shop/login.html')

# def signup(request):
#    if request.method=="POST":
#       Firstname = request.POST.get('Firstname','')
#       Lastname = request.POST.get('Lastname','')
#       email = request.POST.get('email','')
#       Password = request.POST.get('Password','')
#       # print(f"{Firstname},{Lastname},{email},{Password}")
#       su=Signup(Firstname=Firstname, Lastname=Lastname, email=email, Password=Password)
#       su.save()
#    return render(request,'shop/signup.html')

def handleSignup(request):
   if request.method=="POST":
      username = request.POST['username']
      fname = request.POST['fname']
      lname = request.POST['lname']
      email = request.POST['email']
      pass1 = request.POST['pass1']
      pass2 = request.POST['pass2']

      #checks for erronoues inputz
      if len(username) > 10:
         messages.error(request, "Username must be under 10 char")
         return redirect('ShopHome')
      if not username.isalnum():
         messages.error(request, "Username should only contain letters and numbers")
         return redirect('ShopHome') 
      if pass1 != pass2:
         messages.error(request, "Passwords do not match")
         return redirect('ShopHome')   


      #create the user 
      myuser = User.objects.create_user(username, email, pass1)
      myuser.first_name = fname
      myuser.last_name = lname
      myuser.save()
      messages.success(request, "Your account has been successfully created")
      return redirect('ShopHome')
      
      # return render(request,'shop/signup/',{'new':thank,'id':id})         

   else:
      return HttpResponse('404 - Not Found')

def handleLogin(request):
   if request.method == 'POST':
      loginusername = request.POST['loginusername']
      loginpassword = request.POST['loginpassword']

      user = authenticate(username=loginusername, password=loginpassword)
      if user is not None:
         login(request,user)
         messages.success(request, "Successfully logged in")
         return redirect('ShopHome')
      else:
         messages.error(request, "Invalid Credentials")
         return redirect('ShopHome')   
   return HttpResponse('404 - NOt Found')

def handleLogout(request):
   logout(request)
   messages.success(request, "Successfully Logged Out")
   return redirect('ShopHome')

   return HttpResponse('handleLogout')

@csrf_exempt   
def handlerequest(request): 
   form =request.POST
   response_dict = {} 
   for i in form.keys():
      response_dict[i] = form[i]
      if i == 'CHECKSUMHASH':
         checksum = form[i]
   verify = Checksum.verify_checksum(response_dict,MERCHANT_KEY,checksum)
   if verify:
      if response_dict['RESPCODE'] == '01':
         print('order suscessful')
      else:
         print('order not proceed because' + response_dict['RESPMSG'])         
   return render(request,'shop/paymentstatus.html',{'response':response_dict})
