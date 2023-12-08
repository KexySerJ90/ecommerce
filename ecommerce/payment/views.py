from django.shortcuts import render
from .models import ShippingAdress

# Create your views here.
def checkout(request):
    if request.user.is_authenticated:
        try:
            shipping_address=ShippingAdress.objects.get(user=request.user.id)
            context={'shipping':shipping_address}
            return render(request, 'payment/checkout.html', context=context)
        except:
            return render(request, 'payment/checkout.html')
    else:
        return render(request, 'payment/checkout.html')

def payment_success(request):
    return render(request,'payment/payment-success.html')


def payment_failed(request):
    return render(request,'payment/payment-failed.html')


def complete_order(request):
    pass