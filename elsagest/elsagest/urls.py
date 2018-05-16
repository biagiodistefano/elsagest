"""elsagest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
import elsahome.views as home_views
import elsausers.views as users_views
import librosoci.views as librosoci_views
from graphene_django.views import GraphQLView
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='home/', permanent=False)),
    path('home/', home_views.view, name='home'),
    path('librosoci/', librosoci_views.view, name='libro_soci'),
    path('librosoci/aggiungisocio/', librosoci_views.aggiungi_socio, name="aggiungi_socio"),
    path('graphql/', GraphQLView.as_view(graphiql=True)),
    path('login/', auth_views.login, {'template_name': 'elsausers/login.html'}, name='login'),
    path('logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
    path('password/', users_views.change_password, name='change_password'),
]
