#!/bin/python 

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from fastai.vision.all import *
import os


app = Flask(__name__)
model = load_learner('result-resnet34.pkl')

@app.route('/')
def home():
    return 'ok'

def process_file(f):
   f.save(secure_filename(f.filename))
   prediction = model.predict(f.filename)
   num = int(prediction[1].numpy().tolist())
   prob = float(prediction[2].numpy()[num])
   print(f'Classified as {prediction[0]}, Class number {num} with probability {prob}')
   os.remove(f.filename)
   return {'predicted': prediction[0], 'class_number':num, 'probability': prob}
    


@app.route('/upload', methods = ['GET','POST'])
def upload():
   if request.method == 'GET':
      return render_template('upload.html')
   else:
      f = request.files['file']
      return process_file(f)

@app.route('/uploader', methods = ['POST'])
def upload_file():
   f = request.files['file']
   return process_file(f)
      
		
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

