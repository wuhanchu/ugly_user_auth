# -*- coding:utf-8 -*-
from flask import request, send_file,make_response,render_template
from lib.models import *
from lib.JsonResult import JsonResult
from lib import param_tool,sql_tool
from webapi import baseRoute,app

# 用户列表
@baseRoute.route('/users', methods=['GET'])
def user_list():
    q = SysUser.query
    name = request.args.get("name")
    if name is not None:
        q = q.filter(SysUser.name.like("%" + name + "%"))
    q = q.order_by(SysUser.name.desc())
    offset = int(request.args.get('offset'))
    limit = int(request.args.get('limit'))
    res,total = sql_tool.model_page(q,limit,offset)
    return JsonResult.res_page(res,total)

# 详细用户信息
@baseRoute.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = SysUser.query.get(id)
    return JsonResult.queryResult(user)

@baseRoute.route('/users', methods=['POST'])
def add_user():
    args = request.get_json()
    name = args.get("name")
    username = args.get("username")
    telephone = args.get("telephone")
    #todo 将password转为md5编码
    password = args.get("password")
    user = SysUser(name=name, username=username, password=password, telephone=telephone)
    db.session.add(user)
    db.session.commit()
    return JsonResult.success("创建成功！", {"userid": user.id})

# PUT:全部字段 ；PATCH:部分字段
@baseRoute.route('/users/<id>', methods=['PUT','PATCH'])
def update_user(id):
    user = SysUser.query.get(id)
    if user is None :
        return JsonResult.error("对象不存在，id=%s"%id)
    args = request.get_json()
    #将参数加载进去
    param_tool.set_dict_parm(user,args)
    db.session.commit()
    return JsonResult.success("更新成功！",{"id": user.id})

@baseRoute.route('/users/<id>', methods=['DELETE'])
def del_users(id):
    "删除用户"
    user = SysUser.query.get(id)
    db.session.delete(user)
    # sql = """ delete from ts_meetasr_log where meetid='%s' """ % meetid
    # db.session.execute(sql)
    db.session.commit()
    return JsonResult.success("删除成功！", {"id": id})