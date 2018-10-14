from peewee import *
from database import BaseModel


class Lemma(BaseModel):
  name = TextField(index=True)
  part_of_speech = TextField()
  category = TextField()

  def __repr__(self):
    return '<Lemma(name=%s)>' % (self.name)


class Form(BaseModel):
  name = TextField(index=True)
  head_word = ForeignKeyField(Lemma, backref='forms')
  grammar_case = TextField()

  def __repr__(self):
    return '<Form(name=%s)>' % (self.name)


MODELS = [
  Lemma,
  Form,
]
