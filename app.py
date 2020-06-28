import socket

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


if __name__ == "__main__":
    print(get_local_ipaddr())
