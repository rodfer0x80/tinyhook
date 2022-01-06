#!/bin/bash
PROGNAME="cred_harvester"
kill $(pgrep $PROGNAME) && echo -e "Program terminated" || echo "Program not running"