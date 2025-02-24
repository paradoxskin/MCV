#!/bin/bash
set -xe
# fn
function link_dot() {
    for from in $@; do
        target="$HOME/.$from"
        rm -rf $target
        ln -s $(realpath dot/$from) $target
    done
}
function copy_dot() {
    for dot in $@; do
        cp -rf dot/$dot "$HOME/.$dot"
    done
}
function suckless_build() {
    for build in $@; do
        cd software/$build
        sudo make clean install
        cd -
    done
}
function link_conf() {
    for from in $@; do
        target="$HOME/.config/$from"
        rm -rf $target
        ln -s $(realpath conf/$from) $target
    done
}
function copy_conf() {
    for conf in $@; do
        cp -rf conf/$conf ~/.config/
    done
}

# move
# .fonts
sudo cp -rf misc/fonts /usr/share/fonts/
sudo fc-cache

# .lightdm
cp -rf Pictures/ ~
sudo mkdir -p /usr/share/xsessions
sudo cp -f misc/lightdm/dwm.desktop /usr/share/xsessions/
sudo cp -rf misc/lightdm/lightdm_wp /usr/share/pixmap/
sudo cp -f misc/lightdm/lightdm-gtk-greeter.conf /etc/lightdm/
sudo cp -rf misc/lightdm/mytheme/ /usr/share/themes/

# .flypy
sudo libime_tabledict misc/flypy-dict/fcitx5/flypy.txt /usr/share/libime/flypy.dict
sudo cp -f misc/flypy-dict/fcitx5/flypy.conf /usr/share/fcitx5/inputmethod/
echo "GTK_IM_MODULE=fcitx
QT_IM_MODULE=fcitx
XMODIFIERS=@im=fcitx
SDL_IM_MODULE=fcitx
GLFW_IM_MODULE=ibus" |sudo tee /etc/environment

# .dot
link_dot bashrc scripts tmux.conf vim
copy_dot dwm rainbarf.conf Xmodmap
cp -rf dot/local/* ~/.local/
cat dot/profile >> ~/.profile
cat dot/xprofile > ~/.xprofile

# .config
mkdir -p ~/.config
link_conf flameshot picom.conf ranger
copy_conf dunst fcitx5 neofetch

# .touchpad
sudo cp misc/30-touchpad.conf /etc/X11/xorg.conf.d/

# weap0n
suckless_build cstatusbar dmenu dwm slock st

cd software/rainbarf/
perl Build.PL
./Build test
sudo ./Build install
cd -

mkdir -p software/flameshot/build
cd software/flameshot/build
cmake ..
sudo make install
cd -

cd software/todo.txt-cli
make
sudo make install
mkdir -p ~/.todo
cp -f /usr/local/etc/todo/config ~/.todo/
cd -
