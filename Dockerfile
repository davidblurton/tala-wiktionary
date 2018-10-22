FROM python:3.7

WORKDIR /usr/src/app

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --deploy --system

COPY . .

EXPOSE 5000

CMD [ "python", "./api.py" ]
