# Using FastAI for creating a Waste Classifier

Fastai is a deep learning library which provides high-level components that can quickly and easily provide state-of-the-art results in standard deep learning domains.

It has two main design goals:

To be approachable and rapidly productive
To be also configurable.

## Waste Classifier
The aim is to build a model for waste classification that identifies among the different classes:

- cardboard
- compost
- glass
- metal
- paper
- plastic
- trash

This machine learning model will help people to improve their decision when classifying trash

## Dataset 

The data is already splitted in train and test folders. Inside each folder contains one folder for each class. Those images were obtained using Bing searcher using the api HTTP.
You can find the code used to download the images at [this](https://colab.research.google.com/drive/1JvAYFx1DIEi1MMyI-tuCfE2eHMSKisKT?usp=sharing) Google Colab.

