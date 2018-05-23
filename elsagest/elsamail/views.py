from django.shortcuts import render
from django.core.mail import send_mail, get_connection, send_mass_mail
from django.template.loader import render_to_string
from django.http import JsonResponse
from librosoci.models import Socio, Reminder, SezioneElsa, Ruolo, Consigliere
from .models import UnsubscribeToken, BozzaEmail, Email
from datetime import datetime
from django.db.models import Q
from graphql_relay.node.node import from_global_id
from django.core.mail import get_connection, EmailMultiAlternatives
from bs4 import BeautifulSoup as bs
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings


# thanks to https://stackoverflow.com/a/10215091/3782345
def send_mass_html_mail(datatuple, fail_silently=False, user=None, password=None,
                        connection=None):
    """
    Given a datatuple of (subject, text_content, html_content, from_email,
    recipient_list), sends each message to each recipient list. Returns the
    number of emails sent.

    If from_email is None, the DEFAULT_FROM_EMAIL setting is used.
    If auth_user and auth_password are set, they're used to log in.
    If auth_user is None, the EMAIL_HOST_USER setting is used.
    If auth_password is None, the EMAIL_HOST_PASSWORD setting is used.

    """
    connection = connection or get_connection(
        username=user, password=password, fail_silently=fail_silently)
    messages = []
    for subject, text, html, from_email, recipient in datatuple:
        message = EmailMultiAlternatives(subject, text, from_email, recipient)
        message.attach_alternative(html, 'text/html')
        messages.append(message)
    return connection.send_messages(messages)


# Create your views here.
def promemoria_scadenza(request):
    user = request.user
    if request.method == 'POST':
        try:
            post = request.POST
            if not settings.DRY_EMAILS:
                try:
                    emailcred = user.userprofile.emailcredentials
                except Exception as e:
                    return JsonResponse(
                        {"success": False, "message": "Non hai aggiunto la tua email nelle impostazioni!"})
                connection = get_connection(
                    host=emailcred.host,
                    port=emailcred.port,
                    username=emailcred.username,
                    password=emailcred.password,
                    use_tls=emailcred.tls)
                mittente = emailcred.username
            else:
                mittente = "noreply@elsagest.org"

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
                    corpo = render_to_string('elsamail/modelli/promemoria_scadenza_iscrizione.html', context=context)

                    destinatari = [socio.email]
                    messaggi.append((oggetto, corpo, mittente, destinatari))
            reminder.save()
            if len(messaggi):
                messaggi = tuple(messaggi)
                if not settings.DRY_EMAILS:
                    send_mass_mail(messaggi, fail_silently=False, connection=connection)
                message = f"{len(messaggi)} promemoria inviat{'o' if len(messaggi) > 1 else 'o'} correttamente!"
            else:
                message = f"Tutti i promemoria ai soci in scadenza sono già stati inviati da meno di 15 giorni!"
            return JsonResponse({"success": True, "message": message})
        except Exception as e:
            return JsonResponse({"success": False, "message": f"Si è verificato un errore: {e}"})


def componi_email(request):
    user = request.user
    sezioni = SezioneElsa.objects.exclude(nome="Nessuna")
    sezione = user.userprofile.sezione
    ruoli = Ruolo.objects.filter(id__gte=14)
    context = {
        "sezioni": sezioni,
        "sezione": sezione,
        "ruoli": ruoli,
        "user": user
    }
    return render(request, 'elsamail/componi_email.html', context=context)


id_directors = list(range(8, 14)) + list(range(21, 27))


