from django.db import models

def nameFile(instance, filename):
     return '/'.join(['images', filename])
   

class ImageConvert(models.Model):
    name=models.CharField(max_length=100)
    image = models.ImageField(upload_to=nameFile, blank=True, null=True)   
    