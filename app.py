from flask import Flask,request,make_response
from pymongo import MongoClient
from json import dumps
client = MongoClient()
db = client['test-database']

web = Flask(__name__)

import json
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

from flask_cors import CORS
@web.after_request
def af_request(resp):     
    resp = make_response(resp)  ##需要导入一些函数
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return resp

CORS(web, supports_credentials=True)

def page_query(page=1,limit=20,table='ai_code'):
    '''翻页查询数据的功能'''
    collection = db[table]
    return list(collection.find().skip((page-1)*limit).limit(limit))

def page_count(table):
    '''总页数'''
    collection = db[table]
    return collection.find().count()

@web.route('/ai_code')  ### 接受路由地址数据，还需要接受参数数据/表单数据
def ai_code():
    page = int(request.args.get('page','1'))
    limit = int(request.args.get('limit','20'))
    table = 'ai_code'
    data = page_query(page=page,limit=limit,table=table)
    response_data={"code": 0, "msg": "", "count": page_count(table), "data": data}
    return dumps(response_data,cls=JSONEncoder)

@web.route('/job51')
def job51():
    page = int(request.args.get('page','1'))
    limit = int(request.args.get('limit','20'))
    table = 'job51'
    data = page_query(page=page,limit=limit,table=table)
    response_data={"code": 0, "msg": "", "count": page_count(table), "data": data}
    return dumps(response_data,cls=JSONEncoder) 

@web.route('/doutula')
def doutula():
    page = int(request.args.get('page','1'))
    limit = int(request.args.get('limit','20'))
    table = 'doutu'
    data = page_query(page=page,limit=limit,table=table)
    response_data={"code": 0, "msg": "", "count": page_count(table), "data": data}
    return dumps(response_data,cls=JSONEncoder)
 
web.run('172.16.250.100',port=8800)
