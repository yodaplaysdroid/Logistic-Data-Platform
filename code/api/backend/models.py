import dmPython
from minio import Minio
import pandas as pd
import mysql.connector
import os
from datetime import datetime


class Dameng:
    def __init__(
        self,
        username="weiyin",
        password="lamweiyin",
        server="36.140.31.145",
        port=31826,
    ):
        self.username = username
        self.password = password
        self.server = server
        self.port = port

    def connect(self):
        try:
            self.conn = dmPython.connect(
                user=self.username,
                password=self.password,
                server=self.server,
                port=self.port,
                autoCommit=True,
            )
            self.cursor = self.conn.cursor()
            return 0
        except Exception as e:
            print(e)
            return 99

    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            print(e)
            return 99

    def query(self, sqlquery):
        try:
            self.cursor.execute(sqlquery)
        except Exception as e:
            print(e)
            return 1

        results = self.cursor.fetchall()
        return results

    def exec(self, sqlquery):
        try:
            self.cursor.execute(sqlquery)
            return 0
        except Exception as e:
            print(e)
            return 1

    def get_count(self):
        self.connect()
        result = {}
        result["记录数量"] = self.query("select * from 记录信息")
        self.close()
        return result

    def set_count(self):
        df = []
        tables = ("物流公司", "客户信息", "物流信息", "集装箱动态", "装货表", "卸货表")
        print(self.connect())
        for table in tables:
            df.append(self.query(f"select count(*) from {table}"))
            print(df)
        for i in range(6):
            self.exec(f"update 记录信息 set 记录个数 = {df[i][0][0]} where 表名 = '{tables[i]}'")
            self.exec("commit")
        self.close()

    def get_dashboard_info(self):
        res = {}
        self.connect()
        tmp = self.query("select 记录个数 from 记录信息")
        res["记录数量"] = [x[0] for x in tmp]
        tmp = self.query(
            """select 货物名称, count(货重_吨)
            from 集装箱动态, 物流信息
            where 物流信息.提单号 = 集装箱动态.提单号
            and 操作日期 in (
                select distinct 操作日期
                from 集装箱动态
                where substring(操作日期, 1, 7) in (
                    select distinct 年月
                    from 分析三
                    order by 年月 desc
                    limit 3))
            group by 货物名称
            order by count(货重_吨) desc
            limit 3"""
        )
        res["港口排行"] = [[x[0], x[1]] for x in tmp]
        tmp = self.query(
            """select 货物名称, count(总货重), sum(总货重)
            from 分析三 where 年月 in (
                select distinct 年月
                from 分析三
                order by 年月 desc
                limit 3)
            group by 货物名称
            order by count(总货重) desc
            limit 3"""
        )
        res["货物排行"] = [[x[0], x[1], int(x[2] * 100) / 100] for x in tmp]
        tmp = self.query(
            """select substring(省市区, 1, 2), count(提单号)
            from 客户信息, 物流信息
            where 货主代码=客户编号
            group by substring(省市区, 1, 2)
            order by count(提单号) desc
            limit 3"""
        )
        res["各省消费"] = [[x[0], x[1]] for x in tmp]
        tmp = self.query(
            """select 堆存港口, count(提单号)
            from 集装箱动态
            where 操作='入库'
            group by 堆存港口
            order by count(提单号) desc
            limit 3"""
        )
        res["入库排行"] = [[x[0], x[1]] for x in tmp]
        tmp = self.query(
            """select 堆存港口, count(提单号)
            from 集装箱动态
            where 操作='出库'
            group by 堆存港口
            order by count(提单号) desc
            limit 3"""
        )
        res["出库排行"] = [[x[0], x[1]] for x in tmp]
        tmp = self.query(
            """select substring(装货表.作业开始时间, 1, 7), avg(datediff(day, 装货表.作业开始时间, 卸货表.作业结束时间)) as 时间
            from 装货表, 卸货表
            where 装货表.提单号 = 卸货表.提单号
            group by substring(装货表.作业开始时间, 1, 7)
            order by substring(装货表.作业开始时间, 1, 7)"""
        )
        res["时间周期"] = [[], []]
        for x in tmp:
            res["时间周期"][0].append(x[0])
            res["时间周期"][1].append(x[1])
        self.close()
        return res


