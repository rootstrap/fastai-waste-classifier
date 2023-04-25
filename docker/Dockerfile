FROM python:3.8.12

RUN apt-get -y update  && apt-get install -y 

RUN pip install fastai Pillow streamlit

ADD result-resnet34.pkl /app/ 
ADD main.py /app/ 

WORKDIR /app

CMD ["streamlit", "run", "main.py", "--server.port=8080", "--server.address=0.0.0.0"]

EXPOSE 8080

