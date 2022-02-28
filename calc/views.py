
from geopy.geocoders import Nominatim
from django.shortcuts import render,redirect
from django.core.mail import send_mail,EmailMessage
from django.contrib.auth.models import User
from .models import User
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from .models import Transaction,Bus,Ticket
from .paytm import generate_checksum, verify_checksum

import folium
import difflib






from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as u_login
from django.contrib.auth import logout,authenticate
from calc.forms import UserForm,BookForm
from django.contrib import messages





import time

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.request import urlopen

import json




'''url = "https://harisuriyakr.github.io/routes.json"
response = urlopen(url)
data_json = json.loads(response.read())'''






def validatelocation(request):




    froma_real=request.session.get('froma_real')
    toa_real=request.session.get('toa_real')
    timea_real=request.session.get('timea_real')
    from_data=request.session.get('from_data')
    to_data = request.session.get('to_data')
    '''emailid = request.session.get('email')
    username = request.session.get('username')

    emailid=User.objects.get(username='username').email'''
    bus=request.GET['bus']

    print(bus)
    b=Bus.objects.get(busnumber=bus)






    listofstoppings=b.stopping_including_initial_and_final_destination.split(",")

    stop1=listofstoppings.index(froma_real)
    stop2 = listofstoppings.index(toa_real)

    type = b.type
    cost = b.cost
    seats=b.seats
    index1=listofstoppings.index(froma_real)











    no_of_tickets=request.session.get('no_of_tickets')
    b.save(update_fields=['seats'])
    cost_of_single=cost/len(listofstoppings)
    cost=(abs(stop2-stop1))*cost_of_single
    cost=cost*int(no_of_tickets)



    froma_real=request.session.get('froma_real')
    toa_real = request.session.get('toa_real')




    busnumber=b.busnumber
    type=b.type

    request.session['busnumber'] = busnumber
    request.session['type'] = type



    request.session['cost'] = cost
    ticket=Ticket.objects.create(busnumber=busnumber,initial=froma_real,final=toa_real,no_of_tickets=no_of_tickets)
    ticket.save()
    '''except KeyError as err:
        message="Enter valid from to addres'''


    cost = request.session.get('cost')
    busnumber = request.session.get('busnumber')
    type = request.session.get('type')
    '''emailid = request.session.get('email')'''
    froma_real=request.session.get('froma_real')
    toa_real = request.session.get('toa_real')

    message = "Hello\nThanks for choosing our website. \n you booked from {0} to {1}. \nCost : {2}\nBus Number:{3}\nBus type:{4}\nCeats remaining:{5}\nThanks and regards\nTICKET ADMIN".format(
        froma_real, toa_real, cost,busnumber ,
        type,seats)
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
    return render(request,"calc/details.html",context={'message':message,'from_data':from_data,'to_data':to_data,'cost':cost,'busnumber':busnumber,'type':type,'seats':seats})


def booked(request):
    return render(request,'calc/booked.html',{'message':message,'message1':message1,'src1':src1})







def home(request):


    if request.method=="POST":



        from_data=request.POST['from_data']
        to_data=request.POST['to_data']
        date=request.POST['date']
        time=request.POST['time']
        no_of_tickets=request.POST['no_of_tickets']
        request.session['no_of_tickets']=no_of_tickets


        request.session['from_data']=from_data
        request.session['to_data']=to_data
        request.session['date']=date
        request.session['time']=time

        return redirect('calc:bus_choose')



    return render(request,"calc/home.html")























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
        busnumber=request.session.get("busnumber")
        initial=request.session.get("from_data")
        final=request.session.get("to_data")

        amount = int(request.POST['amount'])
        #t=Ticket(busnumber=)
        user = authenticate(request, username=username, password=password)
        if user is None:
            raise ValueError
        auth_login(request=request, user=user)
    except:
        return render(request, 'calc/pay.html', context={'error': 'Wrong Account Details or amount'})

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
    no_of_tickets=request.session.get("no_of_tickets")

    geolocator = Nominatim(user_agent="http")
    location1 = geolocator.geocode(from_data)
    location2 = geolocator.geocode(to_data)
    data1=location1.raw
    data2=location2.raw

    location1=float(data1['lat']),float(data1['lon'])
    location2=float(data2['lat']),float(data2['lon'])
    p=folium.Map(location1)
    folium.Marker(location1,popup=from_data).add_to(p)
    folium.Marker(location2,popup=to_data).add_to(p)
    from geopy.distance import distance
    km=distance(location1,location2)
    mile=distance(location1,location2).miles
    folium.PolyLine((location1,location2)).add_to(p)
    list_of_buses=[]
    date=request.session.get("date")
    time=request.session.get("time")




    for c in Bus.objects.filter(date=date):
        froma=difflib.get_close_matches(from_data,list(c.stopping_including_initial_and_final_destination.split(',')))
        toa=difflib.get_close_matches(to_data,list(c.stopping_including_initial_and_final_destination.split(',')))
        timea=difflib.get_close_matches(time,list(c.timing.split(',')))
        stop=c.stopping_including_initial_and_final_destination.split(',')
        if len(froma)!=0 and len(toa)!=0 and len(timea)!=0:


            if froma[0] in c.stopping_including_initial_and_final_destination.split(',') and toa[0] in c.stopping_including_initial_and_final_destination.split(',') and timea[0] in c.timing.split(',') :

                froma_real=froma[0]
                toa_real=toa[0]
                timea_real=timea[0]
                busnum=c.busnumber

                list_of_buses.append(busnum)






    p.save('map.html')
    request.session['froma_real']=froma_real
    request.session['toa_real']=toa_real
    request.session['timea_real']=timea_real













    return render(request,'calc/choose_bus.html',context={'list_of_buses':list_of_buses,'stop':froma,'p':p._repr_html_()})
