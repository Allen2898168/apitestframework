from Projects.dss_system.Base.Base import Base


class CaseCode(Base):

    def __init__(self, *args, **kwargs):
        super(CaseCode, self).__init__(*args, **kwargs)

    def create_order(self, data: str):
        """ 创建线下订单 """
        url = self.url.get("test") + self.path.get("offlineOrder")
        headers = self.get_headers
        r = self.client.post(url=url, json=data, headers=headers, verify=False)
        return r

    def production_order(self, data: str):
        """ 排产 """
        url = self.url.get("test") + self.path.get("production")
        headers = self.get_headers
        r = self.client.post(url=url, json=data, headers=headers, verify=False)
        return r

    def entering_warehouse(self, data: str):
        """ 入库 """
        url = self.url.get("test") + self.path.get("enteringWarehouse")
        headers = self.get_headers
        r = self.client.post(url=url, json=data, headers=headers, verify=False)
        return r

    def delivery_order(self, data: str):
        """ 发货 """
        url = self.url.get("test") + self.path.get("deliveryOrder")
        headers = self.get_headers
        r = self.client.post(url=url, json=data, headers=headers, verify=False)
        return r

    def receipt_order(self, data: str):
        """ 签收 """
        url = self.url.get("test") + self.path.get("receiptOrder")
        headers = self.get_headers
        r = self.client.post(url=url, json=data, headers=headers, verify=False)
        return r
