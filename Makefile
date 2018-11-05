setup:
	make download_dump
	pipenv install
	yarn install
	make test


download_dump:
	curl https://dumps.wikimedia.org/iswiktionary/latest/iswiktionary-latest-pages-articles.xml.bz2 -o articles.xml.bz2
	bzip2 --decompress --force articles.xml.bz2


test:
	pipenv run python -m pytest --pdb


ipy:
	pipenv run ipython -i scripts/ipy.py


format:
	pipenv run black **/*.py


populate:
	pipenv run python populate.py


schema:
	PYTHONPATH=. pipenv run python scripts/schema.py
