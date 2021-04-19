# !/usr/bin/env python3
# coding=utf-8
import json, urllib3


# 发送钉钉消息
class DingTalkSender:
    @classmethod
    def nail_inform(self, conf, token):
        d = dict(conf)
        retries_run = d.get('用例总数')
        status = d.get("状态")
        result_online = d.get("在线测试报告地址")

        url = token  # 钉钉token
        con = {"msgtype": "text",
               "text": {
                   "content": "测试钉钉机器人测试报告。\n测试概述:\n运行总数:" + retries_run + "\n执行情况:" + status + "\n在线测试报告:" + result_online}
               }
        urllib3.disable_warnings()
        http = urllib3.PoolManager()
        jd = json.dumps(con)
        jd = bytes(jd, 'utf-8')
        http.request('POST', url, body=jd, headers={'Content-Type': 'application/json'})
