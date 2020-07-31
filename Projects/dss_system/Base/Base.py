from Common.Case import Case
import jsonpath
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning


class Base(Case):
    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)
        self.client.packages.urllib3.disable_warnings(InsecureRequestWarning)

    def gets_db_cursor(self):
        """连接dss项目， db_g_user数据库"""
        connect = self.get_db_conn(schema="dss")
        cursor = connect.cursor()
        return connect, cursor

    def execute_sql(self, set_sql: str):
        """ 执行sql update INSERT """
        conn, cursor = self.gets_db_cursor()

        sql = set_sql
        result = cursor.execute(sql)
        conn.commit()
        return result

    def select_sql(self, set_sql):
        """ 查询数据 """
        conn, cursor = self.gets_db_cursor()
        sql = set_sql
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    def login(self):
        """获取token"""
        with self.setUp():
            data = self.data.get("loginDate")
            data["password"] = self.encrypt_md5(self.encrypt_md5(data.get("password")))

        with self.steps():
            resp = self.client.post(url=self.url.get("loginUrl"), json=data, headers=self.get_headers, verify=False)
            resp_data = json.loads(resp.text)
            resp_token = ''.join(jsonpath.jsonpath(resp_data, "$..token"))
        with self.verify():
            assert resp_token is not None, "错误 返回%s, token获取异常" % resp_token

        with self.cleanUp():
            # 存储token到公共变量池
            self.procedure().token["token"] = resp_token
