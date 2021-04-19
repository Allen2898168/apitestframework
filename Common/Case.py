from unittest import TestCase
from contextlib import contextmanager
from Common.Configure import Configure
from Common.Common import GlobaData, Common
import os
import yaml
import logging
import pymysql
import requests


class Case(TestCase):
    """ 测试用例基类 """
    client = requests

    @classmethod
    def project_conf(cls):
        """ 获取项目配置 """
        conf = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        with open(os.path.join(conf, "Projects", Configure.get_running_project(), "Conf", "Conf.yml"), "r",
                  encoding="utf-8") as f:
            return yaml.load(f, Loader=yaml.SafeLoader)

    def get_all_dbs_config(self):
        """ 获取所有数据库的连接配置信息 """
        return self.global_conf.get("DB")

    def get_db(self, name: str):
        """ 通过'name'获取某个数据库的连接信息 """
        for db in self.get_all_dbs_config():
            if db.get("name") == name:
                return db

    @classmethod
    def procedure(cls):
        return GlobaData

    @classmethod
    def encrypt_md5(cls, org_data: str):
        return Common.encrypt_md5(org_data)

    def __init__(self, *args, **kwargs):
        super(Case, self).__init__(*args, **kwargs)
        self.data = self.project_conf().get("data")
        self.url = self.project_conf().get("url")
        self.path = self.project_conf().get("path")
        self.get_headers = self.project_conf().get("headers")
        self.sql = self.project_conf().get("sql")
        self.logger = logging
        self.global_conf = Configure.get_global_config()

    def get_db_conn(self, schema: str):
        """ 获取数据库连接 """
        return pymysql.connect(host=self.get_db(name=schema).get("config").get("host"),
                               user=self.get_db(name=schema).get("config").get("user"),
                               port=self.get_db(name=schema).get("config").get("port"),
                               password=self.get_db(name=schema).get("config").get("password"),
                               database=self.get_db(name=schema).get("config").get("database"),
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)

    @contextmanager
    def setUp(self):
        """ 前置条件 """
        yield self.setUp

    @contextmanager
    def steps(self):
        """ 步骤 """
        yield self.steps

    @contextmanager
    def verify(self):
        """ 校验 """
        yield self.verify

    @contextmanager
    def cleanUp(self):
        """ 数据清理 """
        yield self.cleanUp

    @contextmanager
    def save(self):
        """ 数据保存 """
        yield self.save
