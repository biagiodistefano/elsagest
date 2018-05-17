from django.shortcuts import render
from django.http import JsonResponse
from graphql_relay.node.node import from_global_id
from .models import Socio
from datetime import date, datetime, timedelta

# Create your views here.


def view(request):

    context = {
        "sezione": request.user.userprofile.sezione
    }

    return render(request, 'librosoci/libro_soci.html')


def aggiungi_socio(request):
    if request.method == "POST":
        try:
            post = request.POST
            print(post)
            data_iscrizione = datetime.strptime(post.get("data_iscrizione"), "%d-%m-%Y").date()
            scadenza_iscrizione = data_iscrizione + timedelta(days=364)
            socio = Socio.objects.create(
                nome=post.get("nome"),
                cognome=post.get("cognome"),
                codice_fiscale=post.get("codice_fiscale"),
                email=post.get("email"),
                numero_tessera=post.get("numero_tessera"),
                data_iscrizione=data_iscrizione,
                scadenza_iscrizione=scadenza_iscrizione,
                ruolo_id=14,
                sezione=request.user.userprofile.sezione
            )
            socio.save()
            print("Everything ok!")
            return JsonResponse({"success": True})
        except:
            print("Something went wrong!")
            #return JsonResponse({"success": False})
            raise


def modifica_socio(request):
    if request.method == "POST":
        return None
        try:
            post = request.POST
            print(post)
            data_iscrizione = datetime.strptime(post.get("data_iscrizione"), "%d-%m-%Y").date()
            scadenza_iscrizione = data_iscrizione + timedelta(days=364)
            socio = Socio.objects.create(
                nome=post.get("nome"),
                cognome=post.get("cognome"),
                codice_fiscale=post.get("codice_fiscale"),
                email=post.get("email"),
                numero_tessera=post.get("numero_tessera"),
                data_iscrizione=data_iscrizione,
                scadenza_iscrizione=scadenza_iscrizione,
                ruolo_id=14,
                sezione=request.user.userprofile.sezione
            )
            socio.save()
            print("Everything ok!")
            return JsonResponse({"success": True})
        except:
            print("Something went wrong!")
            #return JsonResponse({"success": False})
            raise
