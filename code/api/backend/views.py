from django.http import JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def dashboard(request):
    if request.method == "POST":
        data = json.loads(request.body)
        refresh = data.get("refresh")
        if refresh == 1:
            Dameng().set_count()

    result = Dameng().get_count()
    return JsonResponse(
        {
            "t1": result[0][1],
            "t2": result[1][1],
            "t3": result[2][1],
            "t4": result[3][1],
            "t5": result[4][1],
            "t6": result[5][1],
        }
    )


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
        istest = data.get("test")

        if istest == 1:
            status = minio_connect(endpoint, accesskey, secretkey)
            if status == 0:
                return JsonResponse(
                    {
                        "message": "[SUCCESS] Connection to MinIO success!",
                        "status": status,
                    }
                )
            else:
                return JsonResponse(
                    {
                        "message": "[ERROR] Connection Error! Please check your entries and make sure no errors",
                        "status": status,
                    }
                )

        if filetype == "txt":
            status = minio_read_txt(endpoint, accesskey, secretkey, [bucket, path])

        elif filetype == "csv":
            status = minio_read_csv(endpoint, accesskey, secretkey, [bucket, path])

        elif filetype == "xls":
            status = minio_read_excel(endpoint, accesskey, secretkey, [bucket, path])

        if status == 0:
            return JsonResponse(
                {"message": "[SUCCESS] Data received successfully!", "status": status}
            )
        elif status == -1:
            return JsonResponse(
                {
                    "message": "[ERROR] Data received unsuccessfully! Please check your directory and make sure it is entered correctly",
                    "status": status,
                }
            )
        else:
            return JsonResponse(
                {
                    "message": "[ERROR] Data received unsuccessfully! Please check your files whether formatted correctly or records violated contraints",
                    "status": status,
                }
            )


@csrf_exempt
def mysql_input(request):
    if request.method == "POST":
        data = json.loads(request.body)
        uname = data.get("username")
        passwd = data.get("password")
        host = data.get("host")
        database = data.get("database")
        istest = data.get("test")

        with open("tmp", "w") as f:
            f.write(uname + passwd + host + database)

        if istest == 1:
            status = mysql_connect(uname, passwd, host, database)
            if status == 0:
                return JsonResponse(
                    {
                        "message": "[SUCCESS] Connection to MySQL success!",
                        "status": status,
                    }
                )
            else:
                return JsonResponse(
                    {
                        "message": "[ERROR] Connection Error! Please check your entries and make sure no errors",
                        "status": status,
                    }
                )

        status = mysql_get_data(uname, passwd, host, database)
        if status == 0:
            return JsonResponse(
                {"message": "[SUCCESS] Data received successfully!", "status": status}
            )
        else:
            return JsonResponse(
                {
                    "message": "[ERROR] Data received unsuccessfully! Please check your tables whether formatted correctly or records violated contraints",
                    "status": status,
                }
            )


@csrf_exempt
def hdfs_input(request):
    if request.method == "POST":
        data = json.loads(request.body)
        host = data.get("host")
        port = data.get("port")
        directory = data.get("directory")
        filetype = data.get("filetype")
        istest = data.get("test")

        if istest == 1:
            status = hdfs_connect(host, port, directory)
            if status == 0:
                return JsonResponse(
                    {
                        "message": "[SUCCESS] Connection to HDFS Success!",
                        "status": status,
                    }
                )
            else:
                return JsonResponse(
                    {
                        "message": "[ERROR] Connection Error! Please check your entries and make sure no errors",
                        "status": status,
                    }
                )

        if filetype == "txt":
            status = hdfs_read_txt(host, port, directory)

        elif filetype == "csv":
            status = hdfs_read_csv(host, port, directory)

        if status == 0:
            return JsonResponse(
                {"message": "[SUCCESS] Data received successfully!", "status": status}
            )
        else:
            return JsonResponse(
                {
                    "message": "[ERROR] Data received unsuccessfully! Please ensure your HDFS is connected and make sure the files are structured properly",
                    "status": status,
                }
            )
