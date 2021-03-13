from unittest import skip

from Projects.dss_system.Modules.CaseMethod import CaseCode
import jsonpath
import json
from datetime import datetime


class TestCustomer(CaseCode):
    """ 线下订单流程测试 """

    def __init__(self, *args, **kwargs):
        super(TestCustomer, self).__init__(*args, **kwargs)

    def test_01_create_order(self):
        """ 创建线下订单 """
        with self.setUp():
            data = self.data.get("offlineOrder")
            order_id = "test" + datetime.now().strftime('%Y%m%d%H%M%S')
            data['externalOrderCode'] = order_id

        with self.steps():
            # 请求
            resp = self.create_order(data)
            resp_json = json.loads(resp.text)
            resp_code = resp_json.get("resultCode")
            resp_msg = resp_json.get("resultMsg")

        with self.verify():
            # 断言
            assert resp_code == 1000 and resp_msg == '操作成功', "错误，实际%s %s" % (resp_code, resp_msg)

        with self.save():
            # 保存订单id
            self.procedure().value.update({"order_code": order_id})

    def test_02_production_order(self):
        """ 订单排产 """
        with self.setUp():
            data = self.data.get("productionOrder")
            data['productionData'][0]['externalOrderCode'] = self.procedure().value.get("order_code")

        with self.steps():
            resp = self.production_order(data=data)
            resp_json = json.loads(resp.text)
            resp_code = resp_json.get("resultCode")
            resp_msg = resp_json.get("resultMsg")
            order_status = self.select_sql(self.sql.get("find_order") % self.procedure().value.get("order_code")) \
                .get("order_status")
        with self.verify():
            assert resp_code == 1000 and resp_msg == '操作成功' and order_status == '待入库', \
                "错误，实际%s %s %s" % (resp_code, resp_msg, order_status)

    def test_03_entering_warehouse(self):
        """ 订单入库 """
        with self.setUp():
            data = self.data.get("enteringWarehouse")
            data['enteringWarehouseData'][0]['externalOrderCode'] = self.procedure().value.get("order_code")

        with self.steps():
            resp = self.entering_warehouse(data=data)
            resp_json = json.loads(resp.text)
            resp_code = resp_json.get("resultCode")
            resp_msg = resp_json.get("resultMsg")
            order_status = self.select_sql(self.sql.get("find_order") % self.procedure().value.get("order_code")) \
                .get("order_status")

        with self.verify():
            assert resp_code == 1000 and resp_msg == '操作成功' and order_status == '待发货', \
                "错误，实际%s %s %s" % (resp_code, resp_msg, order_status)

    def test_04_delivery_order(self):
        """ 订单发货 """
        with self.setUp():
            data = self.data.get("deliveryOrder")
            data['deliveryList'][0]['externalOrderCode'] = self.procedure().value.get("order_code")
            data['externalDeliveryCode'] = self.procedure().value.get("order_code")

        with self.steps():
            resp = self.delivery_order(data=data)
            resp_json = json.loads(resp.text)
            resp_code = resp_json.get("resultCode")
            resp_msg = resp_json.get("resultMsg")
            order_status = self.select_sql(self.sql.get("find_order") % self.procedure().value.get("order_code")) \
                .get("order_status")

        with self.verify():
            assert resp_code == 1000 and resp_msg == '操作成功' and order_status == '待签收', \
                "错误，实际%s %s %s" % (resp_code, resp_msg, order_status)

    def test_05_receipt_order(self):
        """ 订单签收 """
        with self.setUp():
            data = self.data.get("receiptOrder")
            data['receiptList'][0]['externalOrderCode'] = self.procedure().value.get("order_code")
            data['externalDeliveryCode'] = self.procedure().value.get("order_code")

        with self.steps():
            resp = self.receipt_order(data=data)
            resp_json = json.loads(resp.text)
            resp_code = resp_json.get("resultCode")
            resp_msg = resp_json.get("resultMsg")
            order_status = self.select_sql(self.sql.get("find_order") % self.procedure().value.get("order_code")) \
                .get("order_status")

        with self.verify():
            assert resp_code == 1000 and resp_msg == '操作成功' and order_status == '已签收', \
                "错误，实际%s %s %s" % (resp_code, resp_msg, order_status)