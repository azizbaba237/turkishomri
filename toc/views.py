from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .utils import cookieCart, cartData, guestOrder
import datetime
import json


# Index for all like store 
def index(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
        
    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'index.html', context)




#  Cart view 
def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    # Log pour vérifier les données
    print("Order:", order)
    print("Items:", items)
    print("Cart Items:", cartItems)
        
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'cart.html', context)


# Checkout view 
def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
        
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'checkout.html', context)


# Update items 
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action  = data['action']
    print('action', action)
    print('productid', productId)
    
    # Vérifier si l'utilisateur est authentifié avant d'accéder à `customer`
    if request.user.is_authenticated:
        customer = request.user.customer
    else:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
        
        
    return JsonResponse('item was added', safe=False)


# Viw for POST request to send data too.
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.load(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer 
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
    
    else:
        customer, order = guestOrder(request, data)
            
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
        
    # to make sure that the total sent matches what the cart total is actually supposed to be.
    if total == order.get_cart_total:
        order.complete = True
    order.save()
    
    #create an instance of the shipping address if an address was sent.
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order    = order,
            address  = data['shipping']['address'],
            city     = data['shipping']['city'],
            state    = data['shipping']['state'],
            zipcode  = data['shipping']['zipcode'],
        )
    
    return JsonResponse('Payement subimted', safe=False)