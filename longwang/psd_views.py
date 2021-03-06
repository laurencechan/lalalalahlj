# -*- coding: utf-8 -*-#
# filename:psd_views.py

import json
import pymongo
from flask import Blueprint, render_template, abort
from connect import conn
from longwang.mongodb_news import get_image_news, search_news_db, get_head_image, image_server, datetime_op, \
    search_indexnews_db, \
    get_mongodb_dict
from bson import ObjectId

from longwang.pager.pager import pager

db = conn.mongo_conn()
psd_page = Blueprint('psd_page', __name__, template_folder='templates')

pre_page = 10


# 二级频道首页
@psd_page.route('/psd/')
def psd_index():
    detail = db.Channel.find_one({"_id": ObjectId("576500d7dcc88e31a6f3500d")})
    # 轮换图
    lht = get_head_image(ObjectId("576500d7dcc88e31a6f3500d"), 4)
    # 头条新闻
    ttxw = get_image_news("577c646159f0d8efacae7e65", 6)
    # 今日热评文字1
    # jrrp_1 = get_image_news("577c647559f0d8efacae7e68", 1)
    # 今日热评图片1
    jrrp_2 = get_image_news("577c647559f0d8efacae7e68", 1)
    # 今日热评文字3
    jrrp_5 = get_image_news("577c647559f0d8efacae7e68", 4, jrrp_2)
    # 独家视界
    djsj = get_image_news("577c648559f0d8efacae7e6b", 10)
    # 当事者说
    dszs = get_image_news("577c649059f0d8efacae7e6e", 4)
    # 排行24
    ph_24 = get_image_news("576b37b8a6d2e970226062d1", 8)
    # 排行周
    ph_week = get_image_news("576b37cda6d2e970226062d4", 8)
    # 排行月
    ph_month = get_image_news("576b37daa6d2e970226062d7", 8)
    # 专题
    zt_images = get_head_image("5765057edcc88e31a7d2e4c6", 4)
    zt = search_indexnews_db("579584633c7e431eaf791a06", 3)
    # 今日热评
    jrrp = search_news_db([ObjectId("5782f547dcc88e7769576fbd")], 5)
    # 政治经济
    zzjj = search_news_db([ObjectId("5782f5cadcc88e7769576fc0")], 5)
    # 社会民生
    shms = search_news_db([ObjectId("5782f5d2dcc88e776838c3f4")], 5)
    # 文化娱乐
    whyl = search_news_db([ObjectId("5782f5dadcc88e7769576fc1")], 5)
    # 教育科技
    jykj = search_news_db([ObjectId("578311fadcc88e4cb57770c3")], 5)
    # 合作媒体
    hzmt = db.Media.find({"ChannelID": ObjectId("576500d7dcc88e31a6f3500d")})
    menu1 = db.Channel.find({"Parent": ObjectId("576500d7dcc88e31a6f3500d"), "Visible": 1}).sort("OrderNumber")
    return render_template('psd/psd_index.html',
                           lht=lht,
                           ttxw=ttxw,
                           # jrrp_1=jrrp_1,
                           jrrp_2=jrrp_2,
                           jrrp_5=jrrp_5,
                           djsj=djsj,
                           dszs=dszs,
                           ph_24=ph_24,
                           ph_month=ph_month,
                           ph_week=ph_week,
                           zt=zt,
                           zt_images=zt_images,
                           jrrp=jrrp,
                           zzjj=zzjj,
                           shms=shms,
                           detail=detail,
                           whyl=whyl,
                           jykj=jykj,
                           hzmt=hzmt,
                           ys="sy",
                           menu=menu1
                           )


# 二级频道列表
@psd_page.route('/psd/')
@psd_page.route('/psd/<id>/<page>/')
def kbg_list(id, page=1):
    channel = db.Channel.find_one({"numid": int(id)})["_id"]
    condition = {"Channel": {"$in": [ObjectId(channel)]}, "Status": 4}
    news_list = db.News.find(condition).sort('Published', pymongo.DESCENDING).skip(
        pre_page * (int(page) - 1)).limit(
        pre_page)
    value = ""
    for i in news_list:
        style = 'style="display: block"'
        if i["Guideimage"] == "":
            style = 'style="display: none"'
        value += "<li><p %s><a href='/d/%s.html' target='_blank'><img src='%s?w=261&h=171' width='261' height='171'/></a></p><h2><a href='/d/%s.html' target='_blank'>%s</a></h2> \
        <h5>%s</h5> <h6>&nbsp;&nbsp;&nbsp;%s</h6></li>" % (
            style, i["numid"], image_server + i["Guideimage"], i["numid"], i["Title"], i["Summary"],
            datetime_op((i["Published"])))
    return json.dumps(value)


