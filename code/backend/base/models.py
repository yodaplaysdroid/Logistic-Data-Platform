from django.db import models
import pyodbc
from pyspark.sql import SparkSession
import pandas as pd
from minio import Minio
import mysql.connector


# Dameng数据库
class Dameng:
    def __init__(self, username="weiyin", password="lamweiyin"):
        self.username = username
        self.password = password

    # 建立数据库连接
    def __connect(self):
        try:
            server = "localhost"
            database = "DAMENG"
            driver = "{DM8 ODBC DRIVER}"
            connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={self.username};PWD={self.password}"
            conn = pyodbc.connect(connection_string)
            return conn
        except Exception as e:
            print(e)
            return -1

    # 创建初始表
    # 返回值count表示创建表时出错次数
    # 通常是因为表格已经存在所导致的
    def create_tables(self):
        count = 0
        try:
            self.query(
                """create table 物流公司 (
                公司名称 varchar(100) not null,
                客户编号 varchar(100) not null unique,
                联系人 varchar(100) not null,
                电话 varchar(100) not null,
                省市区 varchar(100) not null,
                primary key(公司名称))"""
            )
        except Exception as e:
            print(e)
            count += 1
        try:
            self.query(
                """create table 客户信息 (
                客户名称 varchar(100) not null,
                客户编号 varchar(100) not null,
                手机号 varchar(100) not null unique,
                省市区 varchar(100) not null,
                primary key(客户名称, 客户编号))"""
            )
        except Exception as e:
            print(e)
            count += 1
        try:
            self.query(
                """create table 物流信息 (
                提单号 varchar(100) not null,
                货主名称 varchar(100),
                货主代码 varchar(100),
                物流公司_货代 varchar(100),
                集装箱箱号 varchar(100) not null,
                货物名称 varchar(100) not null,
                货重_吨 varchar(100) not null,
                primary key(提单号))"""
            )
        except Exception as e:
            print(e)
            count += 1
        try:
            self.query(
                """create table 集装箱动态 (
                堆存港口 varchar(100) not null,
                集装箱箱号 varchar(100) not null,
                箱尺寸_TEU varchar(100) not null,
                提单号 varchar(100) not null,
                堆场位置 varchar(100) not null,
                操作 varchar(100) not null,
                操作日期 varchar(100) not null,
                primary key(集装箱箱号, 提单号, 操作))"""
            )
        except Exception as e:
            print(e)
            count += 1
        try:
            self.query(
                """create table 装货表 (
                船公司 varchar(100),
                船名称 varchar(100),
                作业开始时间 varchar(100),
                作业结束时间 varchar(100),
                始发时间 varchar(100),
                到达时间 varchar(100),
                作业港口 varchar(100),
                提单号 varchar(100) not null,
                集装箱箱号 varchar(100),
                箱尺寸_TEU varchar(100),
                启运地 varchar(100),
                目的地 varchar(100),
                primary key(提单号))"""
            )
        except Exception as e:
            print(e)
            count += 1
        try:
            self.query(
                """create table 卸货表 (
                船公司 varchar(100),
                船名称 varchar(100),
                作业开始时间 varchar(100),
                作业结束时间 varchar(100),
                始发时间 varchar(100),
                到达时间 varchar(100),
                作业港口 varchar(100),
                提单号 varchar(100) not null,
                集装箱箱号 varchar(100),
                箱尺寸_TEU varchar(100),
                启运地 varchar(100),
                目的地 varchar(100),
                primary key(提单号))"""
            )
        except Exception as e:
            print(e)
            count += 1

        return count

    # 执行sql语句
    def query(self, sqlquery):
        conn = self.__connect()
        cursor = conn.cursor()
        try:
            cursor.execute(sqlquery)
        except Exception as e:
            print(e)
            return -1

        try:
            results = cursor.fetchall()
        except Exception as e:
            print(e)

        cursor.execute("commit")
        conn.close()
        return results

    # 列出当前用户下所有的表
    def get_tables(self):
        return self.query(
            f"select NAME from sysobjects where \"SUBTYPE$\"='UTAB' AND SCHID=(SELECT ID FROM sysobjects WHERE NAME='{self.username.upper()}' AND TYPE$='SCH')"
        )

    # 列出所有用户
    def get_users(self):
        return self.query("select username from dba_users")

    # 列出所有表的所有内容
    def get_all(self):
        df = []
        tables = ("物流公司", "客户信息", "物流信息", "集装箱动态", "装货表", "卸货表")
        for table in tables:
            df.append(self.query(f"select * from {table}"))
        return df


