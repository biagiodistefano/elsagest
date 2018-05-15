from django.shortcuts import render

# Create your views here.


def view(request):

    context = {
        "user": request.user
    }

    return render(request, 'librosoci/libro_soci.html', context)
