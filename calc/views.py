
from django.shortcuts import render,redirect
from django.core.mail import send_mail,EmailMessage
from django.contrib.auth.models import User
from .models import User
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from .models import Transaction,Bus,Stoppings
from .paytm import generate_checksum, verify_checksum



from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as u_login
from django.contrib.auth import logout,authenticate
from calc.forms import UserForm,BookForm
from django.contrib import messages
import pyqrcode
import requests



import time

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.request import urlopen
import matplotlib.pyplot as plt
import json
import png



import webbrowser



'''url = "https://harisuriyakr.github.io/routes.json"
response = urlopen(url)
data_json = json.loads(response.read())'''






def validatelocation(request):




    from_data=request.session.get('from_data')
    to_data = request.session.get('to_data')
    '''emailid = request.session.get('email')
    username = request.session.get('username')

    emailid=User.objects.get(username='username').email'''
    bus=request.GET['bus']


    print(bus)
    b=Bus.objects.get(busnumber=bus)
    busy=Stoppings.objects.filter(b=b)




    listofstoppings=[c.stopping for c in busy]
    stop1=listofstoppings.index(from_data)
    stop2 = listofstoppings.index(to_data)

    type = b.type
    cost = b.cost
    ceats=b.ceats
    ceats=ceats-1
    b.ceats=ceats
    b.save(update_fields=['ceats'])
    cost_of_single=cost/len(listofstoppings)
    cost=(abs(stop2-stop1))*cost_of_single



    from_data=request.session.get('from_data')
    to_data = request.session.get('to_data')


    busnumber=b.busnumber
    type=b.type

    request.session['busnumber'] = busnumber
    request.session['type'] = type

    request.session['cost'] = cost
    '''except KeyError as err:
        message="Enter valid from to addres'''


    cost = request.session.get('cost')
    busnumber = request.session.get('busnumber')
    type = request.session.get('type')
    '''emailid = request.session.get('email')'''
    from_data=request.session.get('from_data')
    to_data = request.session.get('to_data')

    message = "Hello\nThanks for choosing our website. \n you booked from {0} to {1}. \nCost : {2}\nBus Number:{3}\nBus type:{4}\nCeats remaining:{5}\nThanks and regards\nTICKET ADMIN".format(
        from_data, to_data, cost,busnumber ,
        type,ceats)
    '''print(mail_content)
    print(emailid)'''

    '''send_mail(
        'Ticket for your trip',
        mail_content,
        'ksdiwakar04032002@gmail.com',
        [emailid],
        fail_silently=False

    )'''

    '''message1="Ticket send to mail please check!!!"
    distance = bus.distance
    cost = bus.cost'''
    '''img = pyqrcode.create(
        'upi://pay?pa=uoid@okhdfcbank&pn=Name%20K%20R&am={0}&cu=INR&aid=uGICAgIDV2fyYWw'.format(cost))
    img.png("myqr.png", scale=8)
    src1="myqr.png"

    time.sleep(5)
    webbrowser.open(
    "https://www.google.com/maps/dir/{0},+Tamil+Nadu,+India/{1},+Karnataka,+India/".format(from_data, to_data))
    return render(request,'calc/pay.html')'''
    return render(request,"calc/details.html",context={'message':message,'from_data':from_data,'to_data':to_data,'cost':cost,'busnumber':busnumber,'type':type,'ceats':ceats})


def booked(request):
    return render(request,'calc/booked.html',{'message':message,'message1':message1,'src1':src1})







def home(request):
    username=request.session.get('username')
    password = request.session.get('password')
    emailid= request.session.get('email')

    if request.method=="POST":
        form=BookForm(request.POST)
        if form.is_valid():





            from_data = form.cleaned_data["from_data"]
            request.session['from_data']=from_data
            to_data = form.cleaned_data["to_data"]
            request.session['to_data'] = to_data
            '''url = "https://harisuriyakr.github.io/routes.json"
            response = urlopen(url)
            data_json = json.loads(response.read())'''
            bus=Bus(from_data=from_data,to_data=to_data)
            uid_bus="123"
            cost = "200"
            return redirect('calc:bus_choose')


    form = BookForm()
    return render(request,'calc/home.html',{'form':form})


def login(request):


    if request.method=="POST":
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():

            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            email = form.cleaned_data.get("email")
            request.session['username']=username
            request.session['password'] = password
            request.session['email'] = email


            user=authenticate(username=username,password=password)

            if user is not None:
                u_login(request,user)
                messages.info(request,f"You are now logged in as {username}")
                return redirect("calc:home")
            else:
                messages.error(request,f"Inavalid username and password")
        else:
            messages.error(request, f"Inavalid username and password")

    form=AuthenticationForm()

    return render(request,'calc/login.html',context={'form':form})
def register(request):


    if request.method=='POST':
        form=UserForm(request.POST)
        if form.is_valid():
            user=form.save()

            username=form.cleaned_data.get('username')
            request.session['username']=username
            emailid = form.cleaned_data.get('email')

            print(emailid)
            request.session['email']=emailid



            messages.success(request,f"New accont created : {username}")
            u_login(request,user)
            return redirect('calc:home')
        else:
            for msg in form.error_messages:
                messages.error(request,f"{msg}:{form.error_messages[msg]}")
    form = UserForm()



    return render(request,'calc/register.html',context={'form':form})
def logout_request(request):
    logout(request)
    messages.info(request,f"You are logged out successfully")
    return render(request,"calc/home.html")










def initiate_payment(request):
    if request.method == "GET":
        return render(request, 'calc/pay.html')
    try:
        username=request.POST['username']
        password=request.POST['password']
        amount = int(request.POST['amount'])
        user = authenticate(request, username=username, password=password)
        if user is None:
            raise ValueError
        auth_login(request=request, user=user)
    except:
        return render(request, 'calc/pay.html', context={'error': 'Wrong Accound Details or amount'})

    transaction = Transaction.objects.create(made_by=user, amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'calc/redirect.html', context=paytm_params)
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'calc/callback.html', context=received_data)
        return render(request, 'calc/callback.html', context=received_data)
def bus_choose(request):
    '''if request.method=="POST":

        bus=request.POST["bus"]
        request.session['bus']=bus
        print(bus)
        return redirect("/validatelocation")'''



    from_data=request.session.get("from_data")
    to_data = request.session.get("to_data")


    list_of_buses1=[c.b.busnumber for c in Stoppings.objects.filter(stopping=from_data) ]
    list_of_buses2=[c.b.busnumber for c in Stoppings.objects.filter(stopping=to_data) ]

    list_of_buses1=set(list_of_buses1)
    list_of_buses2=set(list_of_buses2)
    list_of_buses=list(list_of_buses1&list_of_buses2)

    print(list_of_buses)



    return render(request,'calc/choose_bus.html',context={'list_of_buses':list_of_buses})
