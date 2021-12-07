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


@app.route('/uploader', methods = ['POST'])
def upload_file():
   print('0')
   f = request.files['file']
   print('1')
   f.save(secure_filename(f.filename))
   print('2')
   prediction = model.predict(f.filename)
   print('3')
   num = int(prediction[1].numpy().tolist())
   print('4')
   prob = float(prediction[2].numpy()[num])
   print(f'Classified as {prediction[0]}', f'Class number {num}', f' with probability {prob}')
   os.remove(f.filename)
   return {'predicted': prediction[0], 'class_number':num, 'probability': prob}
      
		
if __name__ == '__main__':
    app.run(debug=True)

