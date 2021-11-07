from django.urls import path

from . import views

app_name='calc'
urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.logout_request,name='logout'),
    path('booked/',views.booked,name='booked'),
    path('pay/', views.initiate_payment, name='pay'),
    path('bus_choose/', views.bus_choose, name='bus_choose'),
    path('callback/', views.callback, name='callback'),
    path('validatelocation', views.validatelocation, name='validatelocation'),

]