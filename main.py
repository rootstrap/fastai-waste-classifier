from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from fastai.vision.all import *
import os


app = Flask(__name__)
model = load_learner('result-resnet34.pkl')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      prediction = model.predict(f.filename)
      num = int(prediction[1].numpy().tolist())
      prob = float(prediction[2].numpy()[num])
      print(f'Classified as {prediction[0]}', f'Class number {num}', f' with probability {prob}')
      os.remove(f.filename)
      return {'predicted': prediction[0], 'class_number':num, 'probability': prob}
      
		
if __name__ == '__main__':      
   app.run(debug = True)

