import pymysql
import yaml
import os


def get_config(name: str):
    with open(os.path.join("Conf", "Conf.yml"), "r", encoding="utf-8") as f:
        global_conf = yaml.load(f, Loader=yaml.SafeLoader)
    for db in global_conf.get("DB"):
        if db.get("name", None) == name:
            host = db["config"]["host"]
            port = db["config"]["port"]
            user = db["config"]["user"]
            password = db["config"]["password"]
            database = db["config"]["database"]
            if db["type"] == "mysql":
                con = pymysql.connect(user=user, password=password, host=host, port=port, database=database)
                cur = con.cursor(cursor=pymysql.cursors.DictCursor)
                return con, cur


class MySQL:
    def __init__(self, name: str):
        self.con, self.cur = get_config(name=name)

    def execute(self, sql: str):
        self.cur.execute(sql)
        self.con.commit()

    def fetch(self, number_rows=1):
        return self.cur.fetchmany(size=number_rows)

    def fetch_all(self):
        return self.cur.fetchall()


class Mongo:
    def __init__(self, name: str):
        self.client = get_config(name)

    def get_database(self, database_name: str):
        return self.client[database_name]
