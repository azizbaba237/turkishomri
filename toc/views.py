from django.shortcuts import render
from .models import *


# Index for all like store 
def index(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'index.html', context)




#  Cart view 
def cart(request):
    
    # Check if authenticated, if not create 
    if request.user.is_authenticated :
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else :
        # Create Empty cart for now for none-logged in users
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        
    context = {'items':items, 'order':order}
    return render(request, 'cart.html', context)




# Checkout view 
def checkout(request):
    context = {}
    return render(request, 'checkout.html', context)