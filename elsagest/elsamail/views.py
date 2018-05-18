from django.shortcuts import render
from django.core.mail import send_mail, get_connection, send_mass_mail
from django.template.loader import render_to_string
from django.http import JsonResponse
from librosoci.models import Socio


# Create your views here.
def user_send_email(request):
    user = request.user
    emailcred = user.userprofile.emailcredentials
    if request.method == 'POST':
        post = request.POST
        tipo = post.get("tipo")
        connection = get_connection(
            host=emailcred.host,
            port=emailcred.port,
            username=emailcred.username,
            password=emailcred.password,
            use_tls=emailcred.tls)

        print(emailcred.username, emailcred.password, emailcred.host, emailcred.tls)
        print(connection)
        send_mail(
            "ciao",
            "prova",
            emailcred.username,
            ['biagiodistefano92@gmail.com'],
            fail_silently=False,
            connection=connection
        )
        return JsonResponse({"success": "true", "message": "Promemoria inviati correttamente"})

        # if tipo == "promemoria scadenza multipli":

        messaggi = []
        for socio in Socio.objects.in_scadenza().filter(sezione=user.userprofile.sezione):  # todo non inviare se già inviata nei 15 giorni precedenti
            oggetto = f"ELSA {user.userprofile.sezione.nome} | Promemoria scadenza iscrizione"
            corpo = render_to_string('elsamail/promemoria_scadenza_iscrizione.html', {"socio": socio})
            mittente = emailcred.username
            destinatari = [socio.email]

            send_mail(
                oggetto,
                corpo,
                emailcred.username,
                [socio.email],
                fail_silently=False,
                connection=connection
            )
            messaggi.append((oggetto, corpo, mittente, destinatari))

        messaggi = tuple(messaggi)
        #send_mass_mail(messaggi, fail_silently=False, connection=connection)
        print("OK!")
        return JsonResponse({"success": "true", "message": "Promemoria inviati correttamente"})
