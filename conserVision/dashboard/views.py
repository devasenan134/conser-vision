from django.shortcuts import render

import numpy as np
import cv2
import pickle as pk

root_path = '/Users/devasenan/Documents/conser-vision/conserVision/'

def load_model(model_name):
    model = None
    model_path = root_path+model_name
    with open(model_path, 'rb') as model_sav:
        model = pk.load(model_sav)
        model_sav.close()
    return model

def read_image(img_name):
    size = 128
    img=cv2.imread(root_path+img_name)
    img = cv2.resize(img, (size, size))
    return np.array([img])


# Create your views here.
def dashboard(request):
    cnn_model = load_model('cnn1_model.sav')
    img = read_image('ZJ000004.jpg')
    print(img.shape)
    y_pred = cnn_model.predict(img)
    return render(request, "dashboard/dashboard.html", {
        'res': y_pred
    })