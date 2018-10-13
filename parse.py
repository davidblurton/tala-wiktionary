import click

from database import db as sqldb
from wiktionary import Wiktionary, Declensions
from models import Form, Lemma

wikitionary = Wiktionary('articles.xml')
d = Declensions(wikitionary)

sqldb.drop_tables([Form, Lemma])
sqldb.create_tables([Form, Lemma])

parse_failures = ['Mið-Afríkulýðveldið', 'mar', 'hræðsla', 'áreynsla', 'endurnýjanleg orka', 'Garðabær', 'tannkrem', 'matseðill', '-leysi', 'eftirnafn', 'löggæsla', 'lungnablöðrur', 'fjendur', 'gammageislar', 'geimgeislar', '-nætti', '-gengill', 'rennandi vatn', 'ævilangur fangelsisdómur', 'lendingur']
temp_failures = []

known_failures = parse_failures + temp_failures

with open('failures.txt', 'w') as out:
  failures = []
  count = 0
  unparsed = 0

  with click.progressbar(wikitionary.pages, label='populating') as pages:
    for page in pages:
      try:
          if not page.parsed:
            continue

          if page.title in known_failures:
            continue

          if not page.is_icelandic:
            continue

          lemma = Lemma.create(name=page.title, part_of_speech=page.part_of_speech, category=page.category)

          declensions = d.get_declensions(page.title)
          forms = [Form(name=form, head_word=lemma) for form in declensions]

          with sqldb.atomic():
            if forms:
              Form.bulk_create(forms)

          count += 1
      except Exception as exc:
        failures.append(page.title)

    out.write("{} not parsed".format(unparsed) + "\n")
    out.write("{} failed".format(len(failures)) + "\n")
    out.write("{} successfully parsed".format(count) + "\n\n")
    out.write(str(failures) + "\n")

print("Inserted {} Lemmas".format(Lemma.select().count()))
print("Inserted {} Forms".format(Form.select().count()))
print()
print("Wrote failures to failures.txt")
