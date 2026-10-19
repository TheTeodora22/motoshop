from django.urls import path, re_path
from . import views
urlpatterns = [
    path("",views.index,name="index"),
    path("info",views.info,name="info"),
    path("log",views.log,name="log"),
    re_path(r'^accesare(?P<id>\d+)/$',views.detalii_accesare,name="detalii_accesare"),
    path("exemplu",views.exemplu,name="exemplu"),
    path("exemplu2",views.exemplu2,name="exemplu2"),
    path("despre", views.despre, name="despre"),
    path("istoric", views.istoric, name="istoric"),
    path("produse", views.produse, name="produse"),
    path("contact", views.contact, name="contact"),
    path("cos_virtual", views.cos_virtual, name="cos_virtual"),
]
