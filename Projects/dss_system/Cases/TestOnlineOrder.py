from unittest import skip
import json
import jsonpath
from Projects.dss_system.Modules.CaseMethod import CaseCode


class TestOnlineOrder(CaseCode):
    """ 线上订单流程测试用例集 """

    def __init__(self, *args, **kwargs):
        super(TestOnlineOrder, self).__init__(*args, **kwargs)

    def test_01_buyer_login(self):
        """ 采购端三级厂登陆 """

        with self.setUp():
            data = self.data.get("buyer_login")
            data["password"] = self.encrypt_md5(self.encrypt_md5(data["password"]))  # 两次md5加密密码

        with self.steps():
            resp = self.buyer_login(data=data)
            resp_json = json.loads(resp.text)
            resp_code = resp_json.get("resultCode")
            resp_msg = resp_json.get("resultMsg")

        with self.verify():
            assert resp_code == 1000 and resp_msg == '操作成功', "错误，实际%s %s" % (resp_code, resp_msg)

        with self.save():
            self.token_header(header="ZhibanHeader", resp=resp_json)  # 存储请求头


