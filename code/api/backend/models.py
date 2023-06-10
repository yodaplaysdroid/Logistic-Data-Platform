import dmPython
from pyspark.sql import SparkSession
from minio import Minio
import pandas as pd
import mysql.connector


class Dameng:
    def __init__(self, username="weiyin", password="lamweiyin"):
        self.username = username
        self.password = password

    def __connect(self):
        try:
            conn = dmPython.connect(
                user=self.username,
                password=self.password,
                server="localhost",
                port=5236,
                autoCommit=True,
            )
            return conn
        except Exception as e:
            print(e)
            return -1

    def query(self, sqlquery):
        conn = self.__connect()
        cursor = conn.cursor()

        try:
            cursor.execute(sqlquery)
        except Exception as e:
            print(e)
            return -1

        results = cursor.fetchall()
        conn.close()
        return results

    def exec(self, sqlquery):
        conn = self.__connect()
        cursor = conn.cursor()
        try:
            cursor.execute(sqlquery)
        except Exception as e:
            print(e)
            return -1

        conn.close()
        return 0

    def get_all(self):
        df = []
        tables = ("物流公司", "客户信息", "物流信息", "集装箱动态", "装货表", "卸货表")
        for table in tables:
            df.append(self.query(f"select * from {table}"))
        return df


def hdfs_read_csv(server, port, directory):
    conn = SparkSession.builder.appName("base").getOrCreate()
    dm = Dameng("weiyin", "lamweiyin")

    tables = ("物流公司", "客户信息", "物流信息", "集装箱动态", "装货表", "卸货表")
    count = 0

    try:
        for table in tables:
            conn.read.format("csv").option("header", "true").load(
                f"hdfs://{server}:{port}/{directory}/{table}.csv"
            )
    except Exception as e:
        print("Connection Error / File Not Found:", e)
        return -1

    df = (
        conn.read.format("csv")
        .option("header", "true")
        .load(f"hdfs://{server}:{port}/{directory}/物流公司.csv")
    )
    rows = df.collect()
    values = [[row[i] for i in range(len(row))] for row in rows]
    for r in values:
        count += dm.exec(
            f"insert into 物流公司 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}')"
        )

    df = (
        conn.read.format("csv")
        .option("header", "true")
        .load(f"hdfs://{server}:{port}/{directory}/客户信息.csv")
    )
    rows = df.collect()
    values = [[row[i] for i in range(len(row))] for row in rows]
    for r in values:
        count += dm.exec(
            f"insert into 客户信息 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}')"
        )

    df = (
        conn.read.format("csv")
        .option("header", "true")
        .load(f"hdfs://{server}:{port}/{directory}/物流信息.csv")
    )
    rows = df.collect()
    values = [[row[i] for i in range(len(row))] for row in rows]
    for r in values:
        count += dm.exec(
            f"insert into 物流信息 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}')"
        )

    df = (
        conn.read.format("csv")
        .option("header", "true")
        .load(f"hdfs://{server}:{port}/{directory}/集装箱动态.csv")
    )
    rows = df.collect()
    values = [[row[i] for i in range(len(row))] for row in rows]
    for r in values:
        count += dm.exec(
            f"insert into 集装箱动态 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}')"
        )

    df = (
        conn.read.format("csv")
        .option("header", "true")
        .load(f"hdfs://{server}:{port}/{directory}/装货表.csv")
    )
    rows = df.collect()
    values = [[row[i] for i in range(len(row))] for row in rows]
    for r in values:
        count += dm.exec(
            f"insert into 装货表 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}', '{r[7]}', '{r[8]}', '{r[9]}', '{r[10]}', '{r[11]}')"
        )

    df = (
        conn.read.format("csv")
        .option("header", "true")
        .load(f"hdfs://{server}:{port}/{directory}/卸货表.csv")
    )
    rows = df.collect()
    values = [[row[i] for i in range(len(row))] for row in rows]
    for r in values:
        count += dm.exec(
            f"insert into 卸货表 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}', '{r[7]}', '{r[8]}', '{r[9]}', '{r[10]}', '{r[11]}')"
        )

    conn.stop()
    return count


