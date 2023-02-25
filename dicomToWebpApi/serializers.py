from rest_framework import serializers
from . models import ImageConvert



class ImageConvertSerializer(serializers.ModelSerializer):
  
    class Meta:
        model=ImageConvert
        fields=('name','image')        