from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


# Create your models here.

# Customer models 
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete= models.CASCADE)
    name = models.CharField(max_length=2000, null=True)
    email = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
    
# Product models 
class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=True)
    image  = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    #image handle
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    
# Order moderl 
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return str(self.id)
    
    #checks if we have any items that are not digital.
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems :
            if i.product.digital == False:
                shipping = True
        
        return shipping
    
    # Get cart total 
    @property
    def get_cart_total(self) :
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total 
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total 
    
    
    
# Order Items models 
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order   = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    # Calculate total 
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total 
    

# Shipping address models 
class ShippingAddress(models.Model):
    customer  = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order     = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address   = models.CharField(max_length=200, null=False)
    city      = models.CharField(max_length=200, null=False)
    state     = models.CharField(max_length=200, null=False)
    zipcode   = models.CharField(max_length=200, null=False)
    date_added   = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address
    
# Caroussel header 
class CarouselItem(models.Model):
    title = models.CharField(_("Titre"), max_length=200)
    description = models.TextField(_("Description"))
    image = models.ImageField(_("Image"), upload_to="carousel/")
    order = models.PositiveIntegerField(_("Ordre"), default=0)
    is_active = models.BooleanField(_("Actif"), default=True)
    
    class Meta:
        ordering = ["order"]
        verbose_name = _("Élément du carousel")
        verbose_name_plural = _("Éléments du carousel")
    
    def __str__(self):
        return self.title
    
# Pour la gestion des services 
class Service(models.Model):
    """
    Modèle pour gérer les services de l'entreprise
    """
    name = models.CharField(
        _('Nom du service'), 
        max_length=100, 
        unique=True
    )
    description = models.TextField(
        _('Description'), 
        blank=True, 
        null=True
    )
    icon = models.CharField(
        _('Icône'), 
        max_length=50, 
        blank=True, 
        null=True, 
        help_text=_('Nom de la classe d\'icône (ex: fas fa-tools)')
    )
    is_active = models.BooleanField(
        _('Actif'), 
        default=True
    )
    created_at = models.DateTimeField(
        _('Date de création'), 
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('Dernière mise à jour'), 
        auto_now=True
    )

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')
        ordering = ['name']

    def __str__(self):
        return self.name