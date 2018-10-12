import click

from wiktionary import Database, Declensions
from models import Form, Lemma, db as sqldb

articles = Database('articles.xml')
d = Declensions(articles)

sqldb.drop_tables([Form, Lemma])
sqldb.create_tables([Form, Lemma])

parse_failures = ['Mið-Afríkulýðveldið', 'mar', 'hræðsla', 'áreynsla', 'endurnýjanleg orka', 'Garðabær', 'tannkrem', 'matseðill', '-leysi', 'eftirnafn', 'löggæsla', 'lungnablöðrur', 'fjendur', 'gammageislar', 'geimgeislar', '-nætti', '-gengill', 'rennandi vatn', 'ævilangur fangelsisdómur', 'lendingur']
temp_failures = []

known_failures = parse_failures + temp_failures

with open('failures.txt', 'w') as out:
  failures = []
  count = 0
  unparsed = 0

  with click.progressbar(articles.entries, label='populating') as entries:
    for entry in entries:
      if entry.parsed:
        try:
          if entry.title in known_failures:
            continue

          if not entry.is_icelandic:
            continue

          declensions = d.get_declensions(entry.title)

          lemma = Lemma(name=entry.title, part_of_speech=entry.part_of_speech)
          forms = [Form(name=form, head_word=lemma) for form in declensions]

          with sqldb.atomic():
            lemma.save()

            if forms:
              Form.bulk_create(forms)

          count += 1
        except Exception as exc:
          failures.append(entry.title)
      else:
        unparsed += 1

    out.write("{} not parsed".format(unparsed) + "\n")
    out.write("{} failed".format(len(failures)) + "\n")
    out.write("{} successfully parsed".format(count) + "\n\n")
    out.write(str(failures) + "\n")

print("Inserted {} Lemmas".format(Lemma.select().count()))
print("Inserted {} Forms".format(Form.select().count()))
print()
print("Wrote failures to failures.txt")
