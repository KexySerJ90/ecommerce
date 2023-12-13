from decimal import Decimal

import stripe
from django import forms
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ShippingForm
from .models import ShippingAdress, Order, OrderItem
from cart.cart import Cart
from django.core.mail import send_mail

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


# Create your views here.
def checkout(request):
    if request.user.is_authenticated:
        try:
            shipping_address = ShippingAdress.objects.get(user=request.user)
            form = ShippingForm(instance=shipping_address)
            context = {'form': form}
            return render(request, 'payment/checkout.html', context=context)
        except ShippingAdress.DoesNotExist:
            form = ShippingForm()
            context = {'form': form}
            return render(request, 'payment/checkout.html', context=context)
    else:
        form = ShippingForm()
        context = {'form': form}
        return render(request, 'payment/checkout.html', context=context)


def payment_success(request):
    for key in list(request.session.keys()):
        if key == 'session_key':
            del request.session[key]
    return render(request, 'payment/payment-success.html')


def payment_failed(request):
    return render(request, 'payment/payment-failed.html')


def complete_order(request):
    if request.method == 'POST':
        product_list = []
        form = ShippingForm(request.POST)
        payment_type = request.POST.get('stripe-payment')
        cart = Cart(request)
        total_cost = cart.get_total()
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            address1 = form.cleaned_data['address1']
            address2 = form.cleaned_data['address2']
            city = form.cleaned_data['city']
            state = str(form.cleaned_data['state'])
            zipcode = str(form.cleaned_data['zipcode'])
            shipping_address = (address1 + '\n' + address2 + '\n' + city + '\n' + state + '\n' + zipcode)
            match payment_type:
                case 'stripe-payment':
                    session_data = {
                        'mode': 'payment',
                        'success_url': request.build_absolute_uri(reverse('payment-success')),
                        'cancel_url': request.build_absolute_uri(reverse('payment-failed')),
                        'line_items': []
                    }

                    if request.user.is_authenticated:
                        order = Order.objects.create(full_name=full_name, email=email,
                                                     shipping_address=shipping_address,
                                                     amount_paid=total_cost, user=request.user)
                        order_id = order.id

                        for item in cart:
                            OrderItem.objects.create(order_id=order_id, product=item['product'], quantity=item['qty'],
                                                     price=item['price'], user=request.user)
                            session_data['line_items'].append({
                                'price_data': {
                                    'unit_amount': int(item['price'] * Decimal(100)),
                                    'currency': 'usd',
                                    'product_data': {
                                        'name': item['product']
                                    },
                                },
                                'quantity': item['qty'],
                            })
                            product_list.append(item['product'])
                        session_data['client_reference_id'] = order.id
                        session = stripe.checkout.Session.create(**session_data)
                        send_mail('Order revieved',
                                  'Hi' + str(full_name)+'\n\n' + 'Thank you for order' + '\n\n' + 'Please see you later' + '\n\n' + str(
                                      product_list) + '\n\n' + 'Total paid:$' + str(cart.get_total()),
                                  settings.EMAIL_HOST_USER, [email], fail_silently=False,)
                        return redirect(session.url, code=303)

                    else:
                        order = Order.objects.create(full_name=full_name, email=email,
                                                     shipping_address=shipping_address,
                                                     amount_paid=total_cost)
                        order_id = order.pk
                        for item in cart:
                            OrderItem.objects.create(order_id=order_id, product=item['product'], quantity=item['qty'],
                                                     price=item['price'])
                            session_data['line_items'].append({
                                'price_data': {
                                    'unit_amount': int(item['price'] * Decimal(100)),
                                    'currency': 'usd',
                                    'product_data': {
                                        'name': item['product']
                                    },
                                },
                                'quantity': item['qty'],
                            })
                            product_list.append(item['product'])
                        session_data['client_reference_id'] = order.id
                        session = stripe.checkout.Session.create(**session_data)
                        send_mail('Order revieved',
                                  'Hi' + '\n\n' + 'Thank you for order' + '\n\n' + 'Please see you later' + '\n\n' + str(
                                      product_list) + '\n\n' + 'Total paid:$' + str(cart.get_total()),
                                  settings.EMAIL_HOST_USER, [email], fail_silently=False, )
                        return redirect(session.url, code=303)
