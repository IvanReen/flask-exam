from flask_restful import Resource, marshal_with, fields, reqparse
from werkzeug.security import check_password_hash, generate_password_hash

from myApp.ext import db
from myApp.models import User

parser = reqparse.RequestParser()
parser.add_argument('token', type=str, required=True, help='缺少token')
parser.add_argument('oldpassword', type=str, required=True, help='缺少旧密码')
parser.add_argument('newpassword', type=str, required=True, help='缺少新密码')

result_fields = {
    'status': fields.Integer,
    'msg': fields.String,
    'data': fields.String(default=''),
    'error': fields.String(default='')
}


class PasswordChange(Resource):

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

            if check_password_hash(user.password, oldpassword):  # 密码正确
                user.password = generate_password_hash(newpassword)

                db.session.add(user)
                db.session.commit()

                returndata['status'] = 200
                returndata['msg'] = '修改密码成功'

            else:  # 密码错误
                returndata['status'] = 401
                returndata['msg'] = '无法修改密码'
                returndata['error'] = '旧密码错误'
        else:
            returndata['status'] = 401
            returndata['msg'] = '无此用户信息'
            returndata['error'] = 'token错误'

        return returndata
