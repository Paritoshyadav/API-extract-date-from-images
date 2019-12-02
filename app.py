# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 18:03:08 2019

@author: Tinu
"""
import os
from flask import Flask, render_template, request,url_for,redirect
from flask_uploads import UploadSet, configure_uploads, IMAGES

from date import hybridocr
from date import simpleocr
from os.path import join, dirname, realpath

app = Flask(__name__)
cwd = os.getcwd()
UPLOAD_FOLDER = '/static/img'

photos=UploadSet('photos',IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = UPLOAD_FOLDER

cwd = os.getcwd()
cwd

configure_uploads(app,photos)



@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/',methods=['POST','GET'])
def predict():
    if request.method=='POST' and 'photo' in request.files:
        
        filename=photos.save(request.files['photo'])
        file=os.path.join(UPLOAD_FOLDER,filename)
        try:
            
            text=hybridocr(file)
            return render_template('Home.html',extracted_text=text)
        except Exception:
            try:
                text=simpleocr(file)
                return render_template('Home.html',extracted_text=text)
            except Exception:
                return render_template('Home.html',extracted_text="no date is found")
            
        
    
        
    else:
        return render_template('Home.html',extracted_text='not found photo')
        





if __name__ == '__main__':
    app.run(debug=True)

