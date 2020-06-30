import requests
import socket
#from flask import Flask, render_template, url_for, request
from flask import render_template, url_for, request
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import Column, Integer, String, Text
from rest_seacher import app, db
from rest_seacher.models import Restaurant

# app = Flask(__name__)
# app.config["SECRET_KEY"] = "secret key"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///restaurant.db" # path to db
# 
# db = SQLAlchemy(app)
# 
# class Restaurant(db.Model):
# 
#     __tablename__ = "restaurants"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     img_url1 = db.Column(db.String)
#     img_url2 = db.Column(db.String)
#     address = db.Column(db.String)
#     tel = db.Column(db.String)
#     # opening_hours = db.Column(String)
#     opening_hours = db.Column(db.Text)
# 
#     def __repr__(self):
#         return "<Restaurant name={} img_url1={} img_url2={}".format(
#             self.name, self.img_url1, self.img_url2)
# 
# db.create_all()
# 
def add_restaurat_to_db(restaurant):
    "add restaurant info to database"
    db.session.add(restaurant)
    db.session.commit()

def get_local_ipaddr():
    "Get local IP address"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 53))
        ipaddr = s.getsockname()[0]
    except socket.error as e:
        print(e)
        ipaddr = '127.0.0.1'
    finally:
        s.close()
    return ipaddr

@app.route("/")
def home():
    return "home"

@app.route("/gnavi", methods=["POST", "GET"])
def gnavi():
    api_url = "https://api.gnavi.co.jp/RestSearchAPI/v3"

    # delete all rows in Restaurant
    num_rows_deleted = db.session.query(Restaurant).delete()
    db.session.commit()
    print("num rows deleted : {}".format(num_rows_deleted))

    if request.method == "GET":
        return render_template("filtering.html")

    elif request.method == "POST":

        # Read gnavi API key
        with open("gnavi_apikey.txt") as f:
            api_key = f.read().strip()

        # Set parameters
        params = {}
        params["keyid"] = api_key
        params["freeword"] = "居酒屋"
        params["hit_per_page"] = 100

        # Request result
        res = requests.get(api_url, params)
        res = res.json()
         
        # Searched num
        cnt = len(res["rest"])

        # Add restaurant info to database
        restaurants = []
        for i in range(cnt):
            restaurants.append(
                Restaurant(
                    name=res["rest"][i]["name"],
                    img_url1 = res["rest"][i]["image_url"]["shop_image1"],
                    img_url2 = res["rest"][i]["image_url"]["shop_image2"],
                    address = res["rest"][i]["address"],
                    tel = res["rest"][i]["tel"],
                    opening_hours = res["rest"][i]["opentime"]
                )
            )
            db.session.add_all(restaurants)  
            db.session.commit()

            # add_restaurat_to_db(restaurant)

        all_restaurant_info = db.session.query(Restaurant).all()

        search_radius = request.form["search_radius"]
        return render_template("filtering.html", 
            search_radius=search_radius, rests=all_restaurant_info)

if __name__ == "__main__":
    app.run(debug=True, host=get_local_ipaddr(), port=3000, threaded=True,
           ssl_context=("openssl/server.crt", "openssl/server.key")) 
