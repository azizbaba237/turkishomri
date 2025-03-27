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
from django.db import models
from django.utils.translation import gettext_lazy as _

class Services(models.Model):
    """
    Modèle pour les services de l'entreprise
    """
    CATEGORIES = [
        ('sanitaire', _('Produits Sanitaires')),
        ('electricite', _('Électricité')),
        ('vitrerie', _('Vitre et Miroir')),
        ('suivi_chantier', _('Suivi de Chantier')),
    ]

    titre = models.CharField(
        _('Titre du service'), 
        max_length=200, 
        help_text=_('Nom descriptif du service')
    )
    description = models.TextField(
        _('Description'), 
        help_text=_('Description détaillée du service')
    )
    categorie = models.CharField(
        _('Catégorie'), 
        max_length=50, 
        choices=CATEGORIES,
        help_text=_('Catégorie à laquelle appartient le service')
    )
    prix = models.DecimalField(
        _('Prix'), 
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text=_('Prix du service (optionnel)')
    )
    actif = models.BooleanField(
        _('Service actif'), 
        default=True,
        help_text=_('Indique si le service est actuellement proposé')
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
        ordering = ['titre']

    def __str__(self):
        return f"{self.titre} ({self.get_categorie_display()})"