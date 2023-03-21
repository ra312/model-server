FROM python:3.7-buster

RUN pip install mlflow==1.30.0

EXPOSE 5000

CMD mlflow server --host 0.0.0.0 --port 5000
