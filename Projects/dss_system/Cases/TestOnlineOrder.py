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
            self.logger.warning("请求参数：%s" % data)

        with self.steps():
            resp = self.buyer_login(data=data)
            resp_json = json.loads(resp.text)
            self.logger.warning("响应参数：%s" % resp_json)

            resp_code = resp_json.get("resultCode")
            resp_msg = resp_json.get("resultMsg")

        with self.verify():
            assert resp_code == 1000 and resp_msg == '操作成功', "错误，实际%s %s" % (resp_code, resp_msg)

        with self.save():
            token = self.token_header(header="ZhibanHeader", resp=resp_json)
            self.procedure().value.update({"zhibanHeader": token})

    def test_02_cart_order(self):
        """ 测试下单商品，加入购物车 """

        with self.setUp():
            data = self.data.get("buyer_cart_order")
            self.logger.warning("请求参数：%s" % data)

        with self.steps():
            resp = self.buyer_cart_order(data=data)
            resp_json = json.loads(resp.text)
            self.logger.warning("响应参数：%s" % resp_json)
            resp_code = resp_json.get("resultCode")
            resp_msg = resp_json.get("resultMsg")
            resp_data = resp_json.get("resultData")

        with self.verify():
            assert resp_code == 1000 and resp_msg == '操作成功', "错误，实际%s %s" % (resp_code, resp_msg)

        with self.save():
            self.procedure().value.update({"cart_id": resp_data})
            self.logger.warning("cart_id变量：%s" % resp_data)

    def test_03_create_order(self):
        """ 测试处理购物车订单，生成订单 """

        with self.setUp():
            data = self.data.get("buyer_create_order")
            data["cartIds"] = self.procedure().value.get("cart_id")
            self.logger.warning("请求参数：%s" % data)

        with self.steps():
            resp = self.buyer_create_order(data=data)
            resp_json = json.loads(resp.text)
            self.logger.warning("响应参数：%s" % resp_json)
            resp_code = resp_json.get("resultCode")
            resp_msg = resp_json.get("resultMsg")
            resp_data = resp_json.get("resultData").get("orderIds")

        with self.verify():
            assert resp_code == 1000 and resp_msg == '操作成功', "错误，实际%s %s" % (resp_code, resp_msg)

        with self.save():
            self.procedure().value.update({"orderIds": resp_data})
            self.logger.warning("orderIds全局变量：%s" % resp_data)

    def test_04_order_pay(self):
        """ 测试订单支付 """

        with self.setUp():
            data = self.data.get("buyer_order_pay")
            data["orderIdList"] = self.procedure().value.get("orderIds")
            data["payPassword"] = self.encrypt_md5(self.encrypt_md5(data["payPassword"]))
            self.logger.warning("请求参数：%s" % data)

        with self.steps():
            resp = self.buyer_order_pay(data=data)
            resp_json = json.loads(resp.text)
            self.logger.warning("响应参数：%s" % resp_json)
            resp_code = resp_json.get("resultCode")
            resp_msg = resp_json.get("resultMsg")

        with self.verify():
            assert resp_code == 1000 and resp_msg == '操作成功', "错误，实际%s %s" % (resp_code, resp_msg)

    def test_05_notify_order_generated(self):
        """ 测试云印订单接单通知 """

        with self.setUp():
            data = self.data.get("notify_order_generated")
            order_product_code = self.select_sql(
                set_sql=self.sql.get("find_order_id") % self.procedure().value.get("orderIds")[0]).get("order_code")
            data["orderProductList"][0]["orderProductCode"] = order_product_code
            self.logger.warning("请求参数：%s" % data)

        with self.steps():
            resp = self.notify_order_generated(data=data)
            resp_json = json.loads(resp.text)
            self.logger.warning("响应参数：%s" % resp_json)
            resp_code = resp_json.get("resultCode")
            resp_msg = resp_json.get("resultMsg")

        with self.verify():
            assert resp_code == 1000 and resp_msg == '操作成功', "错误，实际%s %s" % (resp_code, resp_msg)

        with self.save():
            self.procedure().value.update({"order_id": order_product_code})
            self.logger.warning("order_product_code全局变量：%s" % order_product_code)

    def test_06_production(self):
        """ 测试云印订单排产通知  """

        with self.setUp():
            data = self.data.get("productionOrder")
            data['productionData'][0]['externalOrderCode'] = self.procedure().value.get("order_id")
            self.logger.warning("请求参数：%s" % data)

        with self.steps():
            resp = self.production_order(data=data)
            resp_json = json.loads(resp.text)
            self.logger.warning("响应参数：%s" % resp_json)
            resp_code = resp_json.get("resultCode")
            resp_msg = resp_json.get("resultMsg")

        with self.verify():
            assert resp_code == 1000 and resp_msg == '操作成功', "错误，实际%s %s" % (resp_code, resp_msg)

    def test_07_entering_warehouse(self):
        """ 测试云印订单入库通知 """
        with self.setUp():
            data = self.data.get("enteringWarehouse")
            data['enteringWarehouseData'][0]['externalOrderCode'] = self.procedure().value.get("order_code")

        with self.steps():
            resp = self.entering_warehouse(data=data)
            resp_json = json.loads(resp.text)
            self.logger.warning("响应参数：%s" % resp_json)
            resp_code = resp_json.get("resultCode")
            resp_msg = resp_json.get("resultMsg")

        with self.verify():
            assert resp_code == 1000 and resp_msg == '操作成功', "错误，实际%s %s" % (resp_code, resp_msg)

    # def test_08_delivery_order(self):
    #     """ 测试云印订单发货通知 """