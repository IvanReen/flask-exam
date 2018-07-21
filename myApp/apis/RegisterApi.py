import uuid

from flask import jsonify
from flask_restful import reqparse, fields, Resource, marshal_with

# 你给我的数据
from werkzeug.security import generate_password_hash

from myApp.ext import db, send_mail
from myApp.models import User

parser_post = reqparse.RequestParser()
parser_post.add_argument('name', type=str, required=True, help='请输入用户名')
parser_post.add_argument('password', type=str, required=True, help='请输入密码')
parser_post.add_argument('email', type=str, required=True, help='请输入邮箱')
parser_post.add_argument('icon', type=str, help='请上传头像')

parser_get = reqparse.RequestParser()
parser_get.add_argument('username', type=str, required=True, help='请输入用户名')

# 我给你的参数格式
user_fields = {
    'name': fields.String,
    'token': fields.String,
    'icon': fields.String,
    'permissions': fields.Integer
}
result_fields = {
    'status': fields.Integer,
    'msg': fields.String,
    'data': fields.Nested(user_fields, default=''),
    'error': fields.String(default='')
}

class Register(Resource):

    def get(self):

        returndata = {}
        parse = parser_get.parse_args()
        user_name = parse.get('username')
        users = User.query.all()
        for user in users:
            if user.name == user_name:
                returndata['status'] = 401
                returndata['msg'] = '用户不可使用'
                return returndata
            else:
                returndata['status'] = 200
                returndata['msg'] = '用户可使用'
                return 1




    @marshal_with(result_fields)
    def post(self):
        parse = parser_post.parse_args()
        user = User()
        user.name = parse.get('name')
        # user.password = parse.get('password')
        # 密码加密处理
        user.password = generate_password_hash(parse.get('password'))
        user.email = parse.get('email')
        user.icon = parse.get('icon')
        user.token = str(uuid.uuid4())

        returndata = {}
        users = User.query.filter(User.name == user.name).filter(User.email == user.email)
        if users.count() > 0:
            returndata['status'] = 406
            returndata['msg'] = '注册失败'
            returndata['error'] = '用户名和邮箱已存在，请直接登录！'
            return returndata
        else:
            users = User.query.filter(User.email == user.email)
            if users.count() > 0:
                returndata['status'] = 406
                returndata['msg'] = '注册失败'
                returndata['error'] = '邮箱已存在，请重新输入'
                return returndata
            users = User.query.filter(User.name == user.name)
            if users.count() > 0:
                returndata['status'] = 406
                returndata['msg'] = '注册失败'
                returndata['error'] = '用户名已存在，请重新输入！'
                return returndata

        db.session.add(user)
        db.session.commit()
        # send_mail(user)


        returndata['status'] = 200
        returndata['msg'] = '注册成功'
        returndata['data'] = user
        return returndata