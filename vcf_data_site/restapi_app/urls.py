from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'api', views.VcfRowViewSet, basename='VCF-Row')
router.register(r'api/<str:pk>', views.VcfRowViewSet, basename="Single-VCF-Row")

urlpatterns = [
    path('upload/', views.UploadFileView.as_view(), name='upload-file'),
    path('', include(router.urls)),
]