from flask_restful import reqparse, fields, Resource, abort, marshal_with

from myApp.ext import db
from myApp.models import Movies, User

# 请求数据
parser_get = reqparse.RequestParser()
parser_get.add_argument('postid', type=int)

parser_post = reqparse.RequestParser()
parser_post.add_argument('token', type=str, required=True, help='缺少token')
parser_post.add_argument('postid', type=int, required=True, help='缺少id')
parser_post.add_argument('title', type=str, required=True, help='缺少中文名')
parser_post.add_argument('wx_small_app_title', type=str, required=True, help='缺少简介')
parser_post.add_argument('discussion', type=str, required=True, help='缺少专题')
parser_post.add_argument('image', type=str, required=True, help='缺少封面')
parser_post.add_argument('rating', type=str, required=True, help='缺少评分')
parser_post.add_argument('duration', type=str, required=True, help='缺少时长')
parser_post.add_argument('publish_time', type=str, required=True, help='缺少上映时间')
parser_post.add_argument('post_type', type=str, required=True, help='缺少类型')
parser_post.add_argument('request_url', type=str, required=True, help='缺少请求地址')
parser_post.add_argument('tags', type=int, help='缺少标志位')

# 响应数据
movie_fields = {
    'postid':fields.Integer,
    'title':fields.String,
    'wx_small_app_title':fields.String,
    'discussion':fields.Integer,
    'image':fields.String,
    'rating':fields.Float,
    'duration':fields.String,
    'publish_time':fields.String,
    'like_num':fields.Integer,
    'share_num':fields.Integer,
    'post_type':fields.Integer,
    'request_url':fields.String,
    'tags':fields.Integer
}

result_fields_get = {
    'status': fields.Integer,
    'msg': fields.String,
    'data': fields.List(fields.Nested(movie_fields)),
    'error': fields.String(default='')
}

result_fields_post = {
    'status': fields.Integer,
    'msg': fields.String,
    'data': fields.Nested(movie_fields),
    'error': fields.String(default='')
}

# 权限
ADMIN = 8
def check_permission_control(permission):
    def check_permission(func):
        def check(*args, **kwargs):
            parse = parser_post.parse_args()
            if token := parse.get('token'):
                users = User.query.filter(User.token == token)
                if users.count() > 0:
                    user = users.first()
                    if user.permissions & permission == permission:
                        return func(*args, **kwargs)
                    else:
                        abort(403, message='你没有权限，请联系管理员')
                else:
                    abort(403, message='你还没有登录，请登录后操作')
            else:
                abort(403, message='你还没有登录，请登录后操作')
        return check
    return check_permission

class MoviesResource(Resource):
    @marshal_with(result_fields_get)
    def get(self):
        parse = parser_get.parse_args()
        if postid := parse.get('postid'):
            movies = Movies.query.filter(Movies.postid == postid).filter(Movies.isdelete == False)
        else:
            movies = Movies.query.all()
        return {'status': 200, 'msg': '数据获取成功', 'data': movies}

    @check_permission_control(ADMIN)
    @marshal_with(result_fields_post)
    def post(self):
        parse = parser_post.parse_args()
        movie = Movies()
        movie.id = parse.get('postid')
        movie.showname = parse.get('title')
        movie.shownameen = parse.get('wx_small_app_title')
        movie.director = parse.get('discussion')
        movie.leadingRole = parse.get('image')
        movie.type = parse.get('rating')
        movie.country = parse.get('duration')
        movie.language = parse.get('publish_time')
        movie.duration = parse.get('post_type')
        movie.screeningmodel = parse.get('request_url')

        db.session.add(movie)
        db.session.commit()
        return {'status': 200, 'msg': '数据获取成功', 'data': movie}