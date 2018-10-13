import graphene
from models import *

import gql.types as types


class Stats(graphene.ObjectType):
  lemmas = graphene.Int()
  forms = graphene.Int()


class Query(graphene.ObjectType):
    lemma = graphene.Field(types.Lemma, name=graphene.String())
    forms = graphene.List(types.Form, form=graphene.String())
    search = graphene.List(types.Form, search=graphene.String())
    stats = graphene.Field(Stats)

    def resolve_lemma(self, info, name):
        return Lemma.get(name=name)

    def resolve_forms(self, info, form):
        return Form.select().where(Form.name == form)

    def resolve_search(self, info, search):
        return Form.select().where(Form.name.startswith(search)).limit(100)

    def resolve_stats(self, info):
        lemmas = Lemma.select().count()
        forms = Form.select().count()

        return Stats(lemmas=lemmas, forms=forms)


schema = graphene.Schema(query=Query, types=[types.Lemma, types.Form])
