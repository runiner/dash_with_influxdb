FROM python:3.8-buster

WORKDIR /workdir/dash_app

ADD dash_app/requirements.txt /workdir/
RUN pip install --no-cache -r /workdir/requirements.txt

ADD common /workdir/common
ENV PYTHONPATH=/workdir/common

ADD dash_app /workdir/dash_app

EXPOSE 8050

CMD ["gunicorn", "-b", "0.0.0.0:8050", "app:server"]
