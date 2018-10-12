from wiktionary import Database, Declensions

word = 'Jesús'

db = Database('articles.xml')

d = Declensions(db)

entry = db.get_by_title(word)

declensions = d.get_declensions(word)

print(declensions)



