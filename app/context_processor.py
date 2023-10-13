from .models import Bank

def bank_clients_from_processor(request):
    bank = Bank.objects.all
    return {'bank': bank}