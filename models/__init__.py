from peewee import *

from playhouse.sqlite_ext import SqliteExtDatabase

db = SqliteExtDatabase('words.db', pragmas=(
    ('cache_size', -1024 * 64),  # 64MB page-cache.
    ('journal_mode', 'wal'),  # Use WAL-mode (you should always use this!).
    ('foreign_keys', 1)))  # Enforce foreign-key constraints.


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
  head_word = ForeignKeyField(Lemma)

  def __repr__(self):
    return '<Form(name=%s)>' % (self.name)


MODELS = [
  Lemma,
  Form,
]


def find_lemmas(word):
  return Lemma.select().join(Form).where(Form.name == word)

def find_forms_for_lemma(word):
  return Form.select().join(Lemma).where(Lemma.name == word)

def find_forms(word):
  return Form.select().where(Form.name == word)

