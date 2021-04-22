import re
import xlrd
import json
import random
import jsonpath
import datetime
from Common.Case import Case
from requests.packages.urllib3.exceptions import InsecureRequestWarning


class Base(Case):
    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)
        self.client.packages.urllib3.disable_warnings(InsecureRequestWarning)
        self.EXPR = '\$\{(.*?)\}'
        self.FUNC_EXPR = '__.*?\(.*?\)'
        self.saves = self.procedure().value
        self.resp = None

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
        result = cursor.fetchone()
        return result

    def get_time(self):
        """ 获取时间戳 唯一编号 """
        now_time = datetime.datetime.now().strftime("%Y%m%d%S")
        random_num = random.randint(0, 99)
        random_num = str(0) + str(random_num)
        unique_num = str(now_time) + str(random_num)
        return unique_num

    def get_data_time(self):
        """ 获取当前日期时间 """
        tomorrow = ((datetime.datetime.now() + datetime.timedelta()).strftime('%Y-%m-%d %H:%M:%S'))
        return tomorrow

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

    def save_date(self, source, key, jexpr: str):
        if jexpr.startswith("$"):
            value = jsonpath.jsonpath(source, jexpr)
            if not value:
                raise KeyError("该jsonpath未匹配到值,请确认接口响应和jsonpath正确性")
            value = value[0]
            self.saves[key] = value
            self.logger.warning("保存 {}=>{} 到全局变量池".format(key, value))
        else:
            self.saves[key] = jexpr
            self.logger.warning("保存 {}=>{} 到全局变量池".format(key, jexpr))

    def build_param(self, data):
        keys = re.findall(self.EXPR, data)
        for key in keys:
            value = self.saves.get(key)
            data = data.replace('${' + key + '}', str(value))

        funcs = re.findall(self.FUNC_EXPR, data)
        for func in funcs:
            fuc = func.split('__')[1]
            fuc_name = fuc.split("(")[0]
            fuc = fuc.replace(fuc_name, fuc_name.lower())
            value = eval(fuc)
            data = data.replace(func, str(value))
        return data

    def setup_sql(self, sql):
        if sql.startswith("select"):
            return self.select_sql(set_sql=sql)
        elif sql.startswith(("update", "insert", "delete")):
            return self.execute_sql(set_sql=sql)

    def teardown_sql(self, sql):
        if sql.startswith("select"):
            return self.select_sql(set_sql=sql)
        elif sql.startswith(("update", "insert", "delete")):
            return self.execute_sql(set_sql=sql)

    def client_server(self, server):
        # 判断请求环境类型
        if server == "test":
            server = self.url.get("test")
        elif server == 'pre':
            server = self.url.get("pre")
        elif server == 'pro':
            server = self.url.get("pro")
        else:
            server = self.logger.warning("未知环境")
        return server

    def token_header(self, header, resp):
        if header == 'DssHeader':
            self.get_headers.get("headers")['X-Auth-Token'] = jsonpath.jsonpath(resp, '$..token')[0]
            self.get_headers.get("headers")['X-CURR-ENTERPRISE-ID'] = ''.join(
                map(str, jsonpath.jsonpath(resp, "$..enterpriseId")))
        elif header == 'ZhibanHeader':
            self.get_headers.get("headers")['X-Auth-Token'] = jsonpath.jsonpath(resp, '$..token')[0]
            self.get_headers.get("headers")['x-supplier-enterprise-id'] = str(
                jsonpath.jsonpath(resp, "$..enterpriseId")[0])
        else:
            header = self.logger.warning("未知headers")
        return header

    def client_request(self, server, path, headers, is_token, method, body):

        client_server = self.client_server(server)
        headers = self.project_conf().get(headers)
        app_key = self.project_conf().get("appkey").get(server)
        url = client_server + path + app_key
        body = json.loads(body)
        if method.upper() == 'GET':
            self.resp = self.client.get(url=url, params=body, headers=headers, verify=False)
        elif method.upper() == 'POST':
            self.resp = self.client.post(url=url, headers=headers, json=body, verify=False)
        else:
            self.logger.warning("其他请求方法待扩展")

        if is_token:
            self.token_header(headers, resp=self.resp)

        return self.resp

    def assert_verify(self, expect, resp):
        # 遍历预期结果:
        expect = expect.replace(' ', '').replace("\n", "")
        for ver in expect.split(";"):
            expr = ver.split("=")[0]
            # 判断Jsonpath还是正则断言
            if expr.startswith("$."):
                actual = jsonpath.jsonpath(resp.json(), expr)
                if not actual:
                    raise KeyError("该jsonpath未匹配到值,请确认接口响应和jsonpath正确性")
                actual = str(actual[0])
            else:
                actual = re.findall(expr, resp.text)[0]
            expect = ver.split("=")[1]
            assert actual == expect, "错误，实际%s " % resp

    def read_excel(self, excel_path):
        workbook = xlrd.open_workbook(excel_path)
        # 获取所有sheet
        sheet_list = workbook.sheet_names()
        sheets_data = []

        for sheet in sheet_list:
            sheet = workbook.sheet_by_name(sheet)
            first_row = sheet.row_values(0)
            rows_length = sheet.nrows
            all_rows = []
            rows_dict = []
            for i in range(rows_length):
                if i == 0:  # 跳过第一行
                    continue
                all_rows.append(sheet.row_values(i))
            for row in all_rows:
                lis = dict(zip(first_row, row))
                rows_dict.append(lis)

            sheet_data = {"sheet": sheet.name, "data": rows_dict}
            sheets_data.append(sheet_data)
        return sheets_data
