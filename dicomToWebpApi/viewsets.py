from rest_framework import viewsets
from . import models
from . models import ImageConvert
from . import serializers
from .serializers import ImageConvertSerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
import os
import io
from PIL import Image
import pydicom
import pprint
from io import BytesIO
from pydicom.data import get_testdata_file
from django.http import FileResponse
from rest_framework.parsers import FileUploadParser,MultiPartParser
from django.conf import settings
import numpy as np

class DicomtoWebpViewset(viewsets.ModelViewSet):
    
    queryset = models.ImageConvert.objects.all()
    serializer_class = serializers.ImageConvertSerializer
    parser_classes=(MultiPartParser,)   
   
    def create(self, request, *args, **kwargs):
        img_data = request.data

        obj = ImageConvert.objects.create(image=request.FILES['image']) # let's insert it to db
        image_path = obj.image.name

        if image_path.endswith(".dcm"):
            webp_filename = convert_dicom_to_webp(image_path)
            if webp_filename.endswith(".webp"):
                imagep=webp_filename
                dicomImage=ImageConvert.objects.create(name=img_data["name"],image=imagep)
                dicomImage.save()              
                with open(os.path.join(settings.MEDIA_ROOT,imagep), 'rb') as f:
                    # Open the WebP image file using the Pillow library
                    pil_image = Image.open(f)

                    # Create a BytesIO object to store the image data
                    image_io = BytesIO()

                    # Save the image to the BytesIO object as JPEG
                    pil_image.save(image_io, 'webp')

                    # Get the contents of the BytesIO object as bytes
                    webp_data = image_io.getvalue() 

                    response = HttpResponse(image_io.getvalue(), content_type='image/webp')
                    response['Content-Disposition'] = 'inline; filename="image.webp"'
                    return response
                              

def convert_dicom_to_webp(input_filename):
    # Load the DICOM file
  
    media_folder_path = os.path.join(settings.MEDIA_ROOT, input_filename)

    dicom_file = pydicom.dcmread(media_folder_path)
   
    # Convert the DICOM file to a PIL Image object
    pil_image = Image.fromarray(dicom_file.pixel_array)
    # Save the PIL Image object as a WebP file in the output directory
    webp_filename = os.path.splitext(input_filename)[0] + ".webp"
    pil_image.save(os.path.join(settings.MEDIA_ROOT, webp_filename), "WEBP")

    return webp_filename