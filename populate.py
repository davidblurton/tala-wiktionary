import click

from database import db as sqldb
from wiktionary import Wiktionary, Declensions
from frequencies import Frequencies
from models import Form, Lemma, Translation, MODELS

wikitionary = Wiktionary("articles.xml")
frequencies = Frequencies("frequency.csv")
d = Declensions(wikitionary)

sqldb.drop_tables(MODELS)
sqldb.create_tables(MODELS)

known_failures = ['Mið-Afríkulýðveldið', 'mar', 'endurnýjanleg orka', 'Garðabær']


with open("failures.txt", "w") as out:
    failures = []
    count = 0

    with click.progressbar(wikitionary.pages, label="populating") as pages:
        for page in pages:
            for entry in page.get_entries():
                try:
                    if entry.name in known_failures:
                        continue

                    if not entry.is_icelandic:
                        continue

                    if not entry.part_of_speech:
                        # TODO: Don't yield entries we don't understand
                        continue

                    lemma = Lemma.create(**entry.to_dict(), frequency=frequencies.get(entry.name) or 0)
                    translations = [
                        Translation(**translation, lemma=lemma)
                        for translation in entry.translations
                    ]

                    declensions = d.get_declensions(entry.name)
                    forms = [
                        Form(**declension, lemma=lemma) for declension in declensions
                    ]

                    with sqldb.atomic():
                        if forms:
                            Form.bulk_create(forms)

                        if translations:
                            Translation.bulk_create(translations)

                    count += 1
                except Exception as exc:
                    print(exc)
                    failures.append(entry.name)

        out.write("{} failed".format(len(failures)) + "\n")
        out.write("{} successfully parsed".format(count) + "\n\n")
        out.write(str(failures) + "\n")

print("Inserted {} Lemmas".format(Lemma.select().count()))
print("Inserted {} Forms".format(Form.select().count()))
print("Inserted {} Translations".format(Translation.select().count()))
print()
print("Wrote failures to failures.txt")
