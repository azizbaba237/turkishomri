from django.contrib import admin
from .models import CarouselItem
from .models import Service
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
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """
    Configuration de l'administration pour le modèle Service
    """
    list_display = ('name', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')