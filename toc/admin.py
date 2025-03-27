from django.contrib import admin
from .models import CarouselItem
from .models import Services
from .models import *

# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)

#Caroussel 
@admin.register(CarouselItem)
class CarouselItemAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "description")
    list_filter = ("is_active",)
    
# Services
@admin.register(Services)
class Services(admin.ModelAdmin):
    """
    Configuration de l'administration pour le modèle Service
    """
    list_display = (
        'titre', 
        'categorie', 
        'prix', 
        'actif', 
        'created_at'
    )
    list_filter = (
        'categorie', 
        'actif'
    )
    search_fields = (
        'titre', 
        'description'
    )
    list_editable = ('actif',)
    readonly_fields = ('created_at', 'updated_at')