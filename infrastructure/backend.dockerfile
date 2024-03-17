FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt update \
    && apt upgrade -y

COPY requirements/requirements.txt /app/

RUN pip install --no-cache-dir pip-tools \
  && pip-sync /app/requirements.txt

COPY . /app

COPY ./infrastructure/start.sh /start.sh

RUN chmod +x /start.sh

CMD ["/start.sh"]
