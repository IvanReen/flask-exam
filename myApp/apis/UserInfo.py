import os
import time

import werkzeug
from flask_restful import Resource, marshal_with, fields, reqparse
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from myApp.ext import db
from myApp.models import User
from myApp.settings import UPLOAD_DIR

parser = reqparse.RequestParser()
parser.add_argument('token', type=str, required=True, help='缺少token')
parser.add_argument('usericon', type=werkzeug.datastructures.FileStorage, location='files', help='请上传头像')
parser.add_argument('oldpassword', type=str, required=True, help='缺少旧密码')
parser.add_argument('newpassword', type=str, required=True, help='缺少新密码')

class IconFormat(fields.Raw):
    def format(self,value):
        return f'/static/img/{value}'

user_fields = {
    'icon': IconFormat(attribute='icon')
}

result_fields = {
    'status': fields.Integer,
    'msg': fields.String,
    'data': fields.String(default=''),
    'error': fields.String(default='')
}

class UserInfoChange(Resource):

    @marshal_with(result_fields)
    def post(self):
        parse = parser.parse_args()
        token = parse.get('token')
        oldpassword = parse.get('oldpassword')
        newpassword = parse.get('newpassword')

        users = User.query.filter(User.token == token)

        returndata = {}

        if users.count() > 0:
            user = users.first()
            # 获取图片数据
            imgfile = parse.get('usericon') or os.path.join(UPLOAD_DIR, 'head.png')
            # 图片名称
            filename = '%d-%s' % (user.id, time.time())
            # 图片保存
            filepath = os.path.join(UPLOAD_DIR, filename)
            # 保存文件
            imgfile.save(filepath)
            # 更新数据
            user.icon = filename
            if check_password_hash(user.password, oldpassword):  # 密码正确
                user.password = generate_password_hash(newpassword)

                db.session.add(user)
                db.session.commit()

                returndata['status'] = 200
                returndata['msg'] = '用户修改信息成功'

            else:  # 密码错误
                returndata['status'] = 401
                returndata['msg'] = '无法修改密码'
                returndata['error'] = '旧密码错误'
        else:
            returndata['status'] = 401
            returndata['msg'] = '无此用户信息'
            returndata['error'] = 'token错误'
        return returndata