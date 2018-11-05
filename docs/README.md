# tala-wiktionary

## Requirements

- python 3
- pipenv
- sqlite (included with python 3)

## Setup

Run `make schema` to install dependencies.
To populate the database, run `make populate`.

## Develop

To run the server 

```
pipenv shell
python api.py
```

To run the frontend

```
yarn start
```
