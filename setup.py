#!/usr/bin/python3

import getpass


if __name__ == '__main__':
    proggie = "main.go"
    dropper = "dropper/wifigrabber.ino"
    if not environ.get('CH_PASSWD'):
        print("CH_PASSWD environmental variable not set")
        passwd = getpass.getpass("CH_PASSWD >>> ")
        system(f"export CH_PASSWD={passwd}")
    interface = input("INTERFACE >>> ")
    port = input("PORT >>> ")
    # get IP and PORT to host server
    with open(proggie, "r") as fp:
        code = fp.read()
    new_code = ""
    for line in code:
        if "const INTERFACE =" in line:
            line = f"const INTERFACE = {interface}"
        if "const PORT =" in line::
            line = f"const PORT = {port}"
        new_code += line
    with open(proggie), "w") as fp:
        fp.write(new_code)
    with open(dropper, "r") as fp:
        code = fp.read()
    new_code = ""
    for line in code:
        if "#define INTERFACE" in line:
            line = f"#define INTERFACE = {interface}"
        if "#define PORT" in line:
            line = f"#define PORT = {port}"
        new_code += line
    with open(dropper, "w") as fp:
        fp.write(new_code)



    # change IP and PORT in all files
    # alert when done what
    exit(0)
