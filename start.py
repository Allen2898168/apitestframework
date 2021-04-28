# coding=UTF-8
import platform
import unittest
import os, sys, logging, yaml
from Common.Reporter import HTMLTestRunner
import Common.LoggingMap as login_map
import importlib
from Common.Mailer import EmailSender
from Common.Configure import Configure
from unittestreport import rerun
frameworkDir = os.path.dirname(__file__)
global_conf = Configure()
runningProject = global_conf.get_running_project()
casesDir = os.path.join(frameworkDir, "Projects", runningProject, "Cases")
logLevel = global_conf.get_loglevel()
reportPath = os.path.join(frameworkDir, "Report", "ErpReport.html")
# conf = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(frameworkDir, "Projects", runningProject, "Conf", "Conf.yml"), "r", encoding="utf-8") as f:
    project_conf = yaml.load(f, Loader=yaml.SafeLoader)
    modulesToRun = project_conf.get("MODULES_TO_RUN")

modules = []
for fileName in os.listdir(casesDir):
    if fileName.startswith("Test") and fileName.endswith(".py"):
        moduleName = fileName[:-3]
        modules.append(moduleName)

class Test:
    # 收集测试用例
    @classmethod
    def suite(cls):
        su = unittest.TestSuite()
        if modules:
            for i in modules:
                m = "Projects.%s.Cases.%s" % (runningProject, i)

                s = importlib.import_module(m)
                org_class = getattr(s, i)
                class_name = org_class.__name__
                if modulesToRun:
                    for j in modulesToRun.split(", "):
                        if j == class_name:
                            for c in dir(org_class):
                                if c.startswith("test_"):
                                    su.addTest(org_class(c))
                else:
                    for c in dir(org_class):
                        if c.startswith("test_"):
                            su.addTest(org_class(c))

        return su



if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(login_map.LoggingMap[logLevel])
    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', stream=sys.stderr)
    MyTests = Test()
    MyTests.suite()
    with open(reportPath, "wb") as f:
        runner = HTMLTestRunner(stream=f, title='开放服务中心接口测试报告', description='Project: %s' % runningProject,
                                online='http://10.10.103.170/ErpReport.html')
        runner.run(MyTests.suite())

    # if global_conf.get_auto_send_report():
    #     EmailSender.send_report(global_conf.get_mail_server_config(), reportPath)
    if global_conf.get_auto_send_report():
        system = platform.system()
        if system == "Windows":
            logger.warning("windows开发环境，不发邮件")
        elif system == "Linux":
            logger.warning("linux环境，发邮件")
            EmailSender.send_report(global_conf.get_mail_server_config(), reportPath)
