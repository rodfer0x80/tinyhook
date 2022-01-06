#!/bin/bash
PROGNAME="tinnyHook"
kill $(pgrep $PROGNAME) && rm -f $PROGNAME && echo -e "Program terminated" || echo "Program not running"
