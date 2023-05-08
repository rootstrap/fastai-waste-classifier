import streamlit as st
from PIL import Image
from fastai.vision.all import load_learner
from datetime import datetime
import sys
import re
import os

model = load_learner('result-resnet34.pkl')

st.set_page_config(layout="wide", page_title="Waste Classifier Prototype")

st.write("## Waste classifier Prototype")


def truncate(num):
    return re.sub(r'^(\d+\.\d{,3})\d*$', r'\1', str(num))


def predict(filename):
    try:
        prediction = model.predict(filename)
        num = int(prediction[1].numpy().tolist())
        prob = truncate(float(prediction[2].numpy()[num]))
        print(
            f'Classified as {prediction[0]}, \
                Class number {num} with probability {prob}'
        )
        
        return {'predicted': prediction[0], \
                'class_number': num, 'probability': prob
            }
    except:
        print(sys.exc_info()[0])
        return 'Error'


def process_image(upload):
    ts = datetime.timestamp(datetime.now())
    orignal_image = Image.open(upload)
    image_name = f'{ts}-{upload.name}'
    orignal_image.save(image_name)
    col2.image(orignal_image)

    response = ''
    prediction = predict(image_name)
    if 'predicted' in prediction.keys():
        response = f"Classified as **{prediction['predicted'].upper()}** \
            with probability **{prediction['probability']}**"
    else:
        response = 'An error has occurred processing file'

    col2.write(f"{response}")
    os.remove(image_name)


col1, col2 = st.columns(2)
col1.write('''The aim is to build a model for waste \
      classification that identifies among the different classes:
    - cardboards\n
    - compost\n
    - glass\n
    - metal\n
    - paper\n
    - plastic\n
    - trash'''
    )

my_upload = st.sidebar.file_uploader(
    "Upload an image", type=["png", "jpg", "jpeg"])

if my_upload is not None:
    process_image(upload=my_upload)
