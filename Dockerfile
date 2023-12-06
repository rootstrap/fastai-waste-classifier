FROM python:3.8.12

RUN apt-get -y update  && apt-get install -y 

WORKDIR /app

COPY requirements.txt requirements.txt 
RUN pip install -r requirements.txt


COPY ./ /app/ 

CMD ["jupyter", "notebook" , "--allow-root", "--ip='0.0.0.0'"]

EXPOSE 8888
