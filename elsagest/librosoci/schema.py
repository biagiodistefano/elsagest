import graphene
from graphene_django.filter.fields import DjangoFilterConnectionField
from graphql_relay.node.node import from_global_id
from graphene_django.types import DjangoObjectType
from .models import Socio, SezioneElsa, RinnovoIscrizione, Ruolo, EmailConsigliere, RuoliSoci
from datetime import date, timedelta
from django.db.models import Q


class SocioType(DjangoObjectType):

    promemoria_inviato = graphene.Boolean()
    iscritto_il = graphene.String()
    scade_il = graphene.String()
    rinnovato_il = graphene.String()
    in_carica_dal = graphene.String()

    class Meta:
        model = Socio
        filter_fields = {
            "id": ["exact"],
            "nome": ["icontains"],
            "cognome": ["icontains"],
            "email": ["icontains"],
            "sezione_id": ["exact"]
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
        model = Ruolo
        filter_fields = {
            "ruolo": ["icontains"]
        }
        interfaces = (graphene.Node, )


class RuoliSociType(DjangoObjectType):

    in_carica_dal = graphene.String()

    class Meta:
        model = RuoliSoci
        filter_fields = {
            "ruolo": ["exact"],
            "socio": ["exact"]
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
    socio = graphene.Field(SocioType, id=graphene.ID(), sezione=graphene.String())
    all_soci = DjangoFilterConnectionField(SocioType, sezione=graphene.String(), scadenza=graphene.Boolean(), orderby=graphene.String(), consiglieri=graphene.Boolean(), search=graphene.String())
    consiglieri = graphene.List(RuoliSociType, sezione=graphene.String(), nazionali=graphene.Boolean())

    def resolve_all_soci(self, context, **kwargs):

        user = context.context.user
        elsa_italia = user.userprofile.sezione.nome == "Italia"
        order_by = kwargs.get("orderby", "cognome")
        sezione_id = kwargs.get("sezione")
        search = kwargs.get("search")
        if sezione_id:
            try:
                sezione_id = int(sezione_id)
            except ValueError:
                sezione_id = from_global_id(sezione_id)[1]
        filtri = Q()

        if search:
            search_filter = Q()
            for kw in search.split():
                print(kw)
                search_filter |= Q(nome__istartswith=kw) | Q(cognome__istartswith=kw)
            filtri &= search_filter

        if not user.is_superuser:
            if not elsa_italia:
                filtri &= Q(sezione=user.userprofile.sezione)
            if kwargs.get("scadenza"):
                order_by = "scadenza_iscrizione"
                filtri &= Q(scadenza_iscrizione__lte=date.today() + timedelta(days=15))

            elif kwargs.get("consiglieri"):
                order_by = "ruolo_socio__id"
                if elsa_italia:
                    if sezione_id:
                        filtri &= Q(sezione_id=sezione_id) & Q(ruolo_socio__in=Ruolo.objects.filter(id__gte=14))
                    else:
                        filtri &= Q(ruolo_socio__in=Ruolo.objects.filter(id__lte=13))
                else:
                    filtri &= Q(sezione=user.userprofile.sezione)

            return Socio.objects.filter(filtri).order_by(order_by)
        else:
            if kwargs.get("scadenza"):
                order_by = "scadenza_iscrizione"
                filtri &= Q(scadenza_iscrizione__lte=date.today() + timedelta(days=15))
            if sezione_id:
                filtri &= Q(sezione_id=sezione_id)  # todo: change to global_id
            if kwargs.get("consiglieri"):
                order_by = "ruolo_socio__id"
                filtri &= Q(ruolo_socio__isnull=False)
            return Socio.objects.filter(filtri).order_by(order_by)

    def resolve_socio(self, context, **kwargs):
        user = context.context.user
        _id = kwargs.get("id")
        if _id:
            try:
                _id = int(_id)
            except ValueError:
                _id = from_global_id(_id)[1]
            return Socio.objects.filter(sezione=user.userprofile.sezione).get(pk=_id)
        return None

    def resolve_consiglieri(self, context, **kwargs):
        user = context.context.user
        sezione_id = kwargs.get("sezione")
        filtri = Q()
        order_by = "ruolo_id"
        if sezione_id:
            try:
                sezione_id = int(sezione_id)
            except ValueError:
                sezione_id = from_global_id(sezione_id)[1]
            sezione = SezioneElsa.objects.get(pk=sezione_id)
        elif not user.is_superuser:
            sezione = user.userprofile.sezione
        else:
            sezione = SezioneElsa.objects.get(nome="Italia")
        if sezione.nome == "Italia" or (user.is_superuser and not sezione_id) or kwargs.get("nazionali"):
            filtri &= Q(ruolo_id__lte=13)
        else:
            filtri &= Q(socio__sezione=sezione) & Q(ruolo_id__gte=14)
        return RuoliSoci.objects.filter(filtri).order_by(order_by)
