import json
import requests
from flask import Flask, render_template, url_for
from flask import request, redirect, session
from rest_searcher import app, db
from rest_searcher.models import Restaurant

# @app.route("/")
# def home():
#     return "home"

@app.route("/test1/<string:username>")
def test1(username):
    print(type(username))
    return username

@app.route("/test2/<username>")
def test2(username):
    return username

@app.route("/page")
def page():
    page = request.args.get('page', default=1, type=int)
    rests = db.session.query(Restaurant).order_by(
        Restaurant.id.asc()).paginate(page=page, per_page=3)
    for rest in rests.items:
        print(rest)
    print(len(rests.items))

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
    rest = db.session.query(Restaurant).filter(Restaurant.id == id).first()
    return render_template("detailed_page.html", rest=rest)
    
@app.route("/gnavi", methods=["POST", "GET"])
def gnavi():
    api_url = "https://api.gnavi.co.jp/RestSearchAPI/v3"

    # delete all rows in Restaurant
    # num_rows_deleted = db.session.query(Restaurant).delete()
    # db.session.commit()
    # print("num rows deleted : {}".format(num_rows_deleted))

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

        # Set parameters
        params = {}
        params["keyid"] = api_key
        params["freeword"] = "居酒屋"
        params["hit_per_page"] = 100

        # if session.get("lat") is not None and session.get("lng") is not None:
        #     params["latitude"] = round(session["lat"], 6)
        #     params["longitude"] = round(session["lat"], 6)
        #     search_radius_idx = request.form["search_radius_idx"]
        #     params["range"] = int(search_radius_idx)

        # Request result
        res = requests.get(api_url, params)
        res = res.json()

        # error handling
        if res.get("error"):
            err_msg = res["error"][0]["message"]
            err_code = res["error"][0]["code"]
            # return err_msg, err_code
            return err_msg, err_code

        # Searched num
        cnt = len(res["rest"])

        # Add restaurants to database
        restaurants = []
        for i in range(cnt):
            rest = Restaurant(
                        name=res["rest"][i]["name"],
                        img_url1 = res["rest"][i]["image_url"]["shop_image1"],
                        img_url2 = res["rest"][i]["image_url"]["shop_image2"],
                        address = res["rest"][i]["address"],
                        tel = res["rest"][i]["tel"],
                        opening_hours = res["rest"][i]["opentime"]
                   )
            restaurants.append(rest)

        # add_restaurat_to_db(restaurant)
        db.session.add_all(restaurants)  
        db.session.commit()

        # get target="_blank" all rows
        all_restaurant_info = db.session.query(Restaurant).all()

        # receive search radius idx 
        search_radius_idx = request.form["search_radius_idx"]

        search_radius = {"1":300, "2":500, "3":1000, "4":2000, "5":3000}[search_radius_idx]

        return redirect(url_for('page'))
        # return render_template("filtering.html", 
        #     search_radius=search_radius, rests=all_restaurant_info, title="gnavi")
