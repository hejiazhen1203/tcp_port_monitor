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
mail_sender = 'youremail'
mail_username = 'youremail'
mail_password = 'yourpass'
smtpserver = 'smtp.exmail.qq.com'

#微信设置
send_weixin = True
corpid = '请填写自己的企业号ID'  # CorpID是企业号的标识
corpsecret = '请填写自己的应用secret'  # 应用secret
agentid = 请填写自己的应用id  # 应用id
