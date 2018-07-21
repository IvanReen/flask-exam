from flask import render_template
from flask_caching import Cache
from flask_mail import Mail, Message
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
cache = Cache(config={
    'CACHE_TYPE':'redis',
})

def init_ext(app):
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    cache.init_app(app)

def send_mail(user):
    msg = Message(
        subject='豆瓣账号激活邮件',
        recipients=[user.email],
        sender='small_pupil@163.com'
    )
    active_url = 'http://127.0.0.1:5000/api/v1/user/?token=' + user.token
    body_html = render_template('useractive.html', name=user.name, active_url=active_url)
    msg.html = body_html
    mail.send(msg)
    cache.set(user.token, user.id, timeout=60)