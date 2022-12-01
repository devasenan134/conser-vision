from django.db import models

# Create your models here.
class Upload_Image(models.Model):
    photo = models.ImageField(upload_to='imgs')
    prediction = models.CharField(max_length=20, null=True, blank=True)