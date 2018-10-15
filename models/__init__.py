from peewee import *
from database import db


class BaseModel(Model):
  class Meta:
    database = db


class Lemma(BaseModel):
  name = TextField(index=True)
  part_of_speech = TextField()
  category = TextField()

  def __repr__(self):
    return '<Lemma(name=%s)>' % (self.name)


class Form(BaseModel):
  name = TextField(index=True)
  lemma = ForeignKeyField(Lemma, backref='forms')
  grammar_tag = TextField()

  def __repr__(self):
    return '<Form(name=%s)>' % (self.name)


class Translation(BaseModel):
  lang = TextField(index=True)
  meaning = TextField(index=True)
  lemma = ForeignKeyField(Lemma, backref='translations')

  def __repr__(self):
    return '<Translation(lang=%s, meaning=%s)>' % (self.name, self.meaning)


MODELS = [
  Lemma,
  Form,
  Translation,
]
