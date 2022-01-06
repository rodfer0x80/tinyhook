#!/bin/bash
PROGNAME="tinnyHook"
kill $(pgrep $PROGNAME) && echo -e "Program terminated" || echo "Program not running"
