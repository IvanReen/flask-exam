import uuid

from flask_restful import reqparse, fields, Resource, marshal_with

from myApp.ext import cache, db
from myApp.models import User

parser = reqparse.RequestParser()
parser.add_argument('token', type=str, required=True, help='请输入token')

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

class UserResource(Resource):
    @marshal_with(result_fields)
    def get(self):
        parse = parser.parse_args()
        token = parse.get('token')

        returndata = {}
        userid = cache.get(token)
        if not userid:
            returndata['status'] = 201
            returndata['msg'] = '激活超时'
            returndata['error'] = '激活失败'
            return returndata
        else:
            cache.delete(token)
            user = User.query.get(userid)
            user.isactive = True
            user.token = str(uuid.uuid4())
            db.session.add(user)
            db.session.commit()
            returndata['status'] = 200
            returndata['msg'] = '激活成功'
            returndata['data'] = user
            return returndata