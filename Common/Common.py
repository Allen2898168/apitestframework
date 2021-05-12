import hashlib, base64


class Common:

    @classmethod
    def encrypt_md5(cls, org_data: str):
        m = hashlib.md5()
        m.update(org_data.encode())
        return m.hexdigest()

    @classmethod
    def encrypt_base64(cls, org_data: str):
        return base64.standard_b64encode(org_data.encode()).decode()


class GlobaData(object):
    """ 公共变量池 """
    value = {}
