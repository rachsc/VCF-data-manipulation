from django.urls import path, include
from . import views
from rest_framework import routers

app_name = "restapi"
router = routers.DefaultRouter()
router.register(r'api', views.VcfRowViewSet, basename='vcf-data')
router.register(r'api/<str:pk>', views.VcfRowViewSet, basename="single-vcf-row")

urlpatterns = [
    path('upload/', views.UploadFileView.as_view(), name='upload-file'),
    path('register/', views.UserCreate.as_view(), name='register-user'),
    path('', include(router.urls)),
]