# 创建新用户包括用户的默认表空间
def create_user(uname, passwd):
    su = Dameng(username="SYSDBA", password="SYSDBA001")

    try:
        su.query(
            f"create tablespace {uname} datafile '{uname}.dbf' size 256 autoextend on maxsize 10240"
        )
    except Exception as e:
        print(e)
        return -1

    try:
        su.query(
            f'create user {uname} identified by "{passwd}" default tablespace {uname} default index tablespace {uname}'
        )
    except Exception as e:
        print(e)
        return -2

    su.query(f'grant "RESOURCE", "PUBLIC", "DBA", "VTI" to {uname}')
    return 0


# 删除用户包括他的默认表空间
def delete_user(uname):
    su = Dameng(username="SYSDBA", password="SYSDBA001")

    try:
        su.query(f"drop user {uname} cascade")
        su.query(f"drop tablespace {uname}")
        return 0
    except Exception as e:
        print(e)
        return -1


# 读HDFS存储的csv文件
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
        print(e)
        return -1

    df = (
        conn.read.format("csv")
        .option("header", "true")
        .load(f"hdfs://{server}:{port}/{directory}/物流公司.csv")
    )
    rows = df.collect()
    values = [[row[i] for i in range(len(row))] for row in rows]
    for r in values:
        try:
            dm.query(
                f"insert into 物流公司 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}')"
            )
        except Exception as e:
            print(e)
            count += 1

    df = (
        conn.read.format("csv")
        .option("header", "true")
        .load(f"hdfs://{server}:{port}/{directory}/客户信息.csv")
    )
    rows = df.collect()
    values = [[row[i] for i in range(len(row))] for row in rows]
    for r in values:
        try:
            dm.query(
                f"insert into 客户信息 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}')"
            )
        except Exception as e:
            print(e)
            count += 1

    df = (
        conn.read.format("csv")
        .option("header", "true")
        .load(f"hdfs://{server}:{port}/{directory}/物流信息.csv")
    )
    rows = df.collect()
    values = [[row[i] for i in range(len(row))] for row in rows]
    for r in values:
        try:
            dm.query(
                f"insert into 物流信息 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}')"
            )
        except Exception as e:
            print(e)
            count += 1

    df = (
        conn.read.format("csv")
        .option("header", "true")
        .load(f"hdfs://{server}:{port}/{directory}/集装箱动态.csv")
    )
    rows = df.collect()
    values = [[row[i] for i in range(len(row))] for row in rows]
    for r in values:
        try:
            dm.query(
                f"insert into 集装箱动态 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}')"
            )
        except Exception as e:
            print(e)
            count += 1

    df = (
        conn.read.format("csv")
        .option("header", "true")
        .load(f"hdfs://{server}:{port}/{directory}/装货表.csv")
    )
    rows = df.collect()
    values = [[row[i] for i in range(len(row))] for row in rows]
    for r in values:
        try:
            dm.query(
                f"insert into 装货表 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}', '{r[7]}', '{r[8]}', '{r[9]}', '{r[10]}', '{r[11]}')"
            )
        except Exception as e:
            print(e)
            count += 1

    df = (
        conn.read.format("csv")
        .option("header", "true")
        .load(f"hdfs://{server}:{port}/{directory}/卸货表.csv")
    )
    rows = df.collect()
    values = [[row[i] for i in range(len(row))] for row in rows]
    for r in values:
        try:
            dm.query(
                f"insert into 卸货表 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}', '{r[7]}', '{r[8]}', '{r[9]}', '{r[10]}', '{r[11]}')"
            )
        except Exception as e:
            print(e)
            count += 1

    conn.stop()
    return count


