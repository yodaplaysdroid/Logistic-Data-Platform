import mysql.connector
from .db import Dameng


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
