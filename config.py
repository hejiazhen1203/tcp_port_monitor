#!/usr/bin/env python
# -*- coding: utf-8
import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'moni.db')
logfile = os.path.join(basedir, 'logs/monitor.log')
intervel = 60
alert_th = 3
alert_times = 3

#邮箱设置
send_email = False
mailto_list = ['512610309@qq.com']
mail_sender = 'gyy@cloudwalk.cn'
mail_username = 'gyy@cloudwalk.cn'
mail_password = 'Cloud@0305'
smtpserver = 'smtp.exmail.qq.com'

#微信设置
send_weixin = True
corpid = 'ww3e021b3079c7d9d2'  # CorpID是企业号的标识
corpsecret = 'tWShMrMrhODaHCsbFmU3_5NiIn5pZzeMwto2E6VCjrM'  # 应用secret
agentid = 1000004  # 应用id