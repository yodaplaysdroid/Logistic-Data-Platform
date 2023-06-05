from .db import Dameng
from pyspark.sql import SparkSession


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
