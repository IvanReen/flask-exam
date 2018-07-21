from flask_restful import Api

from myApp.apis.BannerApi import BannerResource
from myApp.apis.IconChange import IconChange
from myApp.apis.LoginApi import Login
from myApp.apis.MovieApi import MoviesResource
from myApp.apis.RegisterApi import Register
from myApp.apis.UserApi import UserResource
from myApp.apis.PasswordChange import PasswordChange
from myApp.apis.UserInfo import UserInfoChange

api = Api()

def init_api(app):
    api.init_app(app)

api.add_resource(Register, '/api/v1/register/', endpoint='register')
api.add_resource(Login, '/api/v1/login/', endpoint='login')
api.add_resource(UserResource, '/api/v1/user/', endpoint='user')
api.add_resource(MoviesResource, '/api/v1/movie/', endpoint='movie')
api.add_resource(BannerResource, '/api/v1/banner/', endpoint='banner')
# api.add_resource(PasswordChange, '/api/v1/pwd/', endpoint='changeinfo')
# api.add_resource(IconChange, '/api/v1/icon/', endpoint='icon')
api.add_resource(UserInfoChange, '/api/v1/userinfo/', endpoint='userinfo')