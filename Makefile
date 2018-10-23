test:
		pipenv run python -m pytest --pdb


ipy:
	pipenv run ipython -i scripts/ipy.py


format:
	pipenv run black **/*.py


populate:
	pipenv run python populate.py
