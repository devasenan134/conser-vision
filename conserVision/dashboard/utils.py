import numpy as np
import cv2
from keras.models import load_model
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import matplotlib
matplotlib.use('SVG')

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views.generic import View



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
    preds = np.array(predictions)
    print(preds[:, 1])
    count_plot = sns.countplot(x=preds[:, 1])
    file = BytesIO()
    count_plot.figure.savefig(file, format="png")
    b64 = base64.b64encode(file.getvalue()).decode()
    return b64



def html_to_pdf(template_src, context_dict={}):
     template = get_template(template_src)
     html  = template.render(context_dict)
     result = BytesIO()
     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
     if not pdf.err:
         return HttpResponse(result.getvalue(), content_type='application/pdf')
     return None
