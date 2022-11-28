from django import forms
from .models import Upload_Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Upload_Image
        fields = ('photo',)
    
    def customSave(self, user):
        lv = self.save(commit=False)
        lv.created_by = user
        lv.save()
        return lv