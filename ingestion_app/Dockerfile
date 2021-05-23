FROM python:3.8-buster

WORKDIR /workdir/ingestion_app

ADD ingestion_app/requirements.txt /workdir/
RUN pip install --no-cache -r /workdir/requirements.txt

ADD common /workdir/common
ENV PYTHONPATH=/workdir/common

ADD ingestion_app /workdir/ingestion_app

CMD ["python", "/workdir/ingestion_app/main.py"]
