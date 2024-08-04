#! /bin/bash
mkfifo /tmp/dwm.fifo
#picom --config ~/.config/picom.conf &
#/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
#flameshot &
#~/.scripts/cgbg
#fcitx5 -d;sleep 3
#xmodmap ~/.Xmodmap
#~/.scripts/startbar.sh
st -A 0.7 -e ~/.scripts/tmux.sh &
