import graphene
import models


class Lemma(graphene.ObjectType):
    name = graphene.String()
    category = graphene.String()
    part_of_speech = graphene.String()
    declensions = graphene.List(graphene.List(graphene.String))

    def resolve_declensions(lemma, info):
      forms = models.Form.select().join(models.Lemma).where(models.Lemma.id == lemma.id)

      declensions = [f.name for f in forms]
      group_size = len(declensions) // 4

      grouped = zip(*(iter(declensions),) * group_size)
      return list(map(list, zip(*grouped)))

class Form(graphene.ObjectType):
    name = graphene.String()
    head_word = graphene.Field(Lemma)
