import graphene
from graphene_django.filter.fields import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from .models import BozzaEmail, Email
from django.db.models import Q, BooleanField, Case, Value, When


class EmailType(DjangoObjectType):

    class Meta:
        model = Email
        filter_fields = {
            "id": ["exact"],
            "oggetto": ["icontains"],
            "corpo": ["icontains"],
        }
        interfaces = (graphene.Node, )


class BozzaEmailType(DjangoObjectType):

    can_delete = graphene.Boolean()

    class Meta:
        model = BozzaEmail
        filter_fields = {
            "id": ["exact"],
            "oggetto": ["icontains"],
            "corpo": ["icontains"],
        }
        interfaces = (graphene.Node, )


class Query(graphene.ObjectType):
    all_emails = DjangoFilterConnectionField(EmailType)
    all_bozze = graphene.List(BozzaEmailType, disponibile_per=graphene.Int())

    def resolve_all_emails(self, context, **kwargs):
        user = context.context.user
        return Email.objects.filter(mittente=user).order_by('-inviata_il')

    def resolve_all_bozze(self, context, **kwargs):
        user = context.context.user
        filtri = Q(user=user) | Q(disponibile_per=2)
        filtri |= Q(disponibile_per=1) & Q(user__userprofile__sezione=user.userprofile.sezione)
        return BozzaEmail.objects.filter(filtri).annotate(can_delete=Case(
            When(user=user, then=Value(True)),
            default=Value(False),
            output_field=BooleanField()
        )).order_by('-creata_il')
