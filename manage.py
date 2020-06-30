import socket
from rest_searcher import app
from rest_searcher.models import Restaurant

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

app.run(debug=True, host=get_local_ipaddr(), port=3000, threaded=True,
       ssl_context=("openssl/server.crt", "openssl/server.key")) 
