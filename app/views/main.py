from flask import render_template, jsonify, Flask, redirect, url_for, request
from app import app
from app import model
from app import graph
import random
import os
import tensorflow as tf
from keras.applications.mobilenet import MobileNet
from keras.preprocessing import image
from keras.layers import Activation, Dense
from keras.models import load_model
from keras.applications.mobilenet import preprocess_input, decode_predictions
from keras.applications import imagenet_utils, mobilenet
import numpy as np
import requests
import datetime


@app.route('/')
@app.route('/index')
def index():
    
    return render_template('index.html', title='Home')

@app.route('/uploaded', methods = ['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
        f = request.files['file']
        path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        f.save(path)
        
        img = image.load_img(path, target_size=(224,224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = mobilenet.preprocess_input(x)
        global graph
        with graph.as_default():
            prediction = model.predict(x)
        results = imagenet_utils.decode_predictions(prediction)
        rst = results[0][0][1]
       
        return render_template('uploaded.html', title='Success', predictions=rst,user_image=f.filename)

    
@app.route('/download', methods=['GET'])
def download():
        url = request.args['url']
        filename = request.args.get('filename', 'image.png')
        r = requests.get(url)
        imgnamedate = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        with app.open_instance_resource(imgnamedate + '.jpg', 'wb') as f:
            f.write(r.content)
        imagepath = app.open_instance_resource(imgnamedate + '.jpg')
        img = image.load_img(imagepath, target_size=(224,224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = mobilenet.preprocess_input(x)
        global graph
        with graph.as_default():
            prediction = model.predict(x)
        
        prediction = model.predict(x)
        results = imagenet_utils.decode_predictions(prediction)
        userimage = imgnamedate +'.jpg'
        rst = results[0][0][1]
        return render_template('uploaded.html', title='Success',predictions= rst, user_image=userimage)
    

@app.route('/map')
def map():
    return render_template('map.html', title='Map')


@app.route('/map/refresh', methods=['POST'])
def map_refresh():
    points = [(random.uniform(48.8434100, 48.8634100),
               random.uniform(2.3388000, 2.3588000))
              for _ in range(random.randint(2, 9))]
    return jsonify({'points': points})


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')
