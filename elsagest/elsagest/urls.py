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
import elsamail.views as email_views
from graphene_django.views import GraphQLView
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from django.urls import include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='home/', permanent=False)),
    path('home/', home_views.view, name='home'),
    path('librosoci/', librosoci_views.view, name='libro_soci'),
    path('librosoci/aggiungisocio/', librosoci_views.aggiungi_socio, name="aggiungi_socio"),
    path('librosoci/modificasocio/', librosoci_views.modifica_socio, name="modifica_socio"),
    path('librosoci/modificaconsiglio/', librosoci_views.modifica_consiglio, name="modifica_consiglio"),
    path('graphql/', GraphQLView.as_view(graphiql=True)),
    path('login/', auth_views.login, {'template_name': 'elsausers/login.html'}, name='login'),
    path('logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
    path('', include('django.contrib.auth.urls')),
    path('password/', users_views.change_password, name='change_password'),
    path('impostazioni/', users_views.settings_view, name='impostazioni'),
    path('impostazioni/utente/', users_views.impostazioni_utente, name='impostazioni_utente'),
    path('impostazioni/sezione/nuovo-utente', users_views.nuovo_utente, name='impostazioni_aggiungi_utente'),
    path('librosoci/popola', librosoci_views.popola_db, name='popola_db'),
    path('elsamail/invia_promemoria', email_views.promemoria_scadenza, name='promemoria_scadenza'),
    path('elsamail/componi', email_views.componi_email, name='componi_email'),
    path('elsamail/invia', email_views.invia_email, name='send_email'),
    path('elsamail/unsubscribe/', email_views.unsubscribe, name='unsubscribe'),
    path('elsamail/salva-bozza/', email_views.salva_bozza, name='salva_bozza'),
    path('elsamail/elimina-bozza/', email_views.elimina_bozza, name='elimina_bozza')
]


# url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
# url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
# url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
# url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
