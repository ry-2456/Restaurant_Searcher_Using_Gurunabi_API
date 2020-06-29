import requests
import socket
from flask import Flask, render_template, url_for, request

app = Flask(__name__)

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

@app.route("/gnavi")
def gnavi():
    api_url = "https://api.gnavi.co.jp/RestSearchAPI/v3"

    # Read gnavi API key
    with open("gnavi_apikey.txt") as f:
        apikey = f.read().strip()

    # Set parameters
    params = {}
    params["keyid"] = apikey
    params["freeword"] = "居酒屋"
    params["hit_per_page"] = 100

    # Request result
    res = requests.get(api_url, params)
    res = res.json()
     
    cnt = len(res["rest"])
    for i in range(cnt):
        print("===============================")
        print("line: {}".format(res["rest"][i]["access"]["line"]))
        print("station: {}".format(res["rest"][i]["access"]["station"]))
        print("station_exit: {}".format(res["rest"][i]["access"]["station_exit"]))
        print("walk: {}".format(res["rest"][i]["access"]["walk"]))
        print("note: {}".format(res["rest"][i]["access"]["note"]))

        print(res["rest"][i]["name"])
        print(res["rest"][i]["address"])
        print(res["rest"][i]["tel"])
        print(res["rest"][i]["opentime"])

        print(res["rest"][i]["image_url"]["shop_image1"])
        print(res["rest"][i]["image_url"]["shop_image2"])
        print(res["rest"][i]["image_url"]["qrcode"])
        print("===============================\n")
    return "gnavi"

if __name__ == "__main__":
    app.run(debug=True, host=get_local_ipaddr(), port=3000, threaded=True,
           ssl_context=("openssl/server.crt", "openssl/server.key")) 
