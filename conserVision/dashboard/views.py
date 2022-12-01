from django.shortcuts import render
from .forms import ImageForm

import numpy as np
import cv2
import pickle as pk
from keras.models import load_model

root_path = 'C:/Users/Karan/conser-vision/conserVision/media/'
# root_path = '/Users/devasenan/Documents/conser-vision/conserVision/media/'
classes = ['antelope_duiker','bird','blank','civet_genet','hog','leopard','monkey_prosimian','rodent']

# def load_model(model_name):
#     model = None
#     model_path = root_path+model_name
#     with open(model_path, 'rb') as model_sav:
#         model = pk.load(model_sav)
#         model_sav.close()
#     return model

# cnn_model = load_model('models/cnn1_model1.h5')
cnn_model = load_model(root_path+'models/cnn1_model1.h5')

def read_image(img_name):
    size = 128
    img=cv2.imread(root_path+img_name)
    img = cv2.resize(img, (size, size))
    img = img/255
    return np.array([img])


# Create your views here.
def dashboard(request):
    form = ImageForm()
    obj = None
    y_pred_label = None

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.customSave(request.user)
        img = read_image(str(obj.photo))
        y_pred = cnn_model.predict(img)
        print(y_pred)
        y_pred_label = classes[np.argmax(y_pred)]
        return render(request, "dashboard/index.html", {
            'status': 1,
            'img': root_path+str(obj.photo),
            'prediction': y_pred_label,
        })

    return render(request, "dashboard/index.html", {
            'form': form,
            'status': 0
    })