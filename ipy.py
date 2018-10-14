from wiktionary import Wiktionary, Declensions

word = 'ormur'

db = Wiktionary('articles.xml')

d = Declensions(db)

page = db.get_by_title(word)
declensions = d.get_declensions(word)

print(declensions)



