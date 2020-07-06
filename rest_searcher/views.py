# -*- coding: utf-8 -*-
import json
import requests
from flask import Flask, render_template, url_for, request, redirect, session
from rest_searcher import app, db
from rest_searcher.models import Restaurant


@app.route("/formtest", methods=["POST", "GET"])
def formtest():
    # キーワード
    freeword = (request.form.get("freeword", default='', type=str)).strip() # ない場合None
    freeword = ','.join(freeword.split()) # 空白文字で区切りカンマで結合
    print("########################")
    print("freeword: {}".format(freeword))
    print()
    # キーワードcondition
    freeword_condition  = request.form.get("freeword_condition", type=int)
    print("freeword_condition: {}".format(['', "AND", "OR"][freeword_condition]))
    print()
    # メニュー
    lunch          = request.form.get("lunch", default=0, type=int) # ない場合None
    breakfast      = request.form.get("breakfast", default=0, type=int) # ない場合None
    late_lunch     = request.form.get("late_lunch", default=0, type=int) # ない場合None
    buffet         = request.form.get("buffet", default=0, type=int) # ない場合None
    bottomless_cup = request.form.get("bottomless_cup", default=0, type=int) # ない場合None
    print("lunch: {}".format(lunch))
    print("breakfast: {}".format(breakfast))
    print("late_lunch: {}".format(late_lunch))
    print("buffet: {}".format(buffet))
    print("bottomless_cup: {}".format(bottomless_cup))
    print()
    # web予約
    web_reserve    = request.form.get("web_reserve", default=0, type=int) # ない場合None
    print("web_reserve: {}".format(web_reserve))
    print()
    # お店以外で食べる 
    takeout    = request.form.get("takeout", default=0, type=int) # ない場合None
    deliverly    = request.form.get("deliverly", default=0, type=int) # ない場合None
    print("takeout: {}".format(takeout))
    print("deliverly: {}".format(deliverly))
    print()
    # 駐車場
    parking    = request.form.get("parking", default=0, type=int) # ない場合None
    print("parking: {}".format(parking))
    print()
    # 検索範囲
    search_radius_idx    = request.form.get("search_radius_idx", default=0, type=int) # ない場合None
    print("search_radius_idx: {}".format(search_radius_idx))
    print()
    # 支払い方法
    e_money    = request.form.get("e_money", default=0, type=int) # ない場合None
    card    = request.form.get("card", default=0, type=int) # ない場合None
    print("e_money: {}".format(e_money))
    print("card: {}".format(card))
    print("#########################")

    return render_template("filtering.html")

@app.route("/page")
def page():
    page = request.args.get('page', default=1, type=int)
    rests = db.session.query(Restaurant).order_by(
        Restaurant.id.asc()).paginate(page=page, per_page=10)
    # for rest in rests.items:
    #     print(rest)
    # print(len(rests.items))

    return render_template("page.html", rests=rests ,title="page")

@app.route("/receive_position", methods=["POST"])
def get_latitude_and_longitude():
    if request.method == "POST":
        # receive lat and lng from javascript
        current_position = request.get_json()
        lat = current_position["lat"]
        lng =  current_position["lng"]
        session["lat"] = lat
        session["lng"] = lng
        # print(url_for("gnavi")) # /gnavi
    return redirect(url_for("gnavi"))

@app.route("/pos")
def get_current_position():
    return render_template("current_pos.html", title="pos")


@app.route("/gnavi/<id>", methods=["POST", "GET"])
def gnavi_detail(id):
    # GETの場合はこれでパラメータを受け取れる
    id_test = request.args.get('page', default=1, type=int)
    print(id_test)

    rest = db.session.query(Restaurant).filter(Restaurant.id == id).first()
    return render_template("detailed_page.html", rest=rest)
    

