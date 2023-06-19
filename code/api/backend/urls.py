from django.urls import path
from . import views

urlpatterns = [
    path("minio/", views.minio_input, name="minio"),
    path("mysql/", views.mysql_input, name="mysql"),
    path("hdfs/", views.hdfs_input, name="hdfs"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("query/", views.query, name="query"),
    path("ann3/", views.ann3, name="ann3"),
    path("ann5/", views.ann5, name="ann5"),
]
