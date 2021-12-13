#!/bin/python 

from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from fastai.vision.all import *
import os
import time

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', 'jpeg']
app.secret_key = "OopbBPqgw95PhuJDb2lG3XSq"
app.config['UPLOAD_FOLDER'] = 'static'

model = load_learner('result-resnet34.pkl')


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
   if request.method == 'GET':
      return render_template('upload.html')
   else:
      f = request.files['file']
      (result, filename) = save_file(f)
      if result:
         prediction = predict(filename)
         if 'predicted' in prediction.keys():
            return render_template('upload.html', filename=filename.split('/')[1], predict_message=f"Classified as {prediction['predicted']} with probability {prediction['probability']}")
         else:
            flash('An error has occurred')
            return render_template('upload.html')
      else:
         flash(filename)
         return render_template('upload.html')


@app.route('/classify', methods = ['POST'])
def upload_file():
   f = request.files['file']
   (result, filename) = save_file(f)
   result = predict(filename)
   os.remove(filename)
   return result

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