@app.route("/", methods=["POST", "GET"])
@app.route("/gnavi", methods=["POST", "GET"])
def gnavi():
    # ぐるなびAPIのURL
    api_url = "https://api.gnavi.co.jp/RestSearchAPI/v3"

    if request.method == "GET":
        return render_template("filtering.html", title="gnavi")

    elif request.method == "POST":
        # Read gnavi API key
        with open("gnavi_apikey.txt") as f:
            api_key = f.read().strip()

        # delete all rows in Restaurant
        num_rows_deleted = db.session.query(Restaurant).delete()
        db.session.commit()
        print("num rows deleted : {}".format(num_rows_deleted))

        ######################### 検索条件の取得 ###################################
        # キーワード
        freeword = (request.form.get("freeword", default='', type=str)).strip() # ない場合None
        freeword = ','.join(freeword.split()) # 空白文字で区切りカンマで結合
        # キーワードcondition
        freeword_condition  = request.form.get("freeword_condition", type=int)
        # メニュー
        lunch          = request.form.get("lunch", default=0, type=int) 
        late_lunch     = request.form.get("late_lunch", default=0, type=int)
        buffet         = request.form.get("buffet", default=0, type=int) 
        breakfast      = request.form.get("breakfast", default=0, type=int)
        bottomless_cup = request.form.get("bottomless_cup", default=0, type=int)
        # web予約
        web_reserve    = request.form.get("web_reserve", default=0, type=int)
        # お店以外で食べる 
        takeout        = request.form.get("takeout", default=0, type=int)
        deliverly      = request.form.get("deliverly", default=0, type=int)
        # 駐車場
        parking        = request.form.get("parking", default=0, type=int)
        # 支払い方法
        e_money        = request.form.get("e_money", default=0, type=int)
        card           = request.form.get("card", default=0, type=int) 
        # 検索範囲
        search_radius_idx  = request.form.get("search_radius_idx", type=int) 

        # リクエストパラメータの設定
        params = {}
        params["keyid"] = api_key
        params["freeword"] = freeword
        params["freeword_condition"] = freeword_condition
        params["lunch"] = lunch
        params["late_lunch"] = late_lunch
        params["buffet"] = buffet
        params["breakfast"] = breakfast
        params["bottomless_cup"] = bottomless_cup
        params["web_reserve"] = web_reserve
        params["takeout"] = takeout
        params["deliverly"] = deliverly
        params["parking"] = parking
        params["e_money"] = e_money
        params["card"] = card
        # params["range"] = search_radius_idx
        params["hit_per_page"] = 100 # 取得件数

        # 現在位置の指定
        # if session.get("lat") is not None and session.get("lng") is not None:
        #     params["latitude"] = round(session["lat"], 6)
        #     params["longitude"] = round(session["lat"], 6)
        #     search_radius_idx = request.form["search_radius_idx"]
        #     params["range"] = int(search_radius_idx)

        # リクエスト結果
        res = requests.get(api_url, params)
        res = res.json()

        # error handling
        if res.get("error"):
            err_msg = res["error"][0]["message"]
            err_code = res["error"][0]["code"]
            return err_msg, err_code

        # レスポンス中のレストランの数
        cnt = len(res["rest"])

        # レストランを
        restaurants = []
        longest_pr_length = 0
        for i in range(cnt):
            if len(res["rest"][i]["opentime"]) < 60: continue
            # アクセス
            line = res["rest"][i]["access"]["line"]
            station = res["rest"][i]["access"]["station"]
            station_exit = res["rest"][i]["access"]["station_exit"]
            walk = res["rest"][i]["access"]["walk"]
            access = line + station + station_exit + "より"
            if '車' in walk: access = access + walk + '分'
            else:            access = access + "徒歩" + str(walk) + '分'

            rest = Restaurant(
                        name = res["rest"][i]["name"],
                        img_url1 = res["rest"][i]["image_url"]["shop_image1"],
                        img_url2 = res["rest"][i]["image_url"]["shop_image2"],
                        address = res["rest"][i]["address"],
                        tel = res["rest"][i]["tel"],
                        opening_hours = res["rest"][i]["opentime"],
                        access = access,
                        holiday = res["rest"][i]["holiday"],
                        pr_long = res["rest"][i]["pr"]["pr_long"],

                        budget = str(res["rest"][i]["budget"]),
                        party = str(res["rest"][i]["party"]),
                        lunch = str(res["rest"][i]["lunch"]),

                        parking_lots = str(res["rest"][i]["parking_lots"]),

                        credit_card = res["rest"][i]["credit_card"],
                        e_money = res["rest"][i]["e_money"],

                        coupon_pc_url = res["rest"][i]["coupon_url"]["pc"],
                        coupon_mobile_url = res["rest"][i]["coupon_url"]["mobile"],
                   )

            restaurants.append(rest)
            print("############################")
            print("budget: ", res["rest"][i]["budget"])
            print("party: ", res["rest"][i]["party"])
            print("lunch: ", res["rest"][i]["lunch"]) 
            print(type(res["rest"][i]["lunch"]))
            print("############################")

        # add_restaurat_to_db(restaurant)
        db.session.add_all(restaurants)  
        db.session.commit()

        # get target="_blank" all rows
        all_restaurant_info = db.session.query(Restaurant).all()

        # receive search radius idx 
        # search_radius_idx = request.form["search_radius_idx"] # ない場合raise error
        search_radius_idx = request.form.get("search_radius_idx") # ない場合None

        search_radius = {"1":300, "2":500, "3":1000, "4":2000, "5":3000}[search_radius_idx]

        return redirect(url_for('page'))
        # return render_template("filtering.html", 
        #     search_radius=search_radius, rests=all_restaurant_info, title="gnavi")



##########################################################################################
# @app.route("/")
# def home():
#     return "home"
# 
# @app.route("/test")
# def test():
#     # name = request.form.get("name", default="unko", type=str) # ない場合None
#     name = request.args.get("name")
#     print(name)
#     return name
# 
# @app.route("/test1/<string:username>")
# def test1(username):
#     print(type(username))
#     return username
# 
# @app.route("/test2/<username>")
# def test2(username):
#     return username
