from django.shortcuts import render
from django.http import JsonResponse
from librosoci.models import SezioneElsa

# Create your views here.


def view(request):

    context = {
        "user": request.user,
        "app": "home",
        "sezione": request.user.userprofile.sezione,
        "sezioni": SezioneElsa.objects.exclude(nome="Nessuna")
    }

    return render(request, 'elsahome/home.html', context)
