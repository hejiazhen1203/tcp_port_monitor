#!/usr/bin/env python
# -*- coding: utf-8
from flask import Flask, render_template
import models
import time
def GetData():
    try:
        session = models.Session()
        datas = session.query(models.Monitor).all()
        resp_list = []
        for data in datas:
            resp = {}
            resp['id'] = data.id
            resp['name'] = data.name
            resp['httpaddr'] = data.httpaddr
            resp['success'] = data.success
            resp['faild'] = data.faild
            resp['alerts'] =data.alerts
            resp['last_commit'] = data.last_commit
            resp['refush'] = int(time.time() - time.mktime(time.strptime(data.last_commit, '%Y-%m-%d %H:%M:%S')))
            resp_list.append(resp)
        return resp_list
    except Exception as e:
        print(e)
        return []
    finally:
        if session:
            session.close()

# print  GetData()
# import sys
# sys.exit(0)
app=Flask(__name__)
@app.route('/')
def index():
    resp_data = GetData()
    return render_template('index.html', data=resp_data)

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8000,threaded=True,debug=True)