def is_id_valid(id):
    province = (
        list(range(11, 16))
        + list(range(21, 24))
        + list(range(31, 38))
        + list(range(41, 47))
        + list(range(50, 55))
        + list(range(61, 66))
        + [71, 81, 82]
    )
    state = list(range(0, 91))
    city = list(range(1, 100))

    def verify(id):
        sum = 0
        wi = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        for i in range(17):
            sum += int(id[i]) * wi[i]
        j = sum % 11
        rem = ["1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2"]
        return id[17] == rem[j]

    def is_valid_date(date_string):
        try:
            datetime.strptime(date_string, "%Y%m%d")
            return True
        except ValueError:
            return False

    if int(id[0:2]) not in province:
        return False
    if int(id[2:4]) not in state:
        return False
    if int(id[4:6]) not in city:
        return False
    if not is_valid_date(id[6:14]):
        return False
    try:
        int(id[14:17])
    except:
        return False
    if not verify(id):
        return False
    return True


def hdfs_connect(directory, filename):
    try:
        if os.system(f"rclone copy {directory}{filename} /tmp") == 0:
            return 0
        else:
            return -1
    except Exception as e:
        print("Connection Error / File Not Found:", e)
        return -1


def hdfs_read(directory, filetype, filename, table, sheet_name):
    try:
        os.system(f"rclone copy {directory}{filename} /tmp")
        os.system(f"mv /tmp/{filename} /tmp/hdfs")
    except Exception as e:
        print("Connection Error / File Not Found:", e)
        return -1

    dm = Dameng("weiyin", "lamweiyin")
    if dm.connect() == 99:
        return 99

    count = 0

    if filetype == "csv":
        try:
            df = pd.read_csv("/tmp/hdfs", encoding="gbk", quotechar="'")
        except Exception as e:
            try:
                df = pd.read_csv("/tmp/hdfs", quotechar="'")
            except Exception as f:
                print(f)
            print("File Reading Error", e)
            return 1

    elif filetype == "txt":
        try:
            df = pd.read_csv("/tmp/hdfs", sep="\t", encoding="gbk", quotechar="'")
        except Exception as e:
            try:
                df = pd.read_csv("/tmp/hdfs", sep="\t", quotechar="'")
            except Exception as f:
                print(f)
            print("File Reading Error", e)
            return 1

    else:
        try:
            df = pd.read_excel("/tmp/hdfs", sheet_name=sheet_name)
        except Exception as e:
            print("File Reading Error", e)
            return 1

    count = 0
    if table == "物流公司":
        for i, r in df.iterrows():
            count += dm.exec(
                f"insert into 物流公司 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}')"
            )
            print(i)

    elif table == "客户信息":
        for i, r in df.iterrows():
            if is_id_valid(r[1]):
                count += dm.exec(
                    f"insert into 客户信息 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}')"
                )
            else:
                count += 1
                dm.exec(
                    f"insert into 假客户信息 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}')"
                )
            print(i)

    elif table == "物流信息":
        for i, r in df.iterrows():
            count += dm.exec(
                f"insert into 物流信息 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}')"
            )
            print(i)

    elif table == "集装箱动态":
        for i, r in df.iterrows():
            count += dm.exec(
                f"insert into 集装箱动态 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}')"
            )
            print(i)

    elif table == "装货表":
        for i, r in df.iterrows():
            count += dm.exec(
                f"insert into 装货表 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}', '{r[7]}', '{r[8]}', '{r[9]}', '{r[10]}', '{r[11]}')"
            )
            print(i)

    elif table == "卸货表":
        for i, r in df.iterrows():
            count += dm.exec(
                f"insert into 卸货表 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}', '{r[7]}', '{r[8]}', '{r[9]}', '{r[10]}', '{r[11]}')"
            )
            print(i)

    dm.exec("commit")
    dm.close()
    return count


def minio_connect(endpoint, access_key, secret_key):
    conn = Minio(
        endpoint=endpoint,
        access_key=access_key,
        secret_key=secret_key,
        secure=False,
    )
    try:
        if not conn.bucket_exists("nonexistingbucket"):
            return 0
    except Exception as e:
        print(e)
        return -1


