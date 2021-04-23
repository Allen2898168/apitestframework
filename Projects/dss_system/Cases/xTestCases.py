import unittest
import os
import json
from ddt import ddt, data, unpack
from Projects.dss_system.Base.Base import Base

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
excel_data = os.path.join(path, "Conf", "case.xls")

excel_data = Base().read_excel(excel_path=excel_data)


@ddt
class TestCases(Base):
    """ 数据驱动测试用例集 """

    def __init__(self, *args, **kwargs):
        super(TestCases, self).__init__(*args, **kwargs)

    for sheet_data in excel_data:
        sheet = sheet_data.get("sheet")
        cases = sheet_data.get("data")

        exec(F"""
@data(*{cases})
@unpack
def test_{sheet}(self,case_id,title,server,path,is_skip,headers,is_token,method,request_data,expect_result,actual_result
                 ,public_value,setup_sql,teardown_sql):

    with self.setUp():
        path = self.build_param(path)
        body = self.build_param(request_data)
        expect_result = self.build_param(expect_result)
        setup_sql = self.setup_sql(setup_sql)
        teardown_sql = self.teardown_sql(teardown_sql)

    with self.steps():
        if is_skip == "skip":
            self.logger.warning("跳过用例编号：%s,标题：%s" %(case_id,title))
        elif is_skip is not "skip":
            self.logger.warning("执行用例编号：%s,标题：%s" %(case_id,title))
            resp = self.client_request(server,path,headers,is_token,method,body)
            resp_json = json.loads(resp.text)
            # self.logger.warning("响应结果：%s" %(resp_json))
        else:
            self.logger.warning("未知is_skip")

    with self.verify():
        self.assert_verify(expect_result,resp)

    with self.save():
        if public_value:
            for save in public_value.split(";"):
                key = save.split("=")[0]
                jsp = save.split("=")[1]
                self.save_date(resp, key, jsp)
        """
             )


if __name__ == '__main__':
    unittest.main()
