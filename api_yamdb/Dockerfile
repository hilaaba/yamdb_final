FROM python:3.7-slim

WORKDIR /app

COPY ./. .

RUN python -m pip install --upgrade pip
# Install Apple M1 specific packages. Remove if you use another hardware
# RUN apt-get update && apt-get -y install libpq-dev gcc && pip3 install psycopg2
RUN pip3 install -r api_yamdb/requirements.txt --no-cache-dir

CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000"]
