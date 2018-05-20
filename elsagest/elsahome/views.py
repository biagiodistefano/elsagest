from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.


def view(request):

    context = {
        "user": request.user,
        "app": "home",
        "sezione": request.user.userprofile.sezione
    }

    return render(request, 'elsahome/home.html', context)