def invia_email(request):
    user = request.user
    sezione = user.userprofile.sezione
    if request.method == "POST":
        try:
            post = request.POST
            html = post.get("email_body")
            if html.strip() == "":
                return JsonResponse({"success": False, "message": "Non puoi inviare email vuote!"})
            if not settings.DRY_EMAILS:
                try:
                    emailcred = user.userprofile.emailcredentials
                except Exception as e:
                    return JsonResponse({"success": False, "message": "Non hai aggiunto la tua email nelle impostazioni!"})
                connection = get_connection(
                    host=emailcred.host,
                    port=emailcred.port,
                    username=emailcred.username,
                    password=emailcred.password,
                    use_tls=emailcred.tls)
                mittente = emailcred.username
            else:
                mittente = 'elsagest@gmail.com'
            soci_destinatari = int(post.get("soci_destinatari"))
            consigli_destinatari = int(post.get("consigli_destinatari"))
            consiglieri_destinatari = int(post.get("consiglieri_destinatari"))
            includi_directors = post.get("includi_directors")
            oggetto = post.get("oggetto")
            html = post.get("email_body")
            soup = bs(html, "html.parser")
            text = soup.get_text(separator="\n")
            current_site = get_current_site(request)
            protocol = request.scheme
            print(post)

            if soci_destinatari == consiglieri_destinatari == consigli_destinatari == 0:
                return JsonResponse({"success": False, "message": f"Seleziona almeno un destinatario!"})

            if sezione.nome != "Italia" and soci_destinatari and soci_destinatari != sezione.id:
                return JsonResponse({"success": False, "message": f"Non hai i permessi sufficienti per scrivere a soci diversi dalla tua sezione locale"})

            messaggi = []

            filtri_soci = Q(subscribed=True)
            if soci_destinatari == 0:
                filtri_soci &= Q(sezione_id=9999)
            elif soci_destinatari != 1000:
                filtri_soci &= Q(sezione_id=soci_destinatari)

            filtri_consiglieri = Q()
            if consigli_destinatari == 0 and not consiglieri_destinatari:
                filtri_consiglieri &= Q(sezione_id=9999)
            elif consigli_destinatari != 1000 and not consiglieri_destinatari:
                filtri_consiglieri &= Q(sezione_id=consigli_destinatari)

            if consigli_destinatari and not consiglieri_destinatari:
                if not includi_directors:
                    filtri_consiglieri &= ~Q(ruolo_id__in=id_directors)

            lista_consiglieri = []
            if consiglieri_destinatari == 14:
                lista_consiglieri = [1, 14]
            elif consiglieri_destinatari:
                lista_consiglieri = [consiglieri_destinatari, consiglieri_destinatari - 13]
                if includi_directors:
                    lista_consiglieri += [consiglieri_destinatari + 6, consiglieri_destinatari - 7]

            if lista_consiglieri:
                filtri_consiglieri |= Q(ruolo_id__in=lista_consiglieri)

            for socio in Socio.objects.filter(filtri_soci):  # todo non inviare se già inviata nei 15 giorni precedenti
                destinatari = [socio.email]
                unsubscribe_token = socio.unsubscribetoken.token
                unsubscribe_link = f"{protocol}://{current_site}/elsamail/unsubscribe/?token={unsubscribe_token}"
                unsubscribe_msg = f"""<p>Se non vuoi più ricevere queste emeail <a target="_blank" href="{unsubscribe_link}">clicca qui</a>"""
                messaggi.append((oggetto, text, html + unsubscribe_msg, mittente, destinatari))

            for consigliere in Consigliere.objects.filter(filtri_consiglieri):  # todo non inviare se già inviata nei 15 giorni precedenti
                destinatari = [consigliere.email]
                messaggi.append((oggetto, text, html, mittente, destinatari))

            for messaggio in messaggi:
                print(messaggio[-1][0])

            if not settings.DRY_EMAILS:
                send_mass_html_mail(messaggi, fail_silently=False, connection=connection)
            email = Email.objects.create(oggetto=oggetto, corpo=html, mittente=user)
            email.save()
            return JsonResponse({"success": True, "message": "Email inviata correttamente!"})
        except Exception as e:
            return JsonResponse({"success": False, "message": f"Si è verificato un errore {e}"})


def salva_bozza(request):
    user = request.user
    if request.method == "POST":
        try:
            post = request.POST
            oggetto = post.get("oggetto")
            corpo = post.get("corpo")
            disponibile_per = post.get("disponibilePer")
            print(oggetto, corpo, disponibile_per)

            bozza = BozzaEmail.objects.create(user=user, oggetto=oggetto, corpo=corpo, disponibile_per=disponibile_per)
            bozza.save()
            return JsonResponse({"success": True, "message": f"Bozza salvata"})

        except Exception as e:
            return JsonResponse({"success": False, "message": f"Si è verificato un errore {e}"})


def elimina_bozza(request):
    user = request.user
    if request.method == "POST":
        try:
            post = request.POST
            bozza_id = post.get("id")
            try:
                bozza_id = int(bozza_id)
            except ValueError:
                bozza_id = from_global_id(bozza_id)[1]

            bozza = BozzaEmail.objects.get(id=bozza_id)
            if bozza.user == user:
                bozza.delete()
                return JsonResponse({"success": True, "message": f"Bozza cancellata"})
            else:
                JsonResponse({"success": False, "message": f"Non hai i permessi per canellare questa bozza"})

        except Exception as e:
            return JsonResponse({"success": False, "message": f"Si è verificato un errore {e}"})


def unsubscribe(request):
    if request.method == "GET":
        token = request.GET.get('token')
        if token:
            try:
                ut = UnsubscribeToken.objects.get(token=token)
                ut.socio.unsubscribe()
                return render(request, 'elsamail/unsubscribe_success.html')
            except:
                return render(request, '404.html')
    return render(request, '404.html')
