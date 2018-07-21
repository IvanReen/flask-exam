import json

import sqlite3

db = sqlite3.connect('sql_exam.db')

cursor = db.cursor()

# 打开文件
with open('01-轮播图.json', 'r') as f:
    # json对象
    city_collection = json.load(f)
    # 获取data的数据
    data = city_collection.get('data')
    print(data)
    # 获取所有的键
    for i in range(9):
        datas = data[i]
        cursor.execute('insert into banner(bannerid,type,object_id,title,image,description,userid,isdelete) values ("{}","{}","{}","{}","{}","{}","{}","{}")'.format(str(datas.get('bannerid')), datas.get('type'), datas.get('object_id'), datas.get('title'), datas.get('image'), datas.get('description'), datas.get('userid'), 0))

        db.commit()
    db.close()


#
# # 打开文件
# with open('02-电影列表.json', 'r') as f:
#     # json对象
#     city_collection = json.load(f)
#     # 获取data的数据
#     data = city_collection.get('data')
#     print(data)
#     # 获取所有的键
#     for i in range(10):
#         datas = data[i]
#         cursor.execute('insert into movies(postid,title,wx_small_app_title,discussion,image,rating,duration,publish_time,like_num,share_num,post_type,request_url,tags,isdelete) values ("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")'.format(str(datas.get('postid')), datas.get('title'), datas.get('wx_small_app_title'), datas.get('discussion'), datas.get('image'), datas.get('rating'), datas.get('duration')+'分钟', datas.get('publish_time'), datas.get('like_num'), datas.get('share_num'), datas.get('post_type'), datas.get('request_url'), datas.get('tags'), 0))
#
#         db.commit()
#     db.close()