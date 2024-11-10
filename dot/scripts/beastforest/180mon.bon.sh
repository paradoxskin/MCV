#!/bin/bash

xrandr -o 2

for id in $(xinput list|grep Wacom |grep pointer |sed -n 's/.*id=\([^\t]*\).*/\1/p'); do
    xinput set-prop $id --type=float "Coordinate Transformation Matrix" -1 0 1 0 -1 1 0 0 1
done