def hdfs_read_txt(server, port, directory):
    conn = SparkSession.builder.appName("base").getOrCreate()
    dm = Dameng("weiyin", "lamweiyin")

    tables = ("物流公司", "客户信息", "物流信息", "集装箱动态", "装货表", "卸货表")
    count = 0

    try:
        for table in tables:
            conn.read.format("csv").option("header", "true").load(
                f"hdfs://{server}:{port}/{directory}/{table}.csv"
            )
    except Exception as e:
        print("Connection Error / File Not Exist:", e)
        return -1

    df = (
        conn.read.format("csv")
        .option("header", "true")
        .option("delimiter", "\t")
        .load(f"hdfs://{server}:{port}/{directory}/物流公司.txt")
    )
    rows = df.collect()
    values = [[row[i] for i in range(len(row))] for row in rows]
    for r in values:
        count += dm.exec(
            f"insert into 物流公司 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}')"
        )

    df = (
        conn.read.format("csv")
        .option("header", "true")
        .option("delimiter", "\t")
        .load(f"hdfs://{server}:{port}/{directory}/客户信息.txt")
    )
    rows = df.collect()
    values = [[row[i] for i in range(len(row))] for row in rows]
    for r in values:
        count += dm.exec(
            f"insert into 客户信息 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}')"
        )

    df = (
        conn.read.format("csv")
        .option("header", "true")
        .option("delimiter", "\t")
        .load(f"hdfs://{server}:{port}/{directory}/物流信息.txt")
    )
    rows = df.collect()
    values = [[row[i] for i in range(len(row))] for row in rows]
    for r in values:
        count += dm.exec(
            f"insert into 物流信息 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}')"
        )

    df = (
        conn.read.format("csv")
        .option("header", "true")
        .option("delimiter", "\t")
        .load(f"hdfs://{server}:{port}/{directory}/集装箱动态.txt")
    )
    rows = df.collect()
    values = [[row[i] for i in range(len(row))] for row in rows]
    for r in values:
        count += dm.exec(
            f"insert into 集装箱动态 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}')"
        )

    df = (
        conn.read.format("csv")
        .option("header", "true")
        .option("delimiter", "\t")
        .load(f"hdfs://{server}:{port}/{directory}/装货表.txt")
    )
    rows = df.collect()
    values = [[row[i] for i in range(len(row))] for row in rows]
    for r in values:
        count += dm.exec(
            f"insert into 装货表 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}', '{r[7]}', '{r[8]}', '{r[9]}', '{r[10]}', '{r[11]}')"
        )

    df = (
        conn.read.format("csv")
        .option("header", "true")
        .option("delimiter", "\t")
        .load(f"hdfs://{server}:{port}/{directory}/卸货表.txt")
    )
    rows = df.collect()
    values = [[row[i] for i in range(len(row))] for row in rows]
    for r in values:
        count += dm.exec(
            f"insert into 卸货表 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}', '{r[7]}', '{r[8]}', '{r[9]}', '{r[10]}', '{r[11]}')"
        )

    conn.stop()
    return count


