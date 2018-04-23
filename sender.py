#!/usr/bin/env python
# -*- coding: utf-8
import smtplib
from email.mime.text import MIMEText
import json
import config
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os, httplib, urllib
def email(sub,info):
    subject = sub
    msg = MIMEText('<html><h3>' + info + '</h3></html>', 'html', 'utf-8')
    msg['subject'] = subject
    msg['from'] = u'公有云<gyy@cloudwalk.cn>'
    msg['to'] = ';'.join(config.mailto_list)
    try:
        smtp = smtplib.SMTP()
        smtp.connect(config.smtpserver)
        smtp.login(config.mail_username, config.mail_password)
        smtp.sendmail(config.mail_sender, config.mailto_list, msg.as_string())
        smtp.quit()
    except Exception, e:
        print(e)
def weixin(sub,info):
    pass
    api_host = "qyapi.weixin.qq.com"
    token_url = "/cgi-bin/gettoken"
    sendmsg_url = "/cgi-bin/message/send"

    def https_get(host, url):
        try:
            http = httplib.HTTPSConnection(host, timeout=5)
            http.request('GET', url)
            response = http.getresponse()
            return response.read()
        except Exception as e:
            return "Error"
            print(e)
        finally:
            if http:
                http.close()

    def https_post(host, url, data):
        try:
            # data = urllib.urlencode(data)
            http = httplib.HTTPSConnection(host, timeout=5)
            http.request('POST', url, data)
            response = http.getresponse()
            return response.read()
        except Exception as e:
            return "Error"
            print(e)
        finally:
            if http:
                http.close()

    def gettoken(corpid, corpsecret):
        gettoken_url = token_url + '?corpid=%s&corpsecret=%s' % (corpid, corpsecret)
        try:
            recv = https_get(api_host, gettoken_url)
            resp = json.loads(recv)
            if resp.get('errcode', 1) == 0:
                return resp['access_token']
            else:
                return None
        except Exception as e:
            print e
            return None

    def senddata(access_token, agentid, subject, content):
        params = {
            "touser": "@all",  # 消息接收者，多个接收者用‘|’分隔，最多支持1000个,@all表示应用内全部成员
            "toparty": "8",  # 部门id,多个接收者用‘|’分隔，最多支持100个,当touser为@all时忽略本参数
            "totag": "1",  # 标签id,多个接收者用‘|’分隔，最多支持100个,当touser为@all时忽略本参数
            "msgtype": "text",  # 消息类型
            "agentid": agentid,  # 应用id
            "safe": 0,  # 消息是否加密
            "text": {
                "content": subject + '\n' + content
            },  # 内容
        }
        params = json.dumps(params)
        send_url = sendmsg_url + '?access_token=%s' % (access_token)
        try:
            recv = https_post(api_host, send_url, params)
            resp = json.loads(recv)
            # print(json.dumps(resp, indent=2, ensure_ascii=False))
        except Exception as e:
            print(e)

    accesstoken = gettoken(config.corpid, config.corpsecret)
    senddata(accesstoken, config.agentid, sub, info)