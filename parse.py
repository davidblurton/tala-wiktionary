import click

from wiktionary import db, Declensions


with open('failures.txt', 'w') as out:
  for gender in ['kk', 'kvk', 'hk']:
    failures = []
    count = 0

    with click.progressbar(db.entries, label=gender) as entries:
      for entry in entries:
        if entry.declension and entry.declension.startswith(gender):
          try:
            entry = db.get_by_title(entry.title)
            templ = db.get_declension_template(entry.declension)

            d = Declensions()
            d.get_declensions(entry, templ)

            count += 1
          except Exception as exc:
            failures.append(entry.title)

      out.write(gender + "\n")
      out.write("{} failed".format(len(failures)) + "\n")
      out.write("{} successfully parsed".format(count) + "\n")
      out.write(str(failures) + "\n\n")

print("Wrote failures to failures.txt")