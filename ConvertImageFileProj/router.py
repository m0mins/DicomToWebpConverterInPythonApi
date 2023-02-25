from dicomToWebpApi.viewsets import DicomtoWebpViewset
from rest_framework import routers

router=routers.DefaultRouter()
router.register('imageFormatConvert',DicomtoWebpViewset)