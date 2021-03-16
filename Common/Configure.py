import yaml
import os


class Configure:

    @classmethod
    def get_global_config(cls):
        conf = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        with open(os.path.join(conf, "Conf.yml"), "r", encoding="utf-8") as f:
            return yaml.load(f, Loader=yaml.SafeLoader)

    @classmethod
    def global_config(cls):
        return cls.get_global_config()

    @classmethod
    def get_running_project(cls):
        running_project = cls.global_config().get("PROJECT_TO_RUN")
        return running_project

    @classmethod
    def get_loglevel(cls):
        return cls.global_config().get("LOG_LEVEL")

    @classmethod
    def get_mail_server_config(cls):
        return cls.global_config().get("EMAIL_SERVER")

    @classmethod
    def get_auto_send_report(cls):
        return cls.global_config().get("AUTO_SEND_REPORT")
# print(Configure.get_global_config())
