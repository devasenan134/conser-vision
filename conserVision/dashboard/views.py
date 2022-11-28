from django.shortcuts import render
from .forms import ImageForm

import numpy as np
import cv2
import pickle as pk

root_path = '/Users/devasenan/Documents/conser-vision/conserVision/media/'

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
    form = ImageForm()
    obj = None
    y_pred = float()

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.customSave(request.user) 
        cnn_model = load_model('models/cnn1_model.sav')
        img = read_image(str(obj.photo))
        y_pred = cnn_model.predict(img)
        print(y_pred)
    return render(request, "dashboard/index.html", {
            'form': form,
            'prediction': y_pred,
    })