def minio_read(
    endpoint,
    access_key,
    secret_key,
    bucket,
    directory,
    table,
    filetype,
    sheet_name="",
):
    conn = Minio(
        endpoint=endpoint,
        access_key=access_key,
        secret_key=secret_key,
        secure=False,
    )
    try:
        if not conn.bucket_exists("nonexistingbucket"):
            pass
    except Exception as e:
        print(e)
        return -1

    dm = Dameng("weiyin", "lamweiyin")
    if dm.connect() == 99:
        return 99

    try:
        conn.fget_object(bucket, directory, "/tmp/minio")
    except Exception as e:
        print(e)
        return -2

    if filetype == "txt":
        try:
            df = pd.read_csv("/tmp/minio", sep="\t", encoding="gbk", quotechar="'")

        except Exception as e:
            try:
                df = pd.read_csv("/tmp/minio", sep="\t", quotechar="'")

            except Exception as f:
                print(f)

            print(e)
            return 1

    elif filetype == "csv":
        try:
            df = pd.read_csv("/tmp/minio", encoding="gbk", quotechar="'")

        except Exception as e:
            try:
                df = pd.read_csv("/tmp/minio", sep="\t", quotechar="'")

            except Exception as f:
                print(f)

            print(e)
            return 1

    else:
        try:
            df = pd.read_excel("/tmp/minio", sheet_name=sheet_name)

        except Exception as e:
            print("Sheets missing: ", e)
            return 1

    count = 0
    if table == "物流公司":
        for i, r in df.iterrows():
            count += dm.exec(
                f"insert into 物流公司 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}')"
            )
            print(i)

    elif table == "客户信息":
        for i, r in df.iterrows():
            if is_id_valid(r[1]):
                count += dm.exec(
                    f"insert into 客户信息 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}')"
                )
            else:
                count += 1
                dm.exec(
                    f"insert into 假客户信息 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}')"
                )
            print(i)

    elif table == "物流信息":
        for i, r in df.iterrows():
            count += dm.exec(
                f"insert into 物流信息 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}')"
            )
            print(i)

    elif table == "集装箱动态":
        for i, r in df.iterrows():
            count += dm.exec(
                f"insert into 集装箱动态 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}')"
            )
            print(i)

    elif table == "装货表":
        for i, r in df.iterrows():
            count += dm.exec(
                f"insert into 装货表 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}', '{r[7]}', '{r[8]}', '{r[9]}', '{r[10]}', '{r[11]}')"
            )
            print(i)

    elif table == "卸货表":
        for i, r in df.iterrows():
            count += dm.exec(
                f"insert into 卸货表 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}', '{r[7]}', '{r[8]}', '{r[9]}', '{r[10]}', '{r[11]}')"
            )
            print(i)

    dm.exec("commit")
    dm.close()
    return count


def mysql_connect(uname, passwd, host, database):
    try:
        conn = mysql.connector.connect(
            user=uname, password=passwd, host=host, database=database
        )
        conn.close()
        return 0
    except Exception as e:
        print("Connection Error: ", e)
        return -1


def mysql_get_data(uname, passwd, host, database, input_table, output_table):
    try:
        conn = mysql.connector.connect(
            user=uname, password=passwd, host=host, database=database
        )
    except Exception as e:
        print("Connection Error: ", e)
        return -1

    dm = Dameng("weiyin", "lamweiyin")
    if dm.connect() == 99:
        return 99

    cursor = conn.cursor()
    try:
        cursor.execute(f"select * from {input_table}")
        results = cursor.fetchall()
    except Exception as e:
        print("Tables missing", e)
        return -2

    count = 0

    if output_table == "物流公司":
        for a, b, c, d, e in results:
            count += dm.exec(
                f"insert into 物流公司 values ('{a}', '{b}', '{c}', '{d}', '{e}')"
            )
            print(a)

    elif output_table == "客户信息":
        for a, b, c, d in results:
            if is_id_valid(b):
                count += dm.exec(
                    f"insert into 客户信息 values ('{a}', '{b}', '{c}', '{d}')"
                )
            else:
                count += 1
                dm.exec(f"insert into 假客户信息 values ('{a}', '{b}', '{c}', '{d}')")
            print(a)

    elif output_table == "物流信息":
        for a, b, c, d, e, f, g in results:
            count += dm.exec(
                f"insert into 物流信息 values ('{a}', '{b}', '{c}', '{d}', '{e}', '{f}', '{g}')"
            )
            print(a)

    elif output_table == "集装箱动态":
        for a, b, c, d, e, f, g in results:
            count += dm.exec(
                f"insert into 集装箱动态 values ('{a}', '{b}', '{c}', '{d}', '{e}', '{f}', '{g}')"
            )
            print(a)

    elif output_table == "卸货表":
        for a, b, c, d, e, f, g, h, i, j, k, l in results:
            count += dm.exec(
                f"insert into 卸货表 values ('{a}', '{b}', '{c}', '{d}', '{e}', '{f}', '{g}', '{h}', '{i}', '{j}', '{k}', '{l}')"
            )
            print(a)

    elif output_table == "装货表":
        for a, b, c, d, e, f, g, h, i, j, k, l in results:
            count += dm.exec(
                f"insert into 装货表 values ('{a}', '{b}', '{c}', '{d}', '{e}', '{f}', '{g}', '{h}', '{i}', '{j}', '{k}', '{l}')"
            )
            print(a)

    conn.close()
    dm.exec("commit")
    dm.close()
    return count


if __name__ == "__main__":
    res = Dameng().get_dashboard_info()
    print(res)
