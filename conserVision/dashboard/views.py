from django.shortcuts import render, HttpResponse, reverse, redirect
from django.core.files.storage import FileSystemStorage
from .forms import ImageForm
from django.conf import settings


from django.views.generic import View
from .utils import make_prediction, rename_file, get_upload_dt, bar_plot, html_to_pdf


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


report_context = {}
# Create your views here.
def batch_predict(request):
    global report_context

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

        fig = bar_plot(predictions)

        report_context = {
            'predictions': predictions,
            'batch_name': batch_name,
            'plot_fig': fig,
        }
        return render(request, 'dashboard/batch_report.html', report_context)

    return render(request, "dashboard/batch_predict.html", {
        'status': 0,
    })


class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        # getting the template
        global report_context
        pdf = html_to_pdf('dashboard/batch_report.html', report_context)        
         # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')
