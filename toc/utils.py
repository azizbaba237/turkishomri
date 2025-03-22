import json 
from .models import *

def cookieCart(request):
    #Create empty cart for now for non-logged in user
	try:
		cart = json.loads(request.COOKIES['cart'])
	except:
		cart = {}
		print('CART:', cart)

	items = []
	order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
	cartItems = order['get_cart_items']

	for i in cart:
		#We use try block to prevent items in cart that may have been removed from causing error
		try:
			cartItems += cart[i]['quantity']

			product = Product.objects.get(id=i)
			total = (product.price * cart[i]['quantity'])

			order['get_cart_total'] += total
			order['get_cart_items'] += cart[i]['quantity']

			item = {
				'id':product.id,
				'product':{'id':product.id,'name':product.name, 'price':product.price, 
				'imageURL':product.imageURL}, 'quantity':cart[i]['quantity'],
				'digital':product.digital,'get_total':total,
				}
			items.append(item)

			if product.digital == False:
				order['shipping'] = True
		except:
			pass
			
	return {'cartItems':cartItems ,'order':order, 'items':items}
    
def cartData(request):
     # Check if authenticated, if not create 
    if request.user.is_authenticated :
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else :
        cookidata = cookieCart( request)
        cartItems = cookidata['cartItems']
        order = cookidata['order']
        items = cookidata['items']
        print("Cookie Data:", cookidata)  # Log pour vérifier les données
        
    return {'items':items, 'order':order, 'cartItems':cartItems}

def guestOrder(request, data):
    name = data['form']['name']
    email = data['form']['email']
        
    cookieData = cookieCart(request)
    items      = cookieData['items']
        
    # Create an order and set the value to the customer variable
    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()
        
    order = Order.objects.create(customer=customer, complete=False)
        
    # loop through our cart items replica list and create real OrderItems by querying the product and setting the nessesary attributes.
    for item in items:
        product = Product.objects.get(id=item['id'])
        orderItem = Order.objects.create(product=product, order=order, quantity=item['quantity'])
    
    return customer, order 