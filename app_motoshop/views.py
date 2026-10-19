from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
import locale
import re

locale.setlocale(locale.LC_TIME, "ro_RO.UTF-8")

# LAB1 : 4,5,6,7.clasa Accesare
class Accesare:
    cnt=0
    def __init__(self,ip_client,url,parametri={}):
        Accesare.cnt += 1
        self.id = Accesare.cnt
        self.ip_client=ip_client
        self.url = url
        self.data = datetime.now()
        self.parametri = parametri
        
    
    def lista_parametri(self):
        return [(key,val if val!="" else None) for key,val in self.parametri.items()]
        
    def string_url(self):
        return self.url
    
    def calculeaza_data(self, format="%A, %d %B %Y", val=""):
        if val == "zi":
            format = "%A, %d %B %Y"
        elif val == "timp":
            format = "%H:%M:%S"
        elif val != "":
            format = "%A, %d %B %Y %H:%M:%S"

        return self.data.strftime(format).title()
    
    def pagina(self):
        st = self.url.find("//")
        st = self.url.find("/", st+2)
        dr = self.url.find("?")
        if st == -1:
            return "/"
        elif dr == -1:
            return self.url[st:] 
        else:
            return self.url[st:dr]
        
    def __str__(self):
        return (
            f"id: {self.id}\n"
            f"ip_client: {self.ip_client}\n"
            f"string_url: {self.string_url()}\n"
            f"pagina: {self.pagina()}\n"
            f"calculeaza_data: {self.calculeaza_data()}\n"
            f"lista_parametri: {self.lista_parametri()}"
        )

accesari = []

# Create your views here.

def record_accesare(request):
    accesare = Accesare(request.ip, request.build_absolute_uri(), request.GET )
    accesari.append(accesare)
    print(accesare)
    return accesare

def index(request):
    record_accesare(request)
    return render(request, "index.html")

# LAB1 : ex 2,3 pag /info
def info(request):
    accesare = record_accesare(request)
    val = request.GET.get("data", "")
    context = {
        "data": accesare.calculeaza_data(val=val),
        "nr_parametri": len(request.GET),
        "parametri": request.GET.items()
    }
    return render(request, "info.html", context)

# LAB1: ex 6,10
# LAB2 : log
def log(request):
    record_accesare(request)
    str=""
    if "ultimele" in request.GET:
        n = request.GET.get('ultimele')
        try:
            n = int(n)
            for i in range(len(accesari)-1,max(len(accesari)-n-1,-1),-1):
                str+=f"<p> Acces {i}: {accesari[i].string_url()} {accesari[i].calculeaza_data("%A, %d %B %Y %H:%M:%S")}</p>"
            if len(accesari)<n:
                str+=f"<p> Exista doar {len(accesari)} accesari fata de {n} accesari cerute </p>"
        except ValueError:
            str+="Eroare: valoarea param -ultimele- nu este intreaga "
    if "iduri" not in request.GET and "ultimele" not in request.GET:
        for x in accesari:
            str += f"<p>{x}</p>"
    if "accesari" in request.GET:
        if request.GET.get('accesari') == "nr":
            str+=f"Nr. accesari: {len(accesari)}"
        if request.GET.get('accesari') == "detalii":
            str+="<ul>"
            for x in accesari:
                str+=f"<li>Acces {x.id}: {x.pagina()} - {x.calculeaza_data()}</li>"
            str+="</ul>"
    if "iduri" in request.GET:
        ids= request.GET.getlist('iduri')
        ids=",".join(ids)
        idlist = [int(x) for x in ids.split(",")]
        if "dubluri" not in request.GET or request.GET.get('dubluri').lower() == 'false':
            idlist = list(dict.fromkeys(idlist))
        for i in idlist:
            if i <= len(accesari):
                str+=f"<p> Acces {i}: {accesari[i-1].string_url()} {accesari[i-1].calculeaza_data()}</p>"
            else:
                str+=f"<p> Nu exista id-ul {i} </p>"
    if "tabel" in request.GET:
        val = request.GET.get("tabel")
        if val == "tot":
            col = ["id","ip_client","url","parametri","data"]
        else:
            col = val.split(",")
        str += "<table border='1'>"
        str += "<tr>"
        for c in col:
            str += f"<th>{c}</th>"
        str += "</tr>"
        for x in accesari:
            str += "<tr>"
            for c in col:
                if c == "parametri":
                    str += f"<td>{x.lista_parametri()}</td>"
                elif c == "data":
                    str += f"<td>{x.calculeaza_data()}</td>"
                else:
                    str += f"<td>{getattr(x, c)}</td>"
            str += "</tr>"
        str+="</table>"
        
    str += "<h2>Parametri</h2>"
    str += f"<p>Nr. parametri: {len(request.GET)}</p>"
    str += "<ul>"
    for p in request.GET:
        str += f"<li>{p}</li>"
    str += "</ul>"
    
    fr = {}

    for accesare in accesari:
        pagina= accesare.pagina()
        if pagina not in fr:
            fr[pagina]= 0
        fr[pagina]+= 1

    pagina_min = min(fr, key=fr.get)
    pagina_max = max(fr, key=fr.get)

    str += f"<p>Pagina cea mai putin accesata: {pagina_min}</p>"
    str += f"<p>Pagina cea mai mult accesata: {pagina_max}</p>"
    return render(request, "log.html", {"continut_log": str})

def despre(request):
    record_accesare(request)
    return render(request, "despre.html")
    
def istoric(request):
    record_accesare(request)
    return render(request, "in_lucru.html", {"pagina": "Istoric"})

def detalii_accesare(request, id):
    record_accesare(request)
    id = int(id)
    if id<=len(accesari):
        if accesari[id-1].id == id:
            return HttpResponse(
                f"<h1>Accesarea {id}</h1>"
                f"<pre>{accesari[id-1]}</pre>"
            )
    return HttpResponse("Accesarea nu exista")

def exemplu(request):
    return render(request,"exemplu.html",
        {
            "titlu_tab":"Titlu fereastra",
            "titlu_articol":"Titlu afisat",
            "continut_articol":"Continut text"
        }
    )

def exemplu2(request):
    return render(request,"exemplu2.html")

def produse(request):
    record_accesare(request)
    return render(request, "in_lucru.html", {"pagina": "Produse"})

def contact(request):
    record_accesare(request)
    return render(request, "in_lucru.html", {"pagina": "Contact"})

def cos_virtual(request):
    record_accesare(request)
    return render(request, "in_lucru.html", {"pagina": "Cos virtual"})