from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.


def view(request):

    context = {
        "user": request.user
    }

    return render(request, 'elsahome/home.html', context)