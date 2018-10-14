import graphene
import models


class Form(graphene.ObjectType):
    name = graphene.String()
    head_word = graphene.Field(lambda: Lemma)
    grammar_case = graphene.String()


class Lemma(graphene.ObjectType):
    name = graphene.String()
    category = graphene.String()
    part_of_speech = graphene.String()
    forms = graphene.List(graphene.List(Form))

    def resolve_forms(lemma, info):
      forms = lemma.forms

      group_size = len(forms) // 4
      grouped = zip(*(iter(forms),) * group_size)

      return list(map(list, zip(*grouped)))

TYPES = [
  Form, Lemma
]
