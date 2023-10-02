FROM python:3.11.2-slim-buster

RUN pip install poetry==1.4.0

COPY pyproject.toml poetry.lock /to_do_app/

WORKDIR /to_do_app/

RUN poetry config virtualenvs.create false

RUN poetry install

COPY . /to_do_app/

RUN poetry install

CMD ["uvicorn", "--host", "0.0.0.0", "to_do_app.app:app"]