# 读取hdfs存储的tsv文件
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
        print(e)
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
        try:
            dm.query(
                f"insert into 物流公司 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}')"
            )
        except Exception as e:
            print(e)
            count += 1

    df = (
        conn.read.format("csv")
        .option("header", "true")
        .option("delimiter", "\t")
        .load(f"hdfs://{server}:{port}/{directory}/客户信息.txt")
    )
    rows = df.collect()
    values = [[row[i] for i in range(len(row))] for row in rows]
    for r in values:
        try:
            dm.query(
                f"insert into 客户信息 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}')"
            )
        except Exception as e:
            print(e)
            count += 1

    df = (
        conn.read.format("csv")
        .option("header", "true")
        .option("delimiter", "\t")
        .load(f"hdfs://{server}:{port}/{directory}/物流信息.txt")
    )
    rows = df.collect()
    values = [[row[i] for i in range(len(row))] for row in rows]
    for r in values:
        try:
            dm.query(
                f"insert into 物流信息 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}')"
            )
        except Exception as e:
            print(e)
            count += 1

    df = (
        conn.read.format("csv")
        .option("header", "true")
        .option("delimiter", "\t")
        .load(f"hdfs://{server}:{port}/{directory}/集装箱动态.txt")
    )
    rows = df.collect()
    values = [[row[i] for i in range(len(row))] for row in rows]
    for r in values:
        try:
            dm.query(
                f"insert into 集装箱动态 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}')"
            )
        except Exception as e:
            print(e)
            count += 1

    df = (
        conn.read.format("csv")
        .option("header", "true")
        .option("delimiter", "\t")
        .load(f"hdfs://{server}:{port}/{directory}/装货表.txt")
    )
    rows = df.collect()
    values = [[row[i] for i in range(len(row))] for row in rows]
    for r in values:
        try:
            dm.query(
                f"insert into 装货表 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}', '{r[7]}', '{r[8]}', '{r[9]}', '{r[10]}', '{r[11]}')"
            )
        except Exception as e:
            print(e)
            count += 1

    df = (
        conn.read.format("csv")
        .option("header", "true")
        .option("delimiter", "\t")
        .load(f"hdfs://{server}:{port}/{directory}/卸货表.txt")
    )
    rows = df.collect()
    values = [[row[i] for i in range(len(row))] for row in rows]
    for r in values:
        try:
            dm.query(
                f"insert into 卸货表 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}', '{r[7]}', '{r[8]}', '{r[9]}', '{r[10]}', '{r[11]}')"
            )
        except Exception as e:
            print(e)
            count += 1

    conn.stop()
    return count


# 读取minio存储的excel文件
def minio_read_excel(endpoint, access_key, secret_key, path):
    try:
        conn = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=False,
        )
    except Exception as e:
        print(e)
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
        print(e)
        return -1

    count = 0

    df = pd.read_excel("tmp", sheet_name="物流公司")
    for i, r in df.iterrows():
        try:
            dm.query(
                f"insert into 物流公司 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}')"
            )
        except Exception as e:
            print(e)
            count += 1

    df = pd.read_excel("tmp", sheet_name="客户信息")
    for i, r in df.iterrows():
        try:
            dm.query(
                f"insert into 客户信息 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}')"
            )
        except Exception as e:
            print(e)
            count += 1

    df = pd.read_excel("tmp", sheet_name="物流信息")
    for i, r in df.iterrows():
        try:
            dm.query(
                f"insert into 物流信息 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}')"
            )
        except Exception as e:
            print(e)
            count += 1

    df = pd.read_excel("tmp", sheet_name="集装箱动态")
    for i, r in df.iterrows():
        try:
            dm.query(
                f"insert into 集装箱动态 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}')"
            )
        except Exception as e:
            print(e)
            count += 1

    df = pd.read_excel("tmp", sheet_name="装货表")
    for i, r in df.iterrows():
        try:
            dm.query(
                f"insert into 装货表 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}', '{r[7]}', '{r[8]}', '{r[9]}', '{r[10]}', '{r[11]}')"
            )
        except Exception as e:
            print(e)
            count += 1

    df = pd.read_excel("tmp", sheet_name="卸货表")
    for i, r in df.iterrows():
        try:
            dm.query(
                f"insert into 卸货表 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}', '{r[7]}', '{r[8]}', '{r[9]}', '{r[10]}', '{r[11]}')"
            )
        except Exception as e:
            print(e)
            count += 1

    return count