# 二级频道列表
@psd_page.route('/psd/<id>.html')
@psd_page.route('/psd/<id>_<page>.html')
def psd_list(id, page=1):
    try:
        channel = db.Channel.find_one({"numid": int(id)})["_id"]
        # 轮换头图
        lht = get_head_image(ObjectId(channel), 5)
        # 新闻列表
        condition = {"Channel": {"$in": [ObjectId(channel)]}, "Status": 4}
        count = db.News.find(condition).sort('Published', pymongo.DESCENDING).count()
        news_list = db.News.find(condition).sort('Published', pymongo.DESCENDING).skip(
            pre_page * (int(page) - 1)).limit(
            pre_page)
        _news_list = []
        for i in news_list:
            _news_list.append(get_mongodb_dict(i))
        pagenums, pagebar_html = pager("/psd/" + str(id), int(page), count, pre_page).show_page()
        # 今日热评文字1
        # jrrp_1 = get_image_news("577c647559f0d8efacae7e68", 1)
        # 今日热评图片1
        jrrp_2 = get_image_news("577c647559f0d8efacae7e68", 1)
        # 今日热评文字3
        jrrp_5 = get_image_news("577c647559f0d8efacae7e68", 3, jrrp_2)
        # 独家视界
        djsj = get_image_news("577c648559f0d8efacae7e6b", 10)
        # 当事者说
        dszs = get_image_news("577c649059f0d8efacae7e6e", 3)
        # 排行24
        ph_24 = get_image_news("576b37b8a6d2e970226062d1", 8)
        # 排行周
        ph_week = get_image_news("576b37cda6d2e970226062d4", 8)
        # 排行月
        ph_month = get_image_news("576b37daa6d2e970226062d7", 8)
        # 专题
        zt_images = get_head_image("5765057edcc88e31a7d2e4c6", 4)
        zt = search_indexnews_db("579584633c7e431eaf791a06", 3)
        # # 合作媒体
        # hzmt = db.Media.find({"ChannelID": ObjectId("576500f0dcc88e31a7d2e4ba")})
        # 频道
        menu1 = db.Channel.find({"Parent": ObjectId("576500d7dcc88e31a6f3500d"), "Visible": 1}).sort("OrderNumber")
        detail = db.Channel.find_one({"_id": ObjectId(channel)})
        # name = get_name(channel)
        return render_template('psd/psd_list.html', lht=lht,
                               c_list=_news_list,
                               jrrp_2=jrrp_2,
                               jrrp_5=jrrp_5,
                               djsj=djsj,
                               dszs=dszs,
                               ph_24=ph_24,
                               ph_month=ph_month,
                               ph_week=ph_week,
                               zt=zt,
                               zt_images=zt_images,
                               detail=detail,
                               menu=menu1,
                               cid=ObjectId(channel),
                               pagebar_html=pagebar_html
                               )
    except:
        abort(404)


# 二级频道分页
# @psd_page.route('/psd/list/<id>/')
# @psd_page.route('/psd/list/<id>/<page>')
def news_list_page(id, page=1):
    channel = db.Channel.find_one({"numid": int(id)})["_id"]
    condition = {"Channel": {"$in": [ObjectId(channel)]}, "Status": 4}
    news_list = db.News.find(condition).sort('Published', pymongo.DESCENDING).skip(
        pre_page * (int(page) - 1)).limit(
        pre_page)
    value = ""
    for i in news_list:
        style = 'style="display: block"'
        if i["Guideimage"] == "":
            style = 'style="display: none"'
        value += "<li %s><p %s><a href='/d/%s.html' target='_blank'><img src='%s?w=261&h=171' width='261' height='171'/></a></p><h2><a href='/d/%s.html' target='_blank'>%s</a></h2> <h5>%s</h5> <h6>&nbsp;&nbsp;&nbsp;%s</h6></li>" % \
                 (style, style, i["numid"], image_server + i["Guideimage"], i["numid"], i["Title"], i["Summary"],
                  datetime_op((i["Published"])))
    return json.dumps(value)


def get_name(channel):
    name = db.Channel.find_one({"_id": ObjectId(channel)})["Name"]
    return name
