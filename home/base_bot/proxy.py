proxy_list = [
    ("38.240.5.132", 1080),
]


def get_proxy():
    ip, port = proxy_list[0]
    return "socks5://%s:%s" % (ip, port)