# 读取存储在minio的csv文件
def minio_read_csv(endpoint, access_key, secret_key, directory):
    try:
        conn = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=False,
        )
    except Exception as e:
        print(e)
        return -1

    dm = Dameng("weiyin", "lamweiyin")

    tables = ("集装箱动态", "客户信息", "物流公司", "物流信息", "卸货表", "装货表")
    try:
        for table in tables:
            conn.fget_object(directory[0], f"{directory[1]}/{table}.csv", "tmp")
    except Exception as e:
        print(e)
        return -1

    count = 0

    conn.fget_object(directory[0], f"{directory[1]}/物流公司.csv", "tmp")
    df = pd.read_csv("tmp")
    for i, r in df.iterrows():
        try:
            dm.query(
                f"insert into 物流公司 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}')"
            )
        except Exception as e:
            print(e)
            count += 1

    conn.fget_object(directory[0], f"{directory[1]}/客户信息.csv", "tmp")
    df = pd.read_csv("tmp")
    for i, r in df.iterrows():
        try:
            dm.query(
                f"insert into 客户信息 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}')"
            )
        except Exception as e:
            print(e)
            count += 1

    conn.fget_object(directory[0], f"{directory[1]}/物流信息.csv", "tmp")
    df = pd.read_csv("tmp")
    for i, r in df.iterrows():
        try:
            dm.query(
                f"insert into 物流信息 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}')"
            )
        except Exception as e:
            print(e)
            count += 1

    conn.fget_object(directory[0], f"{directory[1]}/集装箱动态.csv", "tmp")
    df = pd.read_csv("tmp")
    for i, r in df.iterrows():
        try:
            dm.query(
                f"insert into 集装箱动态 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}')"
            )
        except Exception as e:
            print(e)
            count += 1

    conn.fget_object(directory[0], f"{directory[1]}/装货表.csv", "tmp")
    df = pd.read_csv("tmp")
    for i, r in df.iterrows():
        try:
            dm.query(
                f"insert into 装货表 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}', '{r[7]}', '{r[8]}', '{r[9]}', '{r[10]}', '{r[11]}')"
            )
        except Exception as e:
            print(e)
            count += 1

    conn.fget_object(directory[0], f"{directory[1]}/卸货表.csv", "tmp")
    df = pd.read_csv("tmp")
    for i, r in df.iterrows():
        try:
            dm.query(
                f"insert into 卸货表 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}', '{r[7]}', '{r[8]}', '{r[9]}', '{r[10]}', '{r[11]}')"
            )
        except Exception as e:
            print(e)
            count += 1

    return count


# 读取minio的tsv文件
def minio_read_txt(endpoint, access_key, secret_key, directory):
    try:
        conn = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=False,
        )
    except Exception as e:
        print(e)
        return -1
    dm = Dameng("weiyin", "lamweiyin")

    tables = ("集装箱动态", "客户信息", "物流公司", "物流信息", "卸货表", "装货表")
    try:
        for table in tables:
            conn.fget_object(directory[0], f"{directory[1]}/{table}.txt", "tmp")
    except Exception as e:
        print(e)
        return -1

    count = 0

    conn.fget_object(directory[0], f"{directory[1]}/物流公司.txt", "tmp")
    df = pd.read_csv("tmp", delimiter="\t")
    for i, r in df.iterrows():
        try:
            dm.query(
                f"insert into 物流公司 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}')"
            )
        except Exception as e:
            print(e)
            count += 1

    conn.fget_object(directory[0], f"{directory[1]}/客户信息.txt", "tmp")
    df = pd.read_csv("tmp", delimiter="\t")
    for i, r in df.iterrows():
        try:
            dm.query(
                f"insert into 客户信息 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}')"
            )
        except Exception as e:
            print(e)
            count += 1

    conn.fget_object(directory[0], f"{directory[1]}/物流信息.txt", "tmp")
    df = pd.read_csv("tmp", delimiter="\t")
    for i, r in df.iterrows():
        try:
            dm.query(
                f"insert into 物流信息 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}')"
            )
        except Exception as e:
            print(e)
            count += 1

    conn.fget_object(directory[0], f"{directory[1]}/集装箱动态.txt", "tmp")
    df = pd.read_csv("tmp", delimiter="\t")
    for i, r in df.iterrows():
        try:
            dm.query(
                f"insert into 集装箱动态 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}')"
            )
        except Exception as e:
            print(e)
            count += 1

    conn.fget_object(directory[0], f"{directory[1]}/装货表.txt", "tmp")
    df = pd.read_csv("tmp", delimiter="\t")
    for i, r in df.iterrows():
        try:
            dm.query(
                f"insert into 装货表 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}', '{r[7]}', '{r[8]}', '{r[9]}', '{r[10]}', '{r[11]}')"
            )
        except Exception as e:
            print(e)
            count += 1

    conn.fget_object(directory[0], f"{directory[1]}/卸货表.txt", "tmp")
    df = pd.read_csv("tmp", delimiter="\t")
    for i, r in df.iterrows():
        try:
            dm.query(
                f"insert into 卸货表 values ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}', '{r[5]}', '{r[6]}', '{r[7]}', '{r[8]}', '{r[9]}', '{r[10]}', '{r[11]}')"
            )
        except Exception as e:
            print(e)
            count += 1

    return count


