#!/bin/python 

from flask import Flask, render_template, request, flash, redirect, url_for, make_response
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from fastai.vision.all import *
import os
import time
import datetime


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', 'jpeg']
app.secret_key = "OopbBPqgw95PhuJDb2lG3XSq"
app.config['UPLOAD_FOLDER'] = 'static'

model = load_learner('result-resnet34.pkl')

# remove files older than 1 minute (60s)
def remove_files():
   for file in [os.path.join(app.config['UPLOAD_FOLDER'],file)
            for file in next(os.walk(app.config['UPLOAD_FOLDER']))[2]
            if not file.startswith('.')]:

      file_path = os.path.join(file)
      creation_date = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
      now = datetime.datetime.now()
      diff = now - creation_date
      if diff.seconds > 60:
         print(f'Removing file {file}')
         os.remove(file_path)


def validate_filename(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['UPLOAD_EXTENSIONS']


def predict(filename):
   try:
      prediction = model.predict(filename)
      num = int(prediction[1].numpy().tolist())
      prob = float(prediction[2].numpy()[num])
      print(f'Classified as {prediction[0]}, Class number {num} with probability {prob}')
      return {'predicted': prediction[0], 'class_number':num, 'probability': prob}
   except:
      print(sys.exc_info()[0])
      return 'Error'

def save_file(f):
   
   remove_files()

   filename = secure_filename(f.filename)
   
   if filename=='':
      return (False, 'Empty filename')

   if not validate_filename(filename):
      return (False, 'The file extension should be .jpg, .png or jpeg')

   timestamp = time.time()  
   fullname = os.path.join(app.config['UPLOAD_FOLDER'], filename + f'_{timestamp}')
   f.save(fullname)

   return (True, fullname)
   

@app.route('/')
def home():
    return render_template('upload.html')

@app.route('/check')
def check():
    return 'ok'


@app.route('/upload', methods = ['GET','POST'])
def upload():
   response = render_template('upload.html')
   filename = ''
   if request.method != 'GET':
      f = request.files['file']
      (result, filename) = save_file(f)
      if result:
         prediction = predict(filename)
         if 'predicted' in prediction.keys():
            response = render_template('upload.html', 
               filename=filename.split('/')[1], 
               predict_message=f"Classified as {prediction['predicted']} with probability {prediction['probability']}")
         else:
            flash('An error has occurred')
      else:
         flash(filename)

   return response

@app.route('/classify', methods = ['POST'])
def upload_file():
   f = request.files['file']
   (result, filename) = save_file(f)
   result = predict(filename)
   os.remove(filename)
   return result

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

