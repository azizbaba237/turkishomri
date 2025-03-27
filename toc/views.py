from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from .utils import cookieCart, cartData, guestOrder
from django.views.generic import ListView
from .models import CarouselItem
import datetime
import json
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django import forms


# Index for all like store 
def index(request):
    data = cartData(request)
    cartItems = data['cartItems']
    # order = data['order']
    # items = data['items']
    
    # Récupérer les items du carousel
    carousel_items = CarouselItem.objects.filter(is_active=True).order_by('order')
        
    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems, 'carousel_items':carousel_items}
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

#View for caroussel 
class HomeView(ListView):
    model = CarouselItem
    template_name = "home.html"
    context_object_name = "carousel_items"
    
    def get_queryset(self):
        return CarouselItem.objects.filter(is_active=True).order_by("order")
    

#Services View
def services(request):
    """
    Vue pour afficher tous les services actifs
    """
    # Récupère tous les services actifs, triés par catégorie
    services = Services.objects.filter(actif=True).order_by('categorie')
    context = {
        'services': services
    }
    
    return render(request, 'services.html', context)

# About view
def about(request):
    """
    Vue pour la page À Propos
    """
    context = {
        'title': 'À Propos de Nous',
    }
    return render(request, 'about.html', context)

# Contact
class ContactForm(forms.Form):
    """
    Formulaire de contact personnalisé
    """
    nom = forms.CharField(
        label='Votre Nom', 
        max_length=100, 
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-md',
            'placeholder': 'Votre nom complet'
        })
    )
    email = forms.EmailField(
        label='Votre Email', 
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-md',
            'placeholder': 'votre.email@exemple.com'
        })
    )
    sujet = forms.CharField(
        label='Sujet', 
        max_length=200, 
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border rounded-md',
            'placeholder': 'Objet de votre message'
        })
    )
    message = forms.CharField(
        label='Votre Message', 
        widget=forms.Textarea(attrs={
            'class': 'w-full px-3 py-2 border rounded-md h-32',
            'placeholder': 'Détaillez votre demande...'
        })
    )

def contact(request):
    """
    Vue pour la page de contact
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Récupération des données du formulaire
            nom = form.cleaned_data['nom']
            email = form.cleaned_data['email']
            sujet = form.cleaned_data['sujet']
            message = form.cleaned_data['message']

            # Composition du message complet
            message_complet = f"""
            Nouveau message de {nom} ({email})

            Sujet: {sujet}

            Message:
            {message}
            """

            try:
                # Envoi de l'email
                send_mail(
                    f'Contact Web - {sujet}',
                    message_complet,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
                messages.success(request, 'Votre message a été envoyé avec succès !')
                return redirect('contact')
            except Exception as e:
                messages.error(request, 'Une erreur est survenue. Veuillez réessayer.')

    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})