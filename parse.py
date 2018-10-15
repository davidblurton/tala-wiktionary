import click

from database import db as sqldb
from wiktionary import Wiktionary, Declensions
from models import Form, Lemma, Translation, MODELS

wikitionary = Wiktionary('articles.xml')
d = Declensions(wikitionary)

sqldb.drop_tables(MODELS)
sqldb.create_tables(MODELS)

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

        if page.name in known_failures:
          continue

        if not page.is_icelandic:
          continue

        lemma = Lemma.create(**page.to_dict())
        translations = [Translation(**translation, lemma=lemma) for translation in page.translations]

        declensions = d.get_declensions(page.name)
        forms = [Form(**declension, head_word=lemma) for declension in declensions]

        with sqldb.atomic():
          if forms:
            Form.bulk_create(forms)

          if translations:
            Translation.bulk_create(translations)

        count += 1
      except Exception as exc:
        failures.append(page.name)

    out.write("{} not parsed".format(unparsed) + "\n")
    out.write("{} failed".format(len(failures)) + "\n")
    out.write("{} successfully parsed".format(count) + "\n\n")
    out.write(str(failures) + "\n")

print("Inserted {} Lemmas".format(Lemma.select().count()))
print("Inserted {} Forms".format(Form.select().count()))
print("Inserted {} Translations".format(Translation.select().count()))
print()
print("Wrote failures to failures.txt")
