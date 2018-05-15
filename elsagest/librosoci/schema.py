import graphene
from graphene_django.filter.fields import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from .models import Socio, SezioneElsa, RinnovoIscrizione
from datetime import date, timedelta


class SocioType(DjangoObjectType):
    class Meta:
        model = Socio
        filter_fields = {
            "nome": ["icontains"],
            "cognome": ["icontains"],
            "email": ["icontains"]
        }
        interfaces = (graphene.Node, )


class RinnovoIscrizioneType(DjangoObjectType):
    class Meta:
        model = RinnovoIscrizione
        interfaces = (graphene.Node, )


class SezioneElsaType(DjangoObjectType):
    class Meta:
        model = SezioneElsa
        filter_fields = {
            "citta": ["icontains"]
        }

        interfaces = (graphene.Node, )


class Query(graphene.ObjectType):
    all_soci = DjangoFilterConnectionField(SocioType, scadenza=graphene.String())

    def resolve_all_soci(self, context, **kwargs):
        if kwargs.get("scadenza"):
            return Socio.objects.filter(scadenza_iscrizione__lte=date.today() + timedelta(days=15)).order_by('scadenza_iscrizione')
        return Socio.objects.all()
