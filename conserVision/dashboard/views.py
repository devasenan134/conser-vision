from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .forms import ImageForm
from django.conf import settings

import numpy as np
import cv2
import pickle as pk
from keras.models import load_model
from datetime import datetime
import seaborn as sns

# root_path = 'C:/Users/Karan/conser-vision/conserVision/media/'
root_path = '/Users/devasenan/Documents/conser-vision/conserVision/media/'
cnn_model = load_model(root_path+'models/cnn1_model1.h5')


def read_image(img_name):
    print("from read_img:",img_name)
    size = 128
    img=cv2.imread('/Users/devasenan/Documents/conser-vision/conserVision'+img_name)
    img = cv2.resize(img, (size, size))
    img = img/255
    return np.array([img])


def make_prediction(file_url):
    classes = ['antelope_duiker','bird','blank','civet_genet','hog','leopard','monkey_prosimian','rodent']
    img=read_image(file_url)
    y_pred = cnn_model.predict(img)
    # print(y_pred)
    y_pred_label = classes[np.argmax(y_pred)]
    return y_pred_label


# Create your views here.
def dashboard(request):
    # form = ImageForm()
    obj = None
    y_pred_label = None
    folder_name = 'imgs'

    if request.method == 'POST':
        # form = ImageForm(request.POST, request.FILES)
        upload = request.FILES['photo']
        fss = FileSystemStorage(location=settings.MEDIA_ROOT+folder_name, base_url=settings.MEDIA_URL+folder_name)
        file = fss.save(upload.name, upload)
        print('upload:', upload, 'file:', file)
        file_url = fss.url(file)
        print('url:',file_url)

        # if form.is_valid():
        #     obj = form.customSave(request.user)
        #     print("obj:",obj)
        # img = read_image(str(obj.photo))

        file_label = make_prediction(file_url)
        return render(request, "dashboard/index.html", {
            'status': 1,
            # 'img': root_path+str(obj.photo),
            'img': file_url,
            'prediction': file_label,
        })

    return render(request, "dashboard/index.html", {
            'status': 0,
    })


def get_upload_dt():
    today = datetime.now()
    date = ''.join(map(str, [today.year, today.month, today.day]))
    time = ''.join(map(str, [today.hour, today.minute, today.second]))
    return 'dt'.join([date, time])


def rename_file(file_name, dt):
    name, ext = file_name.split('.')
    new_name = '.'.join([name+dt, ext])
    return new_name

def bar_plot(predictions):
    class_dict = {}
    for img, cls in predictions:
        class_dict[cls] = class_dict.get(cls, 0) + 1
    print(class_dict)   
    sns.barplot(x='classes', y='count', data=class_dict)


# Create your views here.
def batch_predict(request):

    if request.method == 'POST':
        print(request.POST)
        batch_name = request.POST.get('batch_name')

        folder_name = 'batch'
        fss = FileSystemStorage(location=settings.MEDIA_ROOT+folder_name, base_url=settings.MEDIA_URL+folder_name)
        dt = get_upload_dt()
        predictions = []

        for count, file in enumerate(request.FILES.getlist('files')):
            new_name = rename_file(file.name, dt)
            fss.save(new_name, file)
            file_url = fss.url(new_name)
            file_label = make_prediction(file_url)
            predictions.append([file.name, file_label])

        plot = bar_plot(predictions)

        return render(request, 'dashboard/batch_report.html', {
            'predictions': predictions,
            'batch_name': batch_name,
        })

    return render(request, "dashboard/batch_predict.html", {
        'status': 0,
    })