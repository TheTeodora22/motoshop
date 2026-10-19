from django.contrib import admin
from .models import Brand, Categorie, Produs, Furnizor, Discount, VariantaProdus, ImagineProdus

admin.site.register(Brand)
admin.site.register(Categorie)
admin.site.register(Produs)
admin.site.register(Furnizor)
admin.site.register(Discount)
admin.site.register(VariantaProdus)
admin.site.register(ImagineProdus)