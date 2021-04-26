from Projects.dss_system.Base.Base import Base


class CaseCode(Base):

    def __init__(self, *args, **kwargs):
        super(CaseCode, self).__init__(*args, **kwargs)
        a = "113"

    def create_order(self, data: str):
        """ 创建线下订单 """
        url = self.url.get("test") + self.path.get("offlineOrder")
        headers = self.get_headers
        r = self.client.post(url=url, json=data, headers=headers, verify=False)
        return r

    def production_order(self, data: str):
        """ 排产 """
        url = self.url.get("test") + self.path.get("production") + "?" + self.appkey.get("test")
        r = self.client.post(url=url, json=data, verify=False)
        return r

    def entering_warehouse(self, data: str):
        """ 入库 """
        url = self.url.get("test") + self.path.get("enteringWarehouse") + "?" + self.appkey.get("test")
        r = self.client.post(url=url, json=data, verify=False)
        return r

    def delivery_order(self, data: str):
        """ 发货 """
        url = self.url.get("test") + self.path.get("deliveryOrder") + "?" + self.appkey.get("test")
        r = self.client.post(url=url, json=data, verify=False)
        return r

    def receipt_order(self, data: str):
        """ 签收 """
        url = self.url.get("test") + self.path.get("receiptOrder") + "?" + self.appkey.get("test")
        r = self.client.post(url=url, json=data, verify=False)
        return r

    def add_or_modify_customer(self, data: str):
        """ 新增或修改客户档案 """
        url = self.url.get("test") + self.path.get("add_or_modify_customer") + "?" + self.appkey.get("test")
        r = self.client.post(url=url, json=data, verify=False)
        return r

    def cancel_order(self, data: str):
        """ 取消订单 """
        url = self.url.get("test") + self.path.get("cancel_order") + "?" + self.appkey.get("test")
        r = self.client.post(url=url, json=data, verify=False)
        return r

    def end_order(self, data: str):
        """ 完结订单 """
        url = self.url.get("test") + self.path.get("end_order") + "?" + self.appkey.get("test")
        r = self.client.post(url=url, json=data, verify=False)
        return r

    def after_sale(self, data: str):
        """ 售后处理 """
        url = self.url.get("test") + self.path.get("after_sale") + "?" + self.appkey.get("test")
        r = self.client.post(url=url, json=data, verify=False)
        return r

    def statement_bill(self, data: str):
        """ 对账单 """
        url = self.url.get("test") + self.path.get("statement_bill") + "?" + self.appkey.get("test")
        r = self.client.post(url=url, json=data, verify=False)
        return r

    def account_quota(self, data: str):
        """ ERP信用额度通知 """
        url = self.url.get("test") + self.path.get("account_quota") + "?" + self.appkey.get("test")
        r = self.client.post(url=url, json=data, verify=False)
        return r

    def customer_address(self, data: str):
        """ ERP客户地址 """
        url = self.url.get("test") + self.path.get("customer_address") + "?" + self.appkey.get("test")
        r = self.client.post(url=url, json=data, verify=False)
        return r

    def buyer_login(self, data: str):
        """ 采购端登陆 """
        headers = self.get_headers.get("zhibanHeader")
        url = self.url.get("test") + self.path.get("buyer_login") + "?" + self.appkey.get("test")
        r = self.client.post(url=url, json=data, headers=headers, verify=False)
        return r
