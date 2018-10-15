from wiktionary import Wiktionary, Declensions

word = 'hestur'

db = Wiktionary('hestur.xml')

d = Declensions(db)

page = db.get_by_title(word)
declensions = d.get_declensions(word)

print(declensions)



