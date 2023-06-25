from django.http import JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def dashboard(request):
    Dameng().set_count()

    res = Dameng().get_dashboard_info()
    return JsonResponse(res)


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


@csrf_exempt
def query(request):
    if request.method == "POST":
        query = json.loads(request.body).get("query")
        print(query)
        dm = Dameng()
        dm.connect()
        results = dm.query(query)
        dm.close()
        res = {}
        for r in results:
            res[r[0]] = r[0]
    return JsonResponse(res)


@csrf_exempt
def ann3(request):
    if request.method == "POST":
        data = json.loads(request.body)
        year1 = data.get("year1")
        month1 = data.get("month1")
        year2 = data.get("year2")
        month2 = data.get("month2")
        dm = Dameng()
        dm.connect()
        print(data)
        if year1 != "" and year2 != "":
            dm.exec("drop view 分析3")
            dm.exec(
                f"""create view 分析3 as
                select s1.货物名称, sum(s1.总货重) as y1, sum(s2.总货重) as y2, (sum(s2.总货重) - sum(s1.总货重)) as y3 from
                (select * from 分析三 where 年月 = '{year1}-{month1}') as s1,
                (select * from 分析三 where 年月 = '{year2}-{month2}') as s2
                where s1.货物名称 = s2.货物名称
                group by s1.货物名称"""
            )
            dm.close()
            return JsonResponse(
                {
                    "status": 0,
                }
            )
        elif year1 == "" and year2 == "":
            dm.exec("drop view 分析3")
            dm.exec(
                f"""create view 分析3 as
                select s1.货物名称, sum(s1.总货重) as y1, sum(s2.总货重) as y2, (sum(s2.总货重) - sum(s1.总货重)) as y3 from
                (select * from 分析三 where 年月 like '%-{month1}%') as s1,
                (select * from 分析三 where 年月 like '%-{month2}%') as s2
                where s1.货物名称 = s2.货物名称
                group by s1.货物名称"""
            )
            dm.close()
            return JsonResponse(
                {
                    "status": 0,
                }
            )
        else:
            dm.close()
            return JsonResponse(
                {
                    "status": 1,
                }
            )


@csrf_exempt
def ann5(request):
    if request.method == "POST":
        data = json.loads(request.body)
        col = data.get("col")
        val = data.get("val")
        dm = Dameng()
        dm.connect()
        print(data)
        if col == "堆存港口":
            dm.exec("drop view 分析5")
            dm.exec(
                f"""create view 分析5 as select 货物名称 as x, 数量吞吐量, 总货重 from 分析五 where 堆存港口 = '{val}'"""
            )
            dm.close()
            return JsonResponse(
                {
                    "status": 0,
                }
            )
        elif col == "货物名称":
            dm.exec("drop view 分析5")
            dm.exec(
                f"""create view 分析5 as select 堆存港口 as x, 数量吞吐量, 总货重 from 分析五 where 货物名称 = '{val}'"""
            )
            dm.close()
            return JsonResponse(
                {
                    "status": 0,
                }
            )
        else:
            dm.close()
            return JsonResponse(
                {
                    "status": 1,
                }
            )
