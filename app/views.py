from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import View, CreateView, ListView, TemplateView
from .models import *
from django import forms
from django.db import transaction

class Processor(TemplateView):
    template_name = 'processor.html'  


class PaypalForm(forms.ModelForm):
    class Meta:
        model = PayPal
        fields = ('__all__')

class PaypalView(CreateView):
    
    template_name = 'paypal.html'
    success_url = reverse_lazy('home')
    form_class = PaypalForm 
    
class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ('__all__')

class BankView(CreateView):    
    template_name = 'bank.html'
    success_url = reverse_lazy('home')
    form_class = BankForm    

class Home(ListView):
    model = PayPal
    template_name = 'home.html'
    context_object_name = 'paypal_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bank_list'] = Bank.objects.all()
        return context

class TerminalForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("__all__")

class Terminal(View):    
    
    def post(self, request):
        form = TerminalForm(request.POST)
        if form.is_valid():            
            bank_client = form.cleaned_data['banks']
            paypal_client = form.cleaned_data['paypals']
            transfer = form.cleaned_data['transfer']                            
            
            bank_data = Bank.objects.get(name=bank_client)
            paypal_data = PayPal.objects.get(name=paypal_client)                
            
            bank_client_balance = int(bank_data.balance)
            paypal_client_balance = int(paypal_data.balance)
            print(bank_client_balance)
            try:
                with transaction.atomic():
                    bank_client_balance -= int(transfer)
                    paypal_client_balance += int(transfer)
                    bank_data.balance = bank_client_balance
                    paypal_data.balance = paypal_client_balance
                    bank_data.save()
                    paypal_data.save()                    
                    if bank_client_balance < 0 or paypal_client_balance < 0 :
                        print("rollback")
                        transaction.set_rollback(True)
                        
                        # return HttpResponse('Not sufficient funds')
                        context = {'error_message':'not sufficient funds'}
                        return render(request, 'message.html', context)
                    else:
                        return redirect('home')            
            except Exception as e:
                context = {'form':form, 'error_message': str(e)}
                return render(request, 'terminal.html', context)            
        else:
            context = {'form':form}
            return render(request, 'terminal.html', context)
    
    def get(self, request):
        form = TerminalForm()
        context = {'form':form}
        return render(request, 'terminal.html', context)
        
class BankSort(View):
    def get(self, request):
        bank_sorted_by_balance = Bank.banksorted.all()
        not_sorted = Bank.objects.all()
        context = {'clients': bank_sorted_by_balance, 'not_sorted':not_sorted}
        return render(request, 'banksort.html', context)
    
        
# class Terminal(CreateView):
#     model = Order
#     forms_class = TerminalForm
#     template_name = 'terminal.html'
#     success_url = reverse_lazy('home')


# @transaction.atomic
# def terminal(request):
#     if request.method == 'POST':
#         paypalForm = PaypalTerminalForm(request.POST)
#         bankForm = BankTerminalForm(request.POST)
#         if paypalForm.is_valid() and bankForm.is_valid():

#     bank = Bank.objects.all()
#     paypal = PayPal.objects.all()


