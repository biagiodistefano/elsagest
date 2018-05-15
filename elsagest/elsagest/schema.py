import graphene
import librosoci.schema


class Query(librosoci.schema.Query, graphene.ObjectType, ):
    pass


schema = graphene.Schema(query=Query)
