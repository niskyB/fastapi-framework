FROM python:3.10

WORKDIR /code

ENV POETRY_VIRTUALENVS_IN_PROJECT=true \
  VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$VENV_PATH/bin:$PATH"

COPY pyproject.toml poetry.lock prestart.sh backend_pre_start.py alembic.ini migration.py roles.yml /code/

RUN pip install poetry tenacity psycopg2 alembic \
  && poetry config virtualenvs.create false \
  && poetry install \
  && chmod -R 777 ./prestart.sh

COPY ./app /code/app
COPY ./alembic /code/alembic

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

RUN sed -i -e 's/\r$//' prestart.sh

EXPOSE 8000

CMD ["sh", "-c", "./prestart.sh && uvicorn --host=0.0.0.0 --port=8000 app.main:app --reload"]
