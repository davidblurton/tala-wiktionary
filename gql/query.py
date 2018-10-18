import graphene
from models import *

import gql.types as types


class Stats(graphene.ObjectType):
    lemmas = graphene.Int()
    forms = graphene.Int()
    translations = graphene.Int()


class KeyCount(graphene.ObjectType):
    declension_group = graphene.String()
    count = graphene.Int()


class SearchResult(graphene.Union):
    class Meta:
        types = (types.Lemma, types.Form, types.Translation)

    @classmethod
    def resolve_type(cls, instance, info):
        if isinstance(instance, Lemma):
            return types.Lemma
        if isinstance(instance, Form):
            return types.Form
        if isinstance(instance, Translation):
            return types.Translation


class Query(graphene.ObjectType):
    lemma = graphene.Field(types.Lemma, name=graphene.String())
    lemmas = graphene.List(
        types.Lemma, group=graphene.String(), first=graphene.Int(default_value=100)
    )
    forms = graphene.List(types.Form, form=graphene.String())
    search = graphene.List(
        SearchResult, query=graphene.String(), first=graphene.Int(default_value=100)
    )
    stats = graphene.Field(Stats)
    declension_group = graphene.List(KeyCount, group=graphene.String())

    def resolve_declension_group(self, info, group):
        query = (
            Lemma.select(Lemma.declension_group, fn.COUNT(Lemma.id).alias("count"))
            .group_by(Lemma.declension_group)
            .order_by(fn.COUNT(Lemma.id).desc())
        )

        return query

    def resolve_lemma(self, info, name):
        try:
            return Lemma.get(Lemma.name == name)
        except Lemma.DoesNotExist:
            return None

    def resolve_lemmas(self, info, group, first):
        return (
            Lemma.select().where(Lemma.declension_group.startswith(group)).limit(first)
        )

    def resolve_forms(self, info, form):
        return Form.select().where(Form.name == form)

    def resolve_search(self, info, query, first):
        lemmas = Lemma.select().where(Lemma.name == query).limit(first).execute()
        forms = Form.select().where(Form.name == query).limit(first).execute()
        translations = (
            Translation.select()
            .where(Translation.meaning == query)
            .limit(first)
            .execute()
        )

        results = list(lemmas) + list(forms) + list(translations)
        return results[:first]

    def resolve_stats(self, info):
        lemmas = Lemma.select().count()
        forms = Form.select().count()
        translations = Translation.select().count()

        return Stats(lemmas=lemmas, forms=forms, translations=translations)
