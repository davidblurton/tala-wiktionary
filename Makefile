test:
		pipenv run python -m pytest --pdb


ipy:
	pipenv run ipython -i ipy.py


format:
	pipenv run black **/*.py
