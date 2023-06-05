from minio import Minio
from .db import Dameng
import pandas as pd


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
