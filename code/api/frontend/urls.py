from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("mysql/", views.index),
    path("hdfs/", views.index),
    path("minio/", views.index),
]
