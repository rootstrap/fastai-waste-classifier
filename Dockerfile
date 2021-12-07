FROM python:3.8.12

RUN apt-get -y update  && apt-get install -y 

RUN pip install fastai flask werkzeug gunicorn

WORKDIR /app

ADD result-resnet34.pkl /app/ 
ADD main.py /app/ 

CMD ["python", "main.py"]

EXPOSE 5000

