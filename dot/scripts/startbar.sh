#!/bin/bash

cstatusbar &
amixer get Master |awk -F '[]%[]' 'END{printf "V;%d\n", $2}' > /tmp/dwm.fifo
~/.scripts/bgl
echo "T;$(cat ~/TODO)" > /tmp/dwm.fifo
