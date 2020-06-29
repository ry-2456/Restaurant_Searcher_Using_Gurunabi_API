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

@app.route("/gnavi", methods=["POST", "GET"])
def gnavi():
    api_url = "https://api.gnavi.co.jp/RestSearchAPI/v3"

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

    if request.method == "POST":
        search_radius = request.form["search_radius"]
        return render_template("filtering.html", search_radius=search_radius)

    elif request.method == "GET":
        return render_template("filtering.html")

if __name__ == "__main__":
    app.run(debug=True, host=get_local_ipaddr(), port=3000, threaded=True,
           ssl_context=("openssl/server.crt", "openssl/server.key")) 
