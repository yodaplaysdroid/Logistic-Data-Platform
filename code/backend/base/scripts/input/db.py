import pyodbc


class Dameng:
    def __init__(self, username="weiyin", password="lamweiyin"):
        self.username = username
        self.password = password

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

    def create_tables(self):
        message = []

        try:
            self.exec(
                """create table 物流公司 (
                公司名称 varchar(100) not null unique,
                客户编号 varchar(50) not null,
                联系人 varchar(50),
                电话 varchar(20),
                省市区 varchar(100),
                primary key(客户编号))"""
            )
        except Exception as e:
            message.append(["物流公司创建失败：" + e])

        try:
            self.exec(
                """create table 客户信息 (
                客户名称 varchar(50) not null,
                客户编号 varchar(20) not null,
                手机号 varchar(20) not null unique,
                省市区 varchar(100),
                primary key(客户编号))"""
            )
        except Exception as e:
            message.append(["客户信息创建失败：" + e])

        try:
            self.exec(
                """create table 物流信息 (
                提单号 varchar(50) not null,
                货主名称 varchar(50) not null,
                货主代码 varchar(20) not null foreign key references 客户信息(客户编号),
                物流公司_货代 varchar(100) not null foreign key references 物流公司(公司名称),
                集装箱箱号 varchar(50) not null,
                货物名称 varchar(50) not null,
                货重_吨 int not null,
                primary key(提单号))"""
            )
        except Exception as e:
            message.append(["物流信息创建失败：" + e])

        try:
            self.exec(
                """create table 集装箱动态 (
                堆存港口 varchar(100) not null,
                集装箱箱号 varchar(50) not null,
                箱尺寸_TEU int,
                提单号 varchar(100) not null foreign key references 物流信息(提单号),
                堆场位置 varchar(100) not null,
                操作 varchar(50) not null,
                操作日期 varchar(50) not null,
                primary key(集装箱箱号, 提单号, 操作))"""
            )
        except Exception as e:
            message.append(["集装箱动态创建失败：" + e])

        try:
            self.exec(
                """create table 装货表 (
                船公司 varchar(100),
                船名称 varchar(100),
                作业开始时间 varchar(100),
                作业结束时间 varchar(100),
                始发时间 varchar(100),
                到达时间 varchar(100),
                作业港口 varchar(100),
                提单号 varchar(100) not null foreign key references 物流信息(提单号),
                集装箱箱号 varchar(100),
                箱尺寸_TEU varchar(100),
                启运地 varchar(100),
                目的地 varchar(100),
                primary key(提单号))"""
            )
        except Exception as e:
            message.append(["装货表创建失败：" + e])

        try:
            self.exec(
                """create table 卸货表 (
                船公司 varchar(100),
                船名称 varchar(100),
                作业开始时间 varchar(100),
                作业结束时间 varchar(100),
                始发时间 varchar(100),
                到达时间 varchar(100),
                作业港口 varchar(100),
                提单号 varchar(100) not null foreign key references 物流信息(提单号),
                集装箱箱号 varchar(100),
                箱尺寸_TEU varchar(100),
                启运地 varchar(100),
                目的地 varchar(100),
                primary key(提单号))"""
            )
        except Exception as e:
            message.append(["卸货表创建失败：" + e])

        return message

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

        cursor.execute("commit")
        conn.close()
        return 0

    def get_tables(self):
        return self.query(
            f"""select NAME
            from sysobjects
            where \"SUBTYPE$\"='UTAB'
            AND SCHID=(SELECT ID
            FROM sysobjects
            WHERE NAME='{self.username.upper()}'
            AND TYPE$='SCH')"""
        )

    def get_users(self):
        return self.query("select username from dba_users")

    def get_all(self):
        df = []
        tables = ("物流公司", "客户信息", "物流信息", "集装箱动态", "装货表", "卸货表")
        for table in tables:
            df.append(self.query(f"select * from {table}"))
        return df


def create_user(uname, passwd):
    su = Dameng(username="SYSDBA", password="SYSDBA001")

    if (
        su.exec(
            f"create tablespace {uname} datafile '{uname}.dbf' size 256 autoextend on maxsize 10240"
        )
        == -1
    ):
        return -1

    if (
        su.exec(
            f'create user {uname} identified by "{passwd}" default tablespace {uname} default index tablespace {uname}'
        )
        == -1
    ):
        su.exec(f"drop tablespace {uname}")
        return -2

    if su.exec(f'grant "RESOURCE", "PUBLIC", "DBA", "VTI" to {uname}') == 0:
        return 0
    else:
        return -3


def delete_user(uname):
    su = Dameng(username="SYSDBA", password="SYSDBA001")

    try:
        su.exec(f"drop user {uname} cascade")
        su.exec(f"drop tablespace {uname}")
        return 0
    except Exception as e:
        print(e)
        return -1


if __name__ == "__main__":
    print(Dameng().create_tables())
