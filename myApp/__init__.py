from flask import Flask

from myApp.apis import init_api
from myApp.ext import init_ext
from myApp.settings import config


def create_app(env_name=None):
    app = Flask(__name__)
    app.config.from_object(config.get(env_name or 'default'))
    init_ext(app)
    init_api(app)

    return app