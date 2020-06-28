import socket
from flask import Flask, render_template, url_for, request

app = Flask(__name__)

def get_local_ipaddr():
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

if __name__ == "__main__":
    app.run(debug=True, host=get_local_ipaddr(), port=5000, threaded=True,
           ssl_context=("openssl/server.crt", "openssl/server.key")) 
    print(get_local_ipaddr())
