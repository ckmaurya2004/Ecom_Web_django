
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    
    path('',views.index),
    path('signup/',views.signUp),
    path('login/',views.handlerlogin),
    path('logout/',views.handlerlogout),
    path('about/',views.about),
    path('contact/',views.contact),
    path('cart/',views.cart),
    path('checkout/',views.checkout),
    path('tracker/',views.tracker),
   


]