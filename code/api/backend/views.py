from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
import json

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response


@csrf_exempt
def minio_input(request):
    if request.method == "POST":
        data = json.loads(request.body)
        endpoint = data.get("endpoint")
        accesskey = data.get("accesskey")
        secretkey = data.get("secretkey")
        filetype = data.get("filetype")
        bucket = data.get("bucket")
        path = data.get("path")

        with open("tmp", "w") as f:
            f.write(endpoint + accesskey + secretkey + filetype + bucket + path)

        if filetype == "txt":
            status = minio_read_txt(endpoint, accesskey, secretkey, [bucket, path])

        elif filetype == "csv":
            status = minio_read_csv(endpoint, accesskey, secretkey, [bucket, path])

        elif filetype == "xls":
            status = minio_read_excel(endpoint, accesskey, secretkey, [bucket, path])

        if status == 0:
            return JsonResponse(
                {"message": "data received successfully", "status": status}
            )
        else:
            return JsonResponse(
                {"message": "data received unsuccessfully", "status": status}
            )


@csrf_exempt
def mysql_input(request):
    if request.method == "POST":
        data = json.loads(request.body)
        uname = data.get("username")
        passwd = data.get("password")
        host = data.get("host")
        database = data.get("database")

        with open("tmp", "w") as f:
            f.write(uname + passwd + host + database)

        status = mysql_get_data(uname, passwd, host, database)
        if status == 0:
            return JsonResponse(
                {"message": "data received successfully", "status": status}
            )
        else:
            return JsonResponse(
                {"message": "data received unsuccessfully", "status": status}
            )


@csrf_exempt
def hdfs_input(request):
    if request.method == "POST":
        data = json.loads(request.body)
        host = data.get("host")
        port = data.get("port")
        directory = data.get("directory")
        filetype = data.get("filetype")

        with open("tmp", "w") as f:
            f.write(host + port + directory + filetype)

        if filetype == "txt":
            status = hdfs_read_txt(host, port, directory)

        elif filetype == "csv":
            status = hdfs_read_csv(host, port, directory)

        if status == 0:
            return JsonResponse(
                {"message": "data received successfully", "status": status}
            )
        else:
            return JsonResponse(
                {"message": "data received unsuccessfully", "status": status}
            )
