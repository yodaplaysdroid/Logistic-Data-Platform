from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import *


def display_menu(request):
    return render(request, "menu.html")


def minio_input(request):
    if request.method == "POST":
        endpoint = request.POST.get("endpoint")
        accesskey = request.POST.get("accesskey")
        secretkey = request.POST.get("secretkey")
        filetype = request.POST.get("filetype")
        bucket = request.POST.get("bucket")
        path = request.POST.get("path")

        if filetype == "txt":
            minio_read_txt(endpoint, accesskey, secretkey, [bucket, path])

        elif filetype == "csv":
            minio_read_csv(endpoint, accesskey, secretkey, [bucket, path])

        elif filetype == "xls":
            minio_read_excel(endpoint, accesskey, secretkey, [bucket, path])

        return HttpResponseRedirect("/home/success/")

    return render(request, "minio.html")


def mysql_input(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        passwd = request.POST.get("password")
        host = request.POST.get("host")
        database = request.POST.get("database")

        with open("tmp", "w") as f:
            f.write(uname + passwd + host + database)

        mysql_get_data(uname, passwd, host, database)

        return HttpResponseRedirect("/home/success/")

    return render(request, "mysql.html")


def hdfs_input(request):
    if request.method == "POST":
        host = request.POST.get("host")
        port = request.POST.get("port")
        directory = request.POST.get("directory")
        filetype = request.POST.get("filetype")

        with open("tmp", "w") as f:
            f.write(host + port + directory + filetype)

        if filetype == "txt":
            if hdfs_read_txt(host, port, directory) == -1:
                return HttpResponseRedirect("/home/error/")

        elif filetype == "csv":
            if hdfs_read_csv(host, port, directory) == -1:
                return HttpResponseRedirect("/home/error/")

        return HttpResponseRedirect("/home/success/")

    return render(request, "hdfs.html")


def success(request):
    dm = Dameng()
    df = dm.get_all()
    output = str(df)
    return HttpResponse(output)
