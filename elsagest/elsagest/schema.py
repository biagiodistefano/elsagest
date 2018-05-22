import graphene
import librosoci.schema
import elsamail.schema
from graphene_django_extras import get_all_directives


class Query(librosoci.schema.Query, elsamail.schema.Query, graphene.ObjectType, ):
    pass


schema = graphene.Schema(query=Query, directives=get_all_directives())
