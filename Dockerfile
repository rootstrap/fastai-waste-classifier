FROM python:3.8.12

RUN apt-get -y update  && apt-get install -y 

RUN pip install fastai flask werkzeug gunicorn

WORKDIR /app

ADD result-resnet34.pkl /app/ 
ADD main.py /app/ 

CMD ["gunicorn", "main:app", "--bind" ,"0.0.0.0:8080"]


