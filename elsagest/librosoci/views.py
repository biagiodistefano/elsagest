from django.shortcuts import render
from django.http import JsonResponse
from graphql_relay.node.node import from_global_id
from .models import Socio, RinnovoIscrizione
from datetime import date, datetime, timedelta

# Create your views here.


def view(request):

    context = {
        "sezione": request.user.userprofile.sezione,
        "user": request.user
    }

    return render(request, 'librosoci/libro_soci.html', context)


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
        except Exception as e:
            print("Something went wrong!")
            #return JsonResponse({"success": False, "message": str(e)})
            raise


def modifica_socio(request):
    if request.method == "POST":
        try:
            post = request.POST
            print(post)
            socio_id = from_global_id(post.get("id"))[1]
            try:
                data_iscrizione = datetime.strptime(post.get("data_iscrizione"), "%d-%m-%Y").date()
            except:
                data_iscrizione = datetime.strptime(post.get("data_iscrizione"), "%Y-%m-%d").date()
            scadenza_iscrizione = data_iscrizione + timedelta(days=364)
            socio = Socio.objects.get(pk=socio_id)
            socio.nome = post.get("nome")
            socio.cognome = post.get("cognome")
            socio.codice_fiscale = post.get("codice_fiscale")
            socio.email = post.get("email")
            socio.numero_tessera = post.get("numero_tessera")
            socio.data_iscrizione = data_iscrizione
            socio.scadenza_iscrizione = scadenza_iscrizione
            data_nuovo_rinnovo = post.get("data_nuovo_rinnovo")
            quota_nuovo_rinnovo = post.get("quota_nuovo_rinnovo")

            if data_nuovo_rinnovo and not quota_nuovo_rinnovo:
                return JsonResponse({"success": False, "message": "Specificare la quota di rinnovo"})
            elif quota_nuovo_rinnovo and not data_nuovo_rinnovo:
                return JsonResponse({"success": False, "message": "Specificare la data di rinnovo"})
            elif quota_nuovo_rinnovo and data_nuovo_rinnovo:
                data_rinnovo = datetime.strptime(data_nuovo_rinnovo, "%d-%m-%Y").date()
                scadenza_iscrizione = data_rinnovo + timedelta(days=364)
                socio.scadenza_iscrizione = scadenza_iscrizione
                rinnovo = RinnovoIscrizione.objects.create(data_rinnovo=data_rinnovo, quota_rinnovo=quota_nuovo_rinnovo,
                                                           socio=socio)
                rinnovo.save()
            socio.save()
            return JsonResponse({"success": True, "message": "Modifiche salvate!"})
        except Exception as e:
            print("Something went wrong!")
            raise
            return JsonResponse({"success": False, "message": str(e)})

