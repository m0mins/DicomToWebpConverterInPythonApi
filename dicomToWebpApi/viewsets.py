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
            print(webp_filename)
            if webp_filename.endswith(".webp"):
                imagep=webp_filename
                dicomImage=ImageConvert.objects.create(name=img_data["name"],image=imagep)
                dicomImage.save()


                serializer=ImageConvertSerializer(dicomImage)
                image_data = serializer.data['image']           
                media_folder_path = os.path.join(settings.MEDIA_ROOT, image_data)           
                # Create a PIL Image object from the webp bytes
                pil_image = Image.open(BytesIO(media_folder_path.encode()))              
                # Create a BytesIO object to store the image data
                image_io = BytesIO()              
                # Save the image to the BytesIO object as webp
                pil_image.save(image_io, 'webp')              
                # Set the response headers
                response = HttpResponse(image_io.getvalue(), content_type='image/webp')
                response['Content-Disposition'] = 'inline; filename="image.webp"'
                return response



                # serializer=ImageConvertSerializer(dicomImage)
                # return Response(serializer.data)
                # return Response({"Success": "Converted Successfully"}, status=status.HTTP_201_CREATED)
        #     else:
        #         return Response({"Message": "Invalid image format"}, status=400)
        # else:
        #     return Response({"Message": "Error !! Upload a valid dicom image format"}, status=400)
        

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

    