def minio_read_excel(endpoint, access_key, secret_key, path):
    try:
        conn = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=False,
        )
    except Exception as e:
        print("Connection Error:", e)
        return -1

    dm = Dameng("weiyin", "lamweiyin")

    try:
        conn.fget_object(path[0], path[1], "tmp")
    except Exception as e:
        print(e)
        return -1

    tables = ("物流公司", "客户信息", "物流信息", "集装箱动态", "装货表", "卸货表")
    try:
        for table in tables:
            pd.read_excel("tmp", sheet_name=table)

    except Exception as e:
        print("Sheets missing: ", e)
        return -2

    count = 0

    df = pd.read_excel("tmp", sheet_name="物流公司")
    for i, r in df.iterrows():
        count += dm.exec(
            f"insert into 物流公司 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}')"
        )

    df = pd.read_excel("tmp", sheet_name="客户信息")
    for i, r in df.iterrows():
        count += dm.exec(
            f"insert into 客户信息 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}')"
        )

    df = pd.read_excel("tmp", sheet_name="物流信息")
    for i, r in df.iterrows():
        count += dm.exec(
            f"insert into 物流信息 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}')"
        )

    df = pd.read_excel("tmp", sheet_name="集装箱动态")
    for i, r in df.iterrows():
        count += dm.exec(
            f"insert into 集装箱动态 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}')"
        )

    df = pd.read_excel("tmp", sheet_name="装货表")
    for i, r in df.iterrows():
        count += dm.exec(
            f"insert into 装货表 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}', '{r[7]}', '{r[8]}', '{r[9]}', '{r[10]}', '{r[11]}')"
        )

    df = pd.read_excel("tmp", sheet_name="卸货表")
    for i, r in df.iterrows():
        count += dm.exec(
            f"insert into 卸货表 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}', '{r[7]}', '{r[8]}', '{r[9]}', '{r[10]}', '{r[11]}')"
        )

    return count


def minio_read_csv(endpoint, access_key, secret_key, directory):
    try:
        conn = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=False,
        )
    except Exception as e:
        print("Connection Error:", e)
        return -1

    dm = Dameng("weiyin", "lamweiyin")

    tables = ("集装箱动态", "客户信息", "物流公司", "物流信息", "卸货表", "装货表")
    try:
        for table in tables:
            conn.fget_object(directory[0], f"{directory[1]}/{table}.csv", "tmp")
    except Exception as e:
        print("Object Not Found:", e)
        return -2

    count = 0

    conn.fget_object(directory[0], f"{directory[1]}/物流公司.csv", "tmp")
    df = pd.read_csv("tmp")
    for i, r in df.iterrows():
        count += dm.exec(
            f"insert into 物流公司 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}')"
        )

    conn.fget_object(directory[0], f"{directory[1]}/客户信息.csv", "tmp")
    df = pd.read_csv("tmp")
    for i, r in df.iterrows():
        count += dm.exec(
            f"insert into 客户信息 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}')"
        )

    conn.fget_object(directory[0], f"{directory[1]}/物流信息.csv", "tmp")
    df = pd.read_csv("tmp")
    for i, r in df.iterrows():
        count += dm.exec(
            f"insert into 物流信息 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}')"
        )

    conn.fget_object(directory[0], f"{directory[1]}/集装箱动态.csv", "tmp")
    df = pd.read_csv("tmp")
    for i, r in df.iterrows():
        count += dm.exec(
            f"insert into 集装箱动态 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}')"
        )

    conn.fget_object(directory[0], f"{directory[1]}/装货表.csv", "tmp")
    df = pd.read_csv("tmp")
    for i, r in df.iterrows():
        count += dm.exec(
            f"insert into 装货表 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}', '{r[7]}', '{r[8]}', '{r[9]}', '{r[10]}', '{r[11]}')"
        )

    conn.fget_object(directory[0], f"{directory[1]}/卸货表.csv", "tmp")
    df = pd.read_csv("tmp")
    for i, r in df.iterrows():
        count += dm.exec(
            f"insert into 卸货表 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}', '{r[7]}', '{r[8]}', '{r[9]}', '{r[10]}', '{r[11]}')"
        )

    return count


