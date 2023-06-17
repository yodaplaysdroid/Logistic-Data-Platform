from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("mysql/", views.index),
    path("hdfs/", views.index),
    path("minio/", views.index),
    path("ann1/", views.index),
    path("ann2/", views.index),
    path("ann3/", views.index),
    path("ann4/", views.index),
    path("ann5/", views.index),
    path("ann6/", views.index),
]
