import graphene
from graphene_django.filter.fields import DjangoFilterConnectionField
from graphql_relay.node.node import from_global_id
from graphene_django.types import DjangoObjectType
from .models import Socio, SezioneElsa, RinnovoIscrizione, ModificheSoci, Consigliere, EmailConsigliere
from datetime import date, timedelta


class SocioType(DjangoObjectType):
    class Meta:
        model = Socio
        filter_fields = {
            "id": ["exact"],
            "nome": ["icontains"],
            "cognome": ["icontains"],
            "email": ["icontains"]
        }
        interfaces = (graphene.Node, )


class RinnovoIscrizioneType(DjangoObjectType):
    class Meta:
        model = RinnovoIscrizione
        interfaces = (graphene.Node, )


class EmailConsigliereType(DjangoObjectType):
    class Meta:
        model = EmailConsigliere
        interfaces = (graphene.Node, )


class ConsigliereType(DjangoObjectType):
    class Meta:
        model = Consigliere
        filter_fields = {
            "ruolo": ["icontains"]
        }
        interfaces = (graphene.Node, )


class ModificheSociType(DjangoObjectType):
    class Meta:
        model = ModificheSoci
        interfaces = (graphene.Node, )


class SezioneElsaType(DjangoObjectType):
    class Meta:
        model = SezioneElsa
        filter_fields = {
            "citta": ["icontains"]
        }
        interfaces = (graphene.Node, )


class Query(graphene.ObjectType):
    socio = graphene.Field(SocioType, id=graphene.ID())
    all_soci = DjangoFilterConnectionField(SocioType, scadenza=graphene.Boolean(), orderby=graphene.String(), consiglieri=graphene.Boolean())

    def resolve_all_soci(self, context, **kwargs):
        user = context.context.user
        order_by = kwargs.get("orderby", "cognome")
        if kwargs.get("scadenza"):
            return Socio.objects.filter(scadenza_iscrizione__lte=date.today() + timedelta(days=15)).filter(sezione=user.userprofile.sezione).order_by('scadenza_iscrizione')
        elif kwargs.get("consiglieri"):
            return Socio.objects.filter(sezione=user.userprofile.sezione).filter(ruolo_id__gte=1).order_by('ruolo_id')

        return Socio.objects.filter(sezione=user.userprofile.sezione).order_by(order_by)

    def resolve_socio(self, context, **kwargs):
        user = context.context.user
        _id = from_global_id(kwargs.get("id"))[1]
        print(_id)
        return Socio.objects.get(pk=_id)