def minio_read_txt(endpoint, access_key, secret_key, directory):
    try:
        conn = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=False,
        )
    except Exception as e:
        print("Connection Error:", e)
        return -1
    dm = Dameng("weiyin", "lamweiyin")

    tables = ("集装箱动态", "客户信息", "物流公司", "物流信息", "卸货表", "装货表")
    try:
        for table in tables:
            conn.fget_object(directory[0], f"{directory[1]}/{table}.txt", "tmp")
    except Exception as e:
        print("Object Not Found:", e)
        return -2

    count = 0

    conn.fget_object(directory[0], f"{directory[1]}/物流公司.txt", "tmp")
    df = pd.read_csv("tmp", delimiter="\t")
    for i, r in df.iterrows():
        count += dm.exec(
            f"insert into 物流公司 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}')"
        )

    conn.fget_object(directory[0], f"{directory[1]}/客户信息.txt", "tmp")
    df = pd.read_csv("tmp", delimiter="\t")
    for i, r in df.iterrows():
        count += dm.exec(
            f"insert into 客户信息 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}')"
        )

    conn.fget_object(directory[0], f"{directory[1]}/物流信息.txt", "tmp")
    df = pd.read_csv("tmp", delimiter="\t")
    for i, r in df.iterrows():
        count += dm.exec(
            f"insert into 物流信息 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}')"
        )

    conn.fget_object(directory[0], f"{directory[1]}/集装箱动态.txt", "tmp")
    df = pd.read_csv("tmp", delimiter="\t")
    for i, r in df.iterrows():
        count += dm.exec(
            f"insert into 集装箱动态 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}')"
        )

    conn.fget_object(directory[0], f"{directory[1]}/装货表.txt", "tmp")
    df = pd.read_csv("tmp", delimiter="\t")
    for i, r in df.iterrows():
        count += dm.exec(
            f"insert into 装货表 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}', '{r[7]}', '{r[8]}', '{r[9]}', '{r[10]}', '{r[11]}')"
        )

    conn.fget_object(directory[0], f"{directory[1]}/卸货表.txt", "tmp")
    df = pd.read_csv("tmp", delimiter="\t")
    for i, r in df.iterrows():
        count += dm.exec(
            f"insert into 卸货表 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}', '{r[7]}', '{r[8]}', '{r[9]}', '{r[10]}', '{r[11]}')"
        )

    return count


def mysql_get_data(uname, passwd, host, database):
    try:
        conn = mysql.connector.connect(
            user=uname, password=passwd, host=host, database=database
        )
    except Exception as e:
        print("Connection Error: ", e)
        return -1

    dm = Dameng("weiyin", "lamweiyin")
    tables = ("集装箱动态", "客户信息", "物流公司", "物流信息", "卸货表", "装货表")

    cursor = conn.cursor()
    try:
        for table in tables:
            cursor.execute(f"select * from {table}")
            cursor.fetchall()
    except Exception as e:
        print("Tables missing", e)
        return -2

    count = 0

    cursor.execute("select * from 物流公司")
    for a, b, c, d, e in cursor.fetchall():
        count += dm.exec(f"insert into 物流公司 values ('{a}', '{b}', '{c}', '{d}', '{e}')")

    cursor.execute("select * from 客户信息")
    for a, b, c, d in cursor.fetchall():
        count += dm.exec(f"insert into 客户信息 values ('{a}', '{b}', '{c}', '{d}')")

    cursor.execute("select * from 物流信息")
    for a, b, c, d, e, f, g in cursor.fetchall():
        count += dm.exec(
            f"insert into 物流信息 values ('{a}', '{b}', '{c}', '{d}', '{e}', '{f}', '{g}')"
        )

    cursor.execute("select * from 集装箱动态")
    for a, b, c, d, e, f, g in cursor.fetchall():
        count += dm.exec(
            f"insert into 集装箱动态 values ('{a}', '{b}', '{c}', '{d}', '{e}', '{f}', '{g}')"
        )

    cursor.execute("select * from 卸货表")
    for a, b, c, d, e, f, g, h, i, j, k, l in cursor.fetchall():
        count += dm.exec(
            f"insert into 卸货表 values ('{a}', '{b}', '{c}', '{d}', '{e}', '{f}', '{g}', '{h}', '{i}', '{j}', '{k}', '{l}')"
        )

    cursor.execute("select * from 装货表")
    for a, b, c, d, e, f, g, h, i, j, k, l in cursor.fetchall():
        count += dm.exec(
            f"insert into 装货表 values ('{a}', '{b}', '{c}', '{d}', '{e}', '{f}', '{g}', '{h}', '{i}', '{j}', '{k}', '{l}')"
        )

    conn.close()
    return count


if __name__ == "__main__":
    print(Dameng().get_all())
