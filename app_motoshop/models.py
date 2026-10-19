from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Brand(models.Model):
    class Meta:
        verbose_name_plural = "Brand-uri"
    nume = models.CharField(max_length=100, unique=True, error_messages={"unique": "Brandul exista deja."})
    tara = models.CharField(max_length=100,null=True,blank=True,help_text="Tara de origine a brandului")
    activ = models.BooleanField(default=True)

class Categorie(models.Model):
    class Meta:
        ordering = ["ordine","nume"]
        verbose_name_plural = "Categorii"
    nume=models.CharField(max_length=200, unique=True)
    descriere=models.TextField(null=True,blank=True,help_text="descrierea produselor in categorie")
    culoare=models.CharField(max_length=7,default="#FFFFFF",help_text="codul HEX de culoare")
    sigla=models.CharField(max_length=255,null=True,blank=True,help_text="calea siglei categoriei")
    ordine=models.IntegerField(default=0,db_index=True,help_text="ordinea de afisare")
    
class Produs(models.Model):
    class Meta:
        ordering = ["nume"]
        verbose_name_plural = "Produse"
        constraints = [
            models.CheckConstraint(condition=models.Q(pret_baza__gt=0), name="pret_baza_pozitiv")
        ]

    GENURI = [("unisex", "Unisex"), ("femei", "Femei"), ("barbati", "Barbati")]
    TIPURI_UTILIZARE = [("urban", "Urban"), ("touring", "Touring"), ("sport", "Sport")]

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    nume = models.CharField(max_length=200, db_index=True, error_messages={"blank": "Numele este obligatoriu."})
    descriere = models.TextField(null=True, blank=True)
    gen = models.CharField(max_length=10, choices=GENURI)
    pret_baza = models.DecimalField(max_digits=10, decimal_places=2,db_index=True, help_text="Pretul inainte de reduceri.")
    material_principal = models.CharField(max_length=100, null=True, blank=True)
    tip_utilizare = models.CharField(max_length=20, choices=TIPURI_UTILIZARE)
    etichete = ArrayField(models.CharField(max_length=50), default=list, blank=True)
    creat_la = models.DateTimeField(auto_now_add=True)
    activ = models.BooleanField(default=True)
    
class Furnizor(models.Model):
    class Meta:
        verbose_name_plural = "Furnizori"
    nume = models.CharField(max_length=100)
    email = models.EmailField(unique=True, error_messages={"unique": "Acest email este deja folosit."})
    telefon = models.CharField(max_length=15, null=True, blank=True)
    tara = models.CharField(max_length=100, null=True, blank=True)
    activ = models.BooleanField(default=True)
    
class Discount(models.Model):
    class Meta:
        verbose_name_plural = "Discounturi"
        constraints = [
            models.CheckConstraint(condition=models.Q(procent__gte=0) & models.Q(procent__lte=100), name="procent_valid"),
            models.CheckConstraint(condition=models.Q(suma_fixa__gte=0) | models.Q(suma_fixa__isnull=True), name="suma_fixa_valida"),
            models.CheckConstraint(condition=models.Q(end_la__gte=models.F("start_la")), name="perioada_discount_valida")
        ]

    nume = models.CharField(max_length=100, error_messages={"blank": "Numele discountului este obligatoriu."})
    procent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    suma_fixa = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    start_la = models.DateField()
    end_la = models.DateField()
    activ = models.BooleanField(default=True)
    
class VariantaProdus(models.Model):
    class Meta:
        verbose_name_plural = "Variante produse"
        constraints = [
            models.CheckConstraint(condition=models.Q(pret__gt=0), name="pret_varianta_pozitiv"),
            models.CheckConstraint(condition=models.Q(stoc__gte=0), name="stoc_varianta_valid")
        ]

    produs = models.ForeignKey(Produs, on_delete=models.CASCADE)
    furnizor = models.ForeignKey(Furnizor, on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    cod_produs = models.CharField(max_length=100, unique=True,db_index=True, error_messages={"unique": "Codul produsului exista deja."})
    marime = models.CharField(max_length=20)
    culoare = models.CharField(max_length=50)
    pret = models.DecimalField(max_digits=10, decimal_places=2)
    stoc = models.IntegerField(default=0,db_index=True)
    greutate = models.IntegerField(null=True, blank=True)
    disponibil_de_la = models.DateField(null=True, blank=True)
    activ = models.BooleanField(default=True)
    
class ImagineProdus(models.Model):
    class Meta:
        verbose_name_plural = "Imagini produse"
        ordering = ["ordine"]

    produs = models.ForeignKey(Produs, on_delete=models.CASCADE)
    url = models.ImageField(upload_to="produse/")
    alt_text = models.CharField(max_length=200, null=True, blank=True)
    este_coperta = models.BooleanField(default=False)
    ordine = models.IntegerField(default=0)