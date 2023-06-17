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
        directory = data.get("directory")
        table = data.get("table")
        sheet_name = data.get("sheetname")
        istest = data.get("test")

        print(data)

        if istest == 1:
            status = minio_connect(endpoint, accesskey, secretkey)
            if status == 0:
                return JsonResponse(
                    {
                        "message": "连接成功！",
                        "status": status,
                    }
                )
            else:
                return JsonResponse(
                    {
                        "message": "连接失败。",
                        "status": status,
                    }
                )

        status = minio_read(
            endpoint,
            accesskey,
            secretkey,
            bucket,
            directory,
            table,
            filetype,
            sheet_name,
        )

        if status == 0:
            return JsonResponse({"message": "数据迁移成功！", "status": status})
        elif status == -1:
            return JsonResponse(
                {
                    "message": "数据迁移失败：文件不存在",
                    "status": status,
                }
            )
        else:
            return JsonResponse(
                {
                    "message": "数据存在不合格的格式，或不遵守约束条件",
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
        input_table = data.get("inputtable")
        output_table = data.get("outputtable")
        istest = data.get("test")

        print(data)

        if istest == 1:
            status = mysql_connect(uname, passwd, host, database)
            if status == 0:
                return JsonResponse(
                    {
                        "message": "连接成功！",
                        "status": status,
                    }
                )
            else:
                return JsonResponse(
                    {
                        "message": "连接失败。",
                        "status": status,
                    }
                )

        status = mysql_get_data(
            uname, passwd, host, database, input_table, output_table
        )
        if status == 0:
            return JsonResponse({"message": "数据迁移成功！", "status": status})
        elif status == -2:
            return JsonResponse(
                {
                    "message": "数据迁移失败：表格不存在",
                    "status": status,
                }
            )
        else:
            return JsonResponse(
                {
                    "message": "数据存在不合格的格式，或不遵守约束条件",
                    "status": status,
                }
            )


@csrf_exempt
def hdfs_input(request):
    if request.method == "POST":
        data = json.loads(request.body)
        endpoint = data.get("endpoint")
        directory = data.get("directory")
        filename = data.get("filename")
        filetype = data.get("filetype")
        sheet_name = data.get("sheetname")
        table = data.get("table")
        istest = data.get("test")

        print(data)

        if istest == 1:
            status = hdfs_connect(directory, filename)
            if status == 0:
                return JsonResponse(
                    {
                        "message": "连接成功！",
                        "status": status,
                    }
                )
            else:
                return JsonResponse(
                    {
                        "message": "连接失败。",
                        "status": status,
                    }
                )

        status = hdfs_read(directory, filetype, filename, table, sheet_name)

        if status == 0:
            return JsonResponse({"message": "数据导入成功！", "status": status})
        elif status == -1:
            return JsonResponse(
                {
                    "message": "数据导入失败：文件不存在",
                    "status": status,
                }
            )
        else:
            return JsonResponse(
                {
                    "message": "数据存在不合格的格式，或不遵守约束条件",
                    "status": status,
                }
            )
