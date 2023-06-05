from django.urls import path
from . import views

urlpatterns = [
    path("menu/", views.display_menu, name="menu"),
    path("minio/", views.minio_input, name="minio"),
    path("mysql/", views.mysql_input, name="mysql"),
    path("hdfs/", views.hdfs_input, name="hdfs"),
    path("success/", views.success, name="success"),
    path("error/", views.error, name="error"),
    path("debug/refresh/", views.refresh, name="refresh"),
    path("debug/", views.debug, name="debug"),
]
