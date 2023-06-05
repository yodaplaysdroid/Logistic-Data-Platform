from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .scripts.input.db import *
from .scripts.input.minio import *
from .scripts.input.hdfs import *
from .scripts.input.mysql import *


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
            status = minio_read_txt(endpoint, accesskey, secretkey, [bucket, path])

        elif filetype == "csv":
            status = minio_read_csv(endpoint, accesskey, secretkey, [bucket, path])

        elif filetype == "xls":
            status = minio_read_excel(endpoint, accesskey, secretkey, [bucket, path])

        if status == 0:
            return HttpResponseRedirect("/home/success/")
        else:
            return HttpResponseRedirect("/home/error/")

    return render(request, "minio.html")


def mysql_input(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        passwd = request.POST.get("password")
        host = request.POST.get("host")
        database = request.POST.get("database")

        with open("tmp", "w") as f:
            f.write(uname + passwd + host + database)

        if mysql_get_data(uname, passwd, host, database) == 0:
            return HttpResponseRedirect("/home/success/")
        else:
            return HttpResponseRedirect("/home/error/")

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
            status = hdfs_read_txt(host, port, directory)

        elif filetype == "csv":
            status = hdfs_read_csv(host, port, directory)

        if status == 0:
            return HttpResponseRedirect("/home/success/")
        else:
            return HttpResponseRedirect("/home/error/")

    return render(request, "hdfs.html")


def success(request):
    dm = Dameng()
    df = dm.get_all()
    output = str(df)
    return render(request, "success.html", {"output": output})


def error(request):
    return render(request, "error.html")


def refresh(request):
    delete_user("weiyin")
    create_user("weiyin", "lamweiyin")
    Dameng().create_tables()
    return HttpResponseRedirect("/home/success/")


def debug(request):
    return render(request, "debug.html")
