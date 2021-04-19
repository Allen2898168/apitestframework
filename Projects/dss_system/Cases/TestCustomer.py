from unittest import skip

from Projects.dss_system.Modules.CaseMethod import CaseCode
import json


class TestCustomer(CaseCode):
    """ ERP客户模块测试用例集 """

    def __init__(self, *args, **kwargs):
        super(TestCustomer, self).__init__(*args, **kwargs)

    def test_01_create_order(self):
        """
            ERP客户建档 ERP维护客户档案，同步客户档案到云印
        """
        with self.setUp():
            data = self.data.get("add_or_modify_customer")

        with self.steps():
            resp = self.add_or_modify_customer(data)
            resp_json = json.loads(resp.text)
            resp_code = resp_json.get("resultCode")
            resp_msg = resp_json.get("resultMsg")

        with self.verify():
            assert resp_code == 1000 and resp_msg == '操作成功', "错误，实际%s %s" % (resp_code, resp_msg)

        with self.cleanUp():
            self.execute_sql(self.sql.get("find_customer"))
