from django.contrib import admin
from django.urls import path
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view(), name='home'),
    path('paypal/', PaypalView.as_view(), name='paypal'),
    path('bank/', BankView.as_view(), name='bank'),
    path('terminal/', Terminal.as_view(), name='terminal'),
    path('banksort/', BankSort.as_view(), name='banksort'),
    path('processor/', Processor.as_view(), name='processor'),   
]
