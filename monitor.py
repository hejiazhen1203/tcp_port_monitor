#!/usr/bin/env python
# -*- coding: utf-8
import datetime, time
import socket
import threading
import models
import sender
import config

import logging
import logging.handlers
LOG_FILENAME = config.logfile
mylogger = logging.getLogger("monitor")
formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
file_handler = logging.handlers.RotatingFileHandler(LOG_FILENAME,maxBytes=5242880,backupCount=5)
file_handler.setFormatter(formatter)
mylogger.addHandler(file_handler)
mylogger.setLevel(logging.DEBUG)
# mylogger.debug('this is debug info')
# mylogger.info('this is information')
# mylogger.warn('this is warning message')
# mylogger.error('this is error message')
# mylogger.fatal('this is fatal message, it is same as logger.critical')
# mylogger.critical('this is critical message')

def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def check_tcp(ip,port):
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(3)
    try:
        sk.connect((ip, int(port)))
        return 0
    except:
        return 1
    finally:
        sk.close()

#新添加监控项
def add_addr(name, httpaddr, coment):
    try:
        addr = models.Monitor(name=name,httpaddr=httpaddr,coment=coment)
        session = models.Session()
        session.add(addr)
        session.commit()
        return 0
    except Exception as e:
        mylogger.fatal(e)
        return 1
    finally:
        if session:
            session.close()
# add_addr(u"虚拟机ssh服务", "192.168.10.129:22", u"检查22端口是否存活")
# add_addr(u"虚拟机test服务", "192.168.10.129:23", u"检查23端口是否存活")
#执行监控项
def check_addr():
    try:
        session = models.Session()
        addrs = session.query(models.Monitor).all()
        for addr in addrs:
            ip  = addr.httpaddr.split(":")[0]
            port = addr.httpaddr.split(":")[1]
            rev = check_tcp(ip, port)
            if rev == 0:
                addr.success += 1
                addr.faild = 0
                info = u'服务{0}({1})运行正常'.format(addr.name, addr.httpaddr)
                mylogger.info(info)
                # print(info)
            else:
                addr.success = 0
                addr.faild += 1
                info = u'服务{0}({1})运行异常'.format(addr.name, addr.httpaddr)
                mylogger.error(info)
                # print(addr.name + u'异常')
            addr.last_commit = now()
        mylogger.debug('==============================================================')
        session.commit()
    except Exception as e:
        mylogger.fatal(e)
    finally:
        if session:
            session.close()
# check_addr()

#告警函数
def Alert():
    try:
        session = models.Session()
        addrs = session.query(models.Monitor).all()
        for addr in addrs:
            if addr.faild >= config.alert_th and addr.alerts < config.alert_times:
                addr.alerts += 1
                info = u'服务{0}({1})发生告警'.format(addr.name, addr.httpaddr)
                mylogger.info(info)
                # print(addr.name + u'开始报警')
                if config.send_email:
                    info = u'服务{0}({1})运行异常'.format(addr.name, addr.httpaddr)
                    mylogger.info(u'使用邮件发送告警发生内容')
                    sender.email(u'[告警发生]', info)
                elif config.send_weixin:
                    info = u'服务{0}({1})运行异常'.format(addr.name, addr.httpaddr)
                    # info = u'使用微信发送告警内容'
                    mylogger.info(u'使用微信发送告警发生内容')
                    sender.weixin(u'[告警发生]', info)
            elif addr.faild == 0 and addr.alerts != 0:
                addr.alerts = 0
                info = u'服务{0}({1})告警恢复'.format(addr.name, addr.httpaddr)
                mylogger.info(info)
                if config.send_email:
                    info = u'服务{0}({1})运行正常'.format(addr.name, addr.httpaddr)
                    mylogger.info(u'使用邮件发送告警恢复内容')
                    sender.email(u'[告警恢复]', info)
                elif config.send_weixin:
                    info = u'服务{0}({1})运行正常'.format(addr.name, addr.httpaddr)
                    mylogger.info(u'使用邮件发送告警恢复内容')
                    sender.weixin(u'[告警恢复]', info)
        mylogger.debug('==============================================================')
        session.commit()
    except Exception as e:
        mylogger.fatal(e)
    finally:
        if session:
            session.close()
# Alert()
def run_Check():
    while True:
        check_addr()
        time.sleep(config.intervel)

def run_Alert():
    while True:
        Alert()
        time.sleep(config.intervel)
if __name__ == '__main__':
    check_thread = threading.Thread(target=run_Check, args=())
    alert_thread = threading.Thread(target=run_Alert, args=())
    task = [check_thread, alert_thread]
    for tk in task:
        tk.setDaemon(True)
        tk.start()
    for tkt in task:
        tkt.join()
