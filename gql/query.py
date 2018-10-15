import graphene
from models import *

import gql.types as types


class Stats(graphene.ObjectType):
  lemmas = graphene.Int()
  forms = graphene.Int()
  translations = graphene.Int()


class Query(graphene.ObjectType):
    lemma = graphene.Field(types.Lemma, name=graphene.String())
    forms = graphene.List(types.Form, form=graphene.String())
    search = graphene.List(types.Form, search=graphene.String(), limit=graphene.Int(default_value=100))
    stats = graphene.Field(Stats)

    def resolve_lemma(self, info, name):
        try:
            return Lemma.get(Lemma.name == name)
        except Lemma.DoesNotExist:
            return None

    def resolve_forms(self, info, form):
        return Form.select().where(Form.name == form)

    def resolve_search(self, info, search, limit):
        return Form.select().where(Form.name.startswith(search)).limit(limit)

    def resolve_stats(self, info):
        lemmas = Lemma.select().count()
        forms = Form.select().count()
        translations = Translation.select().count()

        return Stats(lemmas=lemmas, forms=forms, translations=translations)
