import graphene
from graphene_django.filter.fields import DjangoFilterConnectionField
from graphql_relay.node.node import from_global_id
from graphene_django.types import DjangoObjectType
from .models import Socio, SezioneElsa, RinnovoIscrizione, Consigliere, EmailConsigliere
from datetime import date, timedelta
from django.db.models import Q


consiglieri_locali = list(range(1, 14))
consiglieri_nazionali = list(range(14, 27))


class SocioType(DjangoObjectType):

    promemoria_inviato = graphene.Boolean()

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
        elsa_italia = user.userprofile.sezione.nome == "Italia"
        order_by = kwargs.get("orderby", "cognome")
        filtri = Q()
        if not user.is_superuser:
            if not elsa_italia:
                filtri &= Q(sezione=user.userprofile.sezione)
            if kwargs.get("scadenza"):
                order_by = "scadenza_iscrizione"
                filtri &= Q(scadenza_iscrizione__lte=date.today() + timedelta(days=15))

            elif kwargs.get("consiglieri"):
                order_by = "ruolo_id"
                if elsa_italia:
                    if kwargs.get("sezione"):
                        filtri &= Q(sezione_id=int(kwargs.get("sezione"))) & Q(ruolo_id__in=consiglieri_locali)
                    else:
                        filtri &= Q(ruolo_id__in=consiglieri_nazionali)
                else:
                    filtri &= Q(sezione=user.userprofile.sezione) & Q(ruolo_id__in=consiglieri_locali)

            return Socio.objects.filter(filtri).order_by(order_by)
        else:
            if kwargs.get("scadenza"):
                order_by = "scadenza_iscrizione"
                filtri &= Q(scadenza_iscrizione__lte=date.today() + timedelta(days=15))
            if kwargs.get("sezione"):
                filtri &= Q(sezione_id=int(kwargs.get("sezione")))
            if kwargs.get("consiglieri"):
                filtri &= Q(ruolo_id__in=consiglieri_locali + consiglieri_nazionali)
            return Socio.objects.filter(filtri).order_by(order_by)

    def resolve_socio(self, context, **kwargs):
        user = context.context.user
        _id = from_global_id(kwargs.get("id"))[1]
        return Socio.objects.filter(sezione=user.userprofile.sezione).get(pk=_id)
