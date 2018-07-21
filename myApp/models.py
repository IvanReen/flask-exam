from myApp.ext import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(50), unique=True)
    phone = db.Column(db.String(20))
    token = db.Column(db.String(255))
    permissions = db.Column(db.Integer, default=1)
    icon = db.Column(db.String(255), default='head.png')
    isactive = db.Column(db.Boolean, default=False)
    isdelete = db.Column(db.Boolean, default=False)

class Banner(db.Model):
    # id
    bannerid = db.Column(db.Integer, primary_key=True)
    # 类型
    type = db.Column(db.Integer)
    # 组
    object_id = db.Column(db.Integer)
    # 名称
    title = db.Column(db.String(255), default='')
    # 图片
    image = db.Column(db.String(255))
    # 描述
    description = db.Column(db.String(255), default='')
    # 拥有者
    userid = db.Column(db.Integer)
    # 删除
    isdelete = db.Column(db.Boolean, default=False)

class Movies(db.Model):
    # id
    postid = db.Column(db.Integer, primary_key=True)
    # 名称
    title = db.Column(db.String(255))
    # 简介
    wx_small_app_title = db.Column(db.String(255))
    # 专题
    discussion = db.Column(db.Integer)
    # 封面
    image = db.Column(db.String(255))
    # 评分
    rating = db.Column(db.Float)
    # 时长
    duration = db.Column(db.String(255))
    # 上映时间
    publish_time = db.Column(db.String(255))
    # 点赞数
    like_num = db.Column(db.Integer)
    # 分享
    share_num = db.Column(db.Integer)
    # 类型
    post_type = db.Column(db.Integer)
    # 请求地址
    request_url = db.Column(db.String(255))
    # 标志
    tags = db.Column(db.Integer)
    # 删除
    isdelete = db.Column(db.Boolean, default=False)