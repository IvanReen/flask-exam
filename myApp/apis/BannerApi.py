from flask_restful import fields, Resource, marshal_with

from myApp.models import Banner

banner_fields = {
    'bannerid':fields.Integer,
    'type': fields.Integer,
    'object_id': fields.Integer,
    'title': fields.String,
    'image': fields.String,
    'description': fields.String,
    'userid': fields.Integer,
}

result_fields = {
    'status': fields.Integer,
    'msg': fields.String,
    'data': fields.List(fields.Nested(banner_fields)),
    'error': fields.String(default='')
}

class BannerResource(Resource):

    @marshal_with(result_fields)
    def get(self):
        cinemas = Banner.query.order_by(-Banner.bannerid)
        return {'status': 200, 'msg': '获取数据成功', 'data': cinemas}