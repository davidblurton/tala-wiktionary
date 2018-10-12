import graphene
import models


class Lemma(graphene.ObjectType):
    name = graphene.String()
    part_of_speech = graphene.String()


class Form(graphene.ObjectType):
    name = graphene.String()
