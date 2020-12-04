from x_msgpack import serialize


def get_message() -> bytes:
    # list of (index, server_addr, alert_level)
    # server_addr =  (addr_type, addr)
    alert_level_list = [
        (0, (0, b"\x3c\x71\xbf\xf4\x64\x56"), b"\x02"),
        (1, (0, b"\x3c\x71\xbf\xfe\x6d\x66"), b"\x00"),
    ]

    # =====
    print("[Choise]")
    for k in locals():
        print("-", k)
    del k
    choise = input("Your selection : ")
    if choise == "choise" or choise not in locals():
        return b"\x14\xfb\x9c\x03\xd9\x7e"
    return serialize(locals()[choise])
