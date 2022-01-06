#!/usr/bin/python3


from os import environ, fork, system
import getpass

def daemon(cmd: str):
    pid2 = fork()
    if pid2 == 0:
        pid = fork()
        if pid == 0:
            system(cmd)
    exit(0)


if __name__ == '__main__':
    if not environ.get('CH_PASSWD'):
        print("CH_PASSWD environmental variable not set")
        passwd = getpass.getpass("Enter CH_PASSWD\n>>> ")
        system(f"export CH_PASSWD={passwd}")
    progname = "tinnyHook"
    logfile = "server.log"
    cmd = f"go build && ./{progname} 1>>{logfile} 2>/dev/null"
    daemon(cmd)
