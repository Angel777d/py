proxy_list = [
    ("150.109.195.10", 1080),
    ("103.21.161.105", 6667),
    ("37.59.8.29", 10692),
    ("211.159.158.94", 1080),
]


def get_proxy():
    ip, port = proxy_list[0]
    return "socks5://%s:%s" % (ip, port)
