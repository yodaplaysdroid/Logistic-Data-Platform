from django.urls import path
from . import views

urlpatterns = [
    path("minio/", views.minio_input, name="minio"),
    path("mysql/", views.mysql_input, name="mysql"),
    path("hdfs/", views.hdfs_input, name="hdfs"),
    path("dashboard/", views.dashboard, name="dashboard"),
]