# 从mysql迁移到达梦
def mysql_get_data(uname, passwd, host, database):
    try:
        conn = mysql.connector.connect(
            user=uname, password=passwd, host=host, database=database
        )
    except Exception as e:
        print(e)
        return -1

    dm = Dameng("weiyin", "lamweiyin")
    tables = ("集装箱动态", "客户信息", "物流公司", "物流信息", "卸货表", "装货表")

    cursor = conn.cursor()
    try:
        for table in tables:
            cursor.execute(f"select * from {table}")
            cursor.fetchall()
    except Exception as e:
        print(e)
        return -2

    count = 0

    cursor.execute("select * from 物流公司")
    for a, b, c, d, e in cursor.fetchall():
        try:
            dm.query(f"insert into 物流公司 values ('{a}', '{b}', '{c}', '{d}', '{e}')")
        except Exception as e:
            print(e)
            count += 1

    cursor.execute("select * from 客户信息")
    for a, b, c, d in cursor.fetchall():
        try:
            dm.query(f"insert into 客户信息 values ('{a}', '{b}', '{c}', '{d}')")
        except Exception as e:
            print(e)
            count += 1

    cursor.execute("select * from 物流信息")
    for a, b, c, d, e, f, g in cursor.fetchall():
        try:
            dm.query(
                f"insert into 物流信息 values ('{a}', '{b}', '{c}', '{d}', '{e}', '{f}', '{g}')"
            )
        except Exception as e:
            print(e)
            count += 1

    cursor.execute("select * from 集装箱动态")
    for a, b, c, d, e, f, g in cursor.fetchall():
        try:
            dm.query(
                f"insert into 集装箱动态 values ('{a}', '{b}', '{c}', '{d}', '{e}', '{f}', '{g}')"
            )
        except Exception as e:
            print(e)
            count += 1

    cursor.execute("select * from 卸货表")
    for a, b, c, d, e, f, g, h, i, j, k, l in cursor.fetchall():
        try:
            dm.query(
                f"insert into 卸货表 values ('{a}', '{b}', '{c}', '{d}', '{e}', '{f}', '{g}', '{h}', '{i}', '{j}', '{k}', '{l}')"
            )
        except Exception as e:
            print(e)
            count += 1

    cursor.execute("select * from 装货表")
    for a, b, c, d, e, f, g, h, i, j, k, l in cursor.fetchall():
        try:
            dm.query(
                f"insert into 装货表 values ('{a}', '{b}', '{c}', '{d}', '{e}', '{f}', '{g}', '{h}', '{i}', '{j}', '{k}', '{l}')"
            )
        except Exception as e:
            print(e)
            count += 1

    conn.close()
    return count


if __name__ == "__main__":
    # print(Dameng("weiyin", "lamweiyin").create_tables())
    # print(mysql_get_data("root", "Owkl.9130", "localhost", "test"))
    print(Dameng("weiyin", "lamweiyin").get_all())
