import graphene
import models

import gql.types as types


class Query(graphene.ObjectType):
    lemma = graphene.Field(types.Lemma, name=graphene.String())
    forms = graphene.List(types.Form, search=graphene.String())

    def resolve_lemma(self, info, name):
        return models.Lemma.get(name=name)

    def resolve_forms(self, info, search):
        return models.find_forms(search)


schema = graphene.Schema(query=Query, types=[types.Lemma, types.Form])
