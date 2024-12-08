#!/bin/bash
# prepare
need_install=(
	clash
	cmake
	dunst
	fcitx5-chinese-addons
	fcitx5-gtk
	fcitx5-lua
	feh
	fzf
	gcc
	gvim
	lightdm-gtk-greeter
	make
	neofetch
	perl-module-build
	picom
	qt5-svg
	qt5-tools
	ranger
	tmux
	ueberzug
	wget
	xorg
)
packages=""
for package in ${need_install[@]}; do
	packages="$packages $package"
done

set -xe
sudo pacman -Syyu --noconfirm
sudo pacman -S $packages --needed --noconfirm 

# highway
mkdir -p ~/.clash
cp misc/Country.mmdb ~/.clash/

if [[ "$1" != "" ]]; then
	wget "$1" -O ~/.clash/clash.yaml
else
	read config
	echo $config > ~/.clash/clash.yaml
fi
clash -f ~/.config/clash/clash.yaml &
PID=$!

sleep 3
kill -0 $PID

# pull
git config --local http.server http://127.0.0.1:7890
git config --local https.server https://127.0.0.1:7890
git submodule update --init --depth=1
kill $PID
