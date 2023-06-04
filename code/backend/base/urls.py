from django.urls import path
from . import views

urlpatterns = [
    path("menu/", views.display_menu, name="menu"),
    path("minio/", views.minio_input, name="minio"),
    path("mysql/", views.mysql_input, name="mysql"),
    path("hdfs/", views.hdfs_input, name="hdfs"),
    path("success/", views.success, name="success"),
]
