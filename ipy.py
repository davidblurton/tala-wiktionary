from wiktionary import Wiktionary, Declensions

word = "matseðill"

db = Wiktionary("articles.xml")

d = Declensions(db)

page = db.get_by_title(word)
entries = list(page.get_entries())

for entry in entries:
  print(entry.to_dict())

declensions = d.get_declensions(word)

