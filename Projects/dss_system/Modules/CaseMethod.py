from Projects.dss_system.Base.Base import Base


class CaseCode(Base):

    def __init__(self, *args, **kwargs):
        super(CaseCode, self).__init__(*args, **kwargs)
        self.headers = self.get_headers
        self.login()

    def token_headers(self):
        """ 保存token到信息头，后续调用该方法做 """

        self.headers["X-Auth-Token"] = self.procedure().token.get("token")
        return self.headers

    def customer_list(self, data: str):
        """ 查询客户列表 """
        url_customer_list = self.url.get("customer_list")
        r = self.client.get(url=url_customer_list, params=data, headers=self.token_headers(), verify=False)
        return r
