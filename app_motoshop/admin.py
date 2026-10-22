from django.contrib import admin
from .models import Brand, Categorie, Produs, Furnizor, Discount, VariantaProdus, ImagineProdus


class BrandAdmin(admin.ModelAdmin):
    list_display = ('nume','tara','activ')
    ordering = ['-nume','activ']
    list_filter=['activ']
    search_fields=['^nume']
    list_per_page=10
    
class ProduseAdmin(admin.ModelAdmin):
    list_display = ('nume','activ')
    ordering = ['nume','activ']
    list_filter=['activ']
    search_fields=['^nume']
    list_per_page=10
    
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nume','activ')
    ordering = ['nume','activ']
    list_filter=['activ']
    search_fields=['^nume']
    list_per_page=10
    
class FurnizorAdmin(admin.ModelAdmin):
    list_display = ('nume','activ')
    ordering = ['nume','activ']
    list_filter=['activ']
    search_fields=['^nume']
    list_per_page=10
    
admin.site.register(Brand,BrandAdmin)
admin.site.register(Categorie)
admin.site.register(Produs,ProduseAdmin)
admin.site.register(Furnizor)
admin.site.register(Discount)
admin.site.register(VariantaProdus)
admin.site.register(ImagineProdus)

admin.site.site_header = "Panou de Administrare MotoShop"
admin.site.site_title = "Admin Site"
admin.site.index_title = "Bine ai venit în panoul de administrare"
