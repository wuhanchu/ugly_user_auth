# -*- coding:utf-8 -*-
import time
from flask import request
from lib.models import *
from lib.JsonResult import JsonResult
from lib import param_tool,sql_tool,com_tool
from webapi import baseRoute
from lib.oauth2 import require_oauth

# 角色列表
@baseRoute.route('/roles', methods=['GET'])
@require_oauth('profile')
def role_list():
    q = SysRole.query
    name = request.args.get("name")
    if name is not None:
        q = q.filter(SysRole.name.like("%" + name + "%"))
    q = q.order_by(SysRole.name.desc())
    offset = int(request.args.get('offset'))
    limit = int(request.args.get('limit'))
    sort = request.args.get('sort')
    if sort == None:
        sort = "-id"
    res,total = sql_tool.model_page(q,limit,offset,sort)
    return JsonResult.res_page(res,total)

# 详细角色信息
@baseRoute.route('/roles/<id>', methods=['GET'])
@require_oauth('profile')
def get_role(id):
    obj = SysRole.query.get(id)
    return JsonResult.queryResult(obj)

@baseRoute.route('/roles', methods=['POST'])
@require_oauth('profile')
def add_role():
    obj = SysRole()
    args = request.get_json()
    # 将参数加载进去
    param_tool.set_dict_parm(obj, args)
    obj.opr_at = int(time.time())
    db.session.add(obj)
    db.session.commit()
    return JsonResult.success("创建成功！", {"id": obj.id})

# PUT:全部字段 ；PATCH:部分字段
@baseRoute.route('/roles/<id>', methods=['PUT','PATCH'])
@require_oauth('profile')
def update_role(id):
    obj = SysRole.query.get(id)
    if obj is None :
        return JsonResult.error("对象不存在，id=%s"%id)
    args = request.get_json()
    if "password" in args:
        args.pop("password")
    #将参数加载进去
    param_tool.set_dict_parm(obj,args)
    db.session.commit()
    return JsonResult.success("更新成功！",{"id": obj.id})

@baseRoute.route('/roles/<id>', methods=['DELETE'])
@require_oauth('profile')
def del_role(id):
    "删除角色"
    obj = SysRole.query.get(id)
    db.session.delete(obj)
    # sql = """ delete from ts_meetasr_log where meetid='%s' """ % meetid
    # db.session.execute(sql)
    db.session.commit()
    return JsonResult.success("删除成功！", {"id": id})


@baseRoute.route('/user_roles/<user_id>', methods=['GET'])
@require_oauth('profile')
def user_roles_list(user_id):
    list  = SysRole.query.join(SysUserRole,SysUserRole.role_id == SysRole.id) .filter(SysUserRole.user_id == user_id).all()
    return JsonResult.queryResult(list)


@baseRoute.route('/user_roles/<user_id>', methods=['PUT'])
@require_oauth('profile')
def update_user_roles(user_id):
    args = request.get_json()
    role_ids = args.get("role_ids")
    user_roles = SysUserRole.query.filter(SysUserRole.user_id == user_id).all()
    for role_id in role_ids:
        # 判断数据库中是否已经存在该用户
        selected = [ur for ur in user_roles if  ur.role_id == role_id]
        if len(selected) == 0:
            user_role = SysUserRole(user_id=user_id, role_id=role_id)
            db.session.add(user_role)
        else:  # 已存在的角色，从user_roles中删掉，剩下的是要删除的用户
            user_roles.remove(selected[0])
    # 删除已经不存在的数据
    [db.session.delete(user_role) for user_role in user_roles]
    db.session.commit()
    return JsonResult.success("更新用户角色成功！")