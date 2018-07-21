import uuid

from flask_restful import reqparse, fields, Resource, marshal_with
from werkzeug.security import check_password_hash

from myApp.ext import send_mail, db, cache
from myApp.models import User

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True, help='请输入用户名')
parser.add_argument('password', type=str, required=True, help='请输入密码')

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

class Login(Resource):
    @marshal_with(result_fields)
    def post(self):
        parse = parser.parse_args()
        username = parse.get('username')
        password = parse.get('password')
        returndata = {}
        users = User.query.filter(User.name == username)
        if users.count() > 0:
            user = users.first()
            if check_password_hash(user.password, password):
                if user.isactive == False:
                    returndata['status'] = 401
                    returndata['msg'] = '登录失败'
                    returndata['error'] = '用户未激活， 请激活后再登录， 查看邮箱。'
                    user.token = str(uuid.uuid4())
                    db.session.add(user)
                    db.session.commit()
                    send_mail(user)
                    cache.set(user.token, user.id, timeout=30)
                    return returndata
                if user.isdelete == True:
                    returndata['status'] = 401
                    returndata['msg'] = '登录失败'
                    returndata['error'] = '用户已注销'
                    return returndata
                user.token = str(uuid.uuid4())
                db.session.add(user)
                db.session.commit()
                returndata['status'] = 200
                returndata['msg'] = '验证成功'
                returndata['data'] = user
                return returndata
            else:
                returndata['status'] = 401
                returndata['msg'] = '登录失败'
                returndata['error'] = '用户密码错误'
                return returndata
        else:
            returndata['status'] = 401
            returndata['msg'] = '登录失败'
            returndata['error'] = '账号有误'
            return returndata