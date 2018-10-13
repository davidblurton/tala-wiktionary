from wiktionary import Database, Declensions

word = 'Darri'

db = Database('articles.xml')

d = Declensions(db)

page = db.get_by_title(word)
declensions = d.get_declensions(word)

print(declensions)



