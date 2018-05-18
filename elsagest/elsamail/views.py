from django.shortcuts import render
from django.core.mail import send_mail, get_connection, send_mass_mail
from django.template.loader import render_to_string
from django.http import JsonResponse
from librosoci.models import Socio, Reminder
from datetime import datetime


# Create your views here.
def user_send_email(request):
    user = request.user
    emailcred = user.userprofile.emailcredentials
    if request.method == 'POST':
        try:
            post = request.POST
            tipo = post.get("tipo")
            connection = get_connection(
                host=emailcred.host,
                port=emailcred.port,
                username=emailcred.username,
                password=emailcred.password,
                use_tls=emailcred.tls)

            messaggi = []
            reminder = Reminder.objects.create(mittente=user)

            for socio in Socio.objects.in_scadenza().filter(sezione=user.userprofile.sezione):  # todo non inviare se già inviata nei 15 giorni precedenti
                if not socio.promemoria_inviato:
                    reminder.destinatari.add(socio)
                    oggetto = f"ELSA {user.userprofile.sezione.nome} | Promemoria scadenza iscrizione"
                    stato_iscrizione = "è scaduta" if socio.scaduto else "scadrà"
                    context = {
                        "user": user,
                        "socio": socio,
                        "stato_iscrizione": stato_iscrizione,
                        "scadenza_iscrizione": datetime.strftime(socio.scadenza_iscrizione, f"%d/%m/%Y")
                    }
                    corpo = render_to_string('elsamail/promemoria_scadenza_iscrizione.html', context=context)
                    mittente = emailcred.username
                    destinatari = [socio.email]
                    messaggi.append((oggetto, corpo, mittente, destinatari))
            reminder.save()
            if len(messaggi):
                messaggi = tuple(messaggi)
                send_mass_mail(messaggi, fail_silently=False, connection=connection)
                message = f"{len(messaggi)} promemoria inviat{'o' if len(messaggi) > 1 else 'o'} correttamente!"
            else:
                message = f"Tutti i promemoria ai soci in scadenza sono già stati inviati da meno di 15 giorni!"
            return JsonResponse({"success": True, "message": message})
        except Exception as e:
            return JsonResponse({"success": False, "message": f"Si è verificato un errore: {e}"})
