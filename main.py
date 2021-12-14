#!/bin/python 

from flask import Flask, render_template, request, redirect, url_for, make_response
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from fastai.vision.all import *
import os
import time
import datetime
from pathlib import Path
import re

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', 'jpeg']
app.secret_key = "OopbBPqgw95PhuJDb2lG3XSq"
app.config['UPLOAD_FOLDER'] = 'static'

model = load_learner('result-resnet34.pkl')

def truncate(num):
    return re.sub(r'^(\d+\.\d{,3})\d*$',r'\1',str(num))

# remove files older than 1 minute (60s)
def remove_files():
   for f in [x for x in Path(app.config['UPLOAD_FOLDER']).iterdir() if x.is_file() and not x.name.startswith('.')]:
      creation_date = datetime.datetime.fromtimestamp(os.path.getmtime(f))
      now = datetime.datetime.now()
      diff = now - creation_date
      if diff.seconds > 60:
         print(f'Removing file {f.name}')
         os.remove(f)


def predict(filename):
   try:
      prediction = model.predict(filename)
      num = int(prediction[1].numpy().tolist())
      prob = truncate(float(prediction[2].numpy()[num]))
      print(f'Classified as {prediction[0]}, Class number {num} with probability {prob}')
      return {'predicted': prediction[0], 'class_number':num, 'probability': prob}
   except:
      print(sys.exc_info()[0])
      return 'Error'

def save_file(f):
   
   filename = secure_filename(f.filename)
   
   if filename=='':
      return (False, 'Empty filename')

   if not filename.lower().endswith(tuple(app.config['UPLOAD_EXTENSIONS'])):
      return (False, f"The file extension should be {app.config['UPLOAD_EXTENSIONS']}")

   remove_files()

   timestamp = time.time()  
   fullname = os.path.join(app.config['UPLOAD_FOLDER'], filename + f'_{timestamp}')
   f.save(fullname)

   return (True, fullname)
   

@app.route('/check')
def check():
    return 'ok'


@app.route('/', methods = ['GET','POST'])
def upload():
   response = render_template('upload.html')
   filename = ''
   if request.method == 'POST':
      f = request.files['file']
      (result, filename) = save_file(f)
      print(response, filename)
      if result:
         prediction = predict(filename)
         if 'predicted' in prediction.keys():
            response = render_template('upload.html', 
               filename=filename.split('/')[1], 
               predict_message=f"Classified as {prediction['predicted']} with probability {prediction['probability']}")
         else:
            response = render_template('upload.html', error_message='An error has occurred processing file')
      else:
         response = render_template('upload.html', error_message=filename)
   return response

@app.route('/classify', methods = ['POST'])
def upload_file():
   f = request.files['file']
   (result, filename) = save_file(f)
   if result:
      result = predict(filename)
      os.remove(filename)
      return result
   else:
      return filename

@app.errorhandler(Exception)          
def basic_error(e):
   print('Error:', e)          
   return render_template('upload.html', error_message='An error has occurred')         
  

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

