import time, os, socket, re, threading
from subprocess import getoutput as system
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

value = {
    "hook": "|",
    "todo": "",
    "wifi": "",
    "touchpad": "",
    "light": "",
    "sound": "",
    "battery": "",
    "date": "",
    "fcitx5": ""
}

display = {
    "hook": "",
    "todo": "",
    "wifi": "",
    "touchpad": "",
    "light": "",
    "sound": "",
    "battery": "",
    "date": "",
    "fcitx5": ""
}

def get_im():
    global value, display
    while True:
        state = system("fcitx5-remote")
        if state != value["fcitx5"]:
            value["fcitx5"] = state
            display["fcitx5"] = [' ', ' ', '^b#fb8feb^^c#443326^󱌱^d^'][int(state)]
            gen()
        time.sleep(.2)

def get_hook():
    global value, display
    state = "."
    if os.path.exists("/tmp/statusBar/hook"):
        with open("/tmp/statusBar/hook") as file:
            state = file.read().replace("\n", "")
    else:
        with open("/tmp/statusBar/hook", "w") as file:
            file.write(".")
    if state == "":
        return False
    if state != value["hook"]:
        value["hook"] = state
        if state == "." or state == "":
            display["hook"] = "^c#ffffff^ ^d^"
        else:
            display["hook"] = "^c#ffffff^" + state + "  "
        return True
    return False

def get_todo():
    global value, display
    with open("/tmp/statusBar/todo") as file:
        text = file.read().replace("\n", "")
    if text == "":
        return False
    if text != value["todo"]:
        value["todo"] = text
        if text == "|":
            display["todo"] = "^c#00bbbb^ ^d^"
        else:
            display["todo"] = f"^b#000000^^c#00bbbb^ {text} ^d^^c#00bbbb^  "
        return True
    return False

def get_touchpad():
    global value, display
    with open("/tmp/statusBar/touchpad") as file:
        enable = file.read().replace("\n", "")
    if enable == "":
        return False
    enable = int(enable)
    if enable != value["touchpad"]:
        value["touchpad"] = enable
        display["touchpad"] = ["^c#ff0000^ ^d^", "^c#ffff99^"" ""^d^"][enable]
        return True
    return False

def get_light():
    global value, display
    with open("/tmp/statusBar/light") as file:
        light = file.read().replace("\n", "")
    if light == "":
        return False
    if light != value["light"]:
        value["light"] = light
        display["light"] = light
        return True
    return False

def get_sound():
    global value, display
    with open("/tmp/statusBar/sound") as file:
        sound = file.read().replace("\n", "")
    if sound == "":
        return False
    if sound != value["sound"]:
        value["sound"] = sound
        if sound == "0":
            display["sound"] = "^c#ff8000^󰎊"
        elif sound != "100":
            display["sound"] = "^c#a8c8ff^󰎈" + sound
        else:
            display["sound"] = "^c#99ffcc^󰎈"
        return True
    return False

def timer():
    global display
    # wifi
    try:
        socket.create_connection(("www.baidu.com", 443), timeout = 2)
        wifi="^c#22ff55^󰞉 "
    except:
        wifi="^c#ffaabb^󰕑 "
    con_list = [i.split() for i in system("nmcli connection show --active").split('\n')][1:]
    ether = ""
    wifi_name = ""
    for i in con_list:
        if i[2] == "wifi":
            wifi_name = "󰢾 " + i[0]
        elif i[2] == "ethernet":
            ether = "󰴼"
    wifi += f"{ether}{wifi_name}^d^"
    display["wifi"] = wifi

    # battery - single battery
    info = system("acpi").split("\n")[0].split(",")
    info[0] = info[0].split(":")[1].replace(" ", "")
    info[1] = int(info[1].replace("\n", "").replace("%", "").replace(" ", ""))
    if info[0] == "Charging":
        battery = f"^c#f5d847^ ^d^{info[1]}"
    elif info[1] >= 95:
        battery = "^c#99ffcc^ ^d^"
    elif info[1] >= 60:
        battery = "^c#009900^ ^d^"
    elif info[1] >= 35:
        battery = "^c#4c9900^ ^d^"
    elif info[1] >= 30:
        battery = "^c#ff8000^ ^d^"
    else:
        battery = "^c#ff0000^ ^d^"
    display["battery"] = battery

    # date
    tm = time.localtime()
    date = "^c#cbcb6a^ ^d^{}:{} ^b#8b8feb^^c#443326^{}^d^".format(
        str(tm.tm_hour).zfill(2),
        str(tm.tm_min).zfill(2),
        ['一', '二', '三', '四', '五', '六', '日'][tm.tm_wday]
    )
    display["date"] = date

    return tm.tm_sec

fun = {
    "hook": get_hook,
    "todo": get_todo,
    "touchpad": get_touchpad,
    "light": get_light,
    "sound": get_sound
}

class FileChecker(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return
        if event.event_type in ['modified']:
            filename = event.src_path.split("/")[-1]
            if fun[filename]():
                gen()

event = FileChecker()
observer = Observer()
th = threading.Thread(target=get_im)
def init():
    path = "/tmp/statusBar/"
    if not os.path.exists(path):
        os.makedirs(path)
    # hook
    get_hook()

    # todo
    if not os.path.exists("/tmp/statusBar/todo"):
        if os.path.exists(os.path.expanduser("~/TODO")):
            system("cp ~/TODO /tmp/statusBar/todo")
        else:
            with open("/tmp/statusBar/todo", "w") as file:
                file.write("|")
    get_todo()

    # touchpad
    result = re.findall(r"id=([0-9]*)", system("xinput |grep TouchPad"))
    if len(result) != 0:
        id = result[0]
        enable = system(f"xinput list-props {id} |grep \"Device Enabled\"").replace("\t", "").replace(" ", "").split(":")[-1]
        with open("/tmp/statusBar/touchpad", "w") as file:
            file.write(enable)
        get_touchpad()

    # light
    with open("/sys/class/backlight/intel_backlight/brightness") as file:
        l_act = int(file.read())
    with open("/sys/class/backlight/intel_backlight/max_brightness") as file:
        l_mx = int(file.read())
    light = str(l_act * 100 // l_mx)
    with open("/tmp/statusBar/light", "w") as file:
        file.write(light)
    get_light()

    # sound
    info = system("amixer|grep 'Left: Playback'")
    if "off" in info:
        sound = "0"
    else:
        sound = re.findall(r"\[(.*)%\]", info)[0]
    with open("/tmp/statusBar/sound", "w") as file:
        file.write(sound)
    get_sound()

    # fcitx5
    th.start()

    # checker
    observer.schedule(event, "/tmp/statusBar/", recursive=False)
    observer.start()
    

def gen():
    cmd = "xsetroot -name '{}{} {} {} ^c#ffff99^ {} {} {} {}{}'".format(
        display["hook"],
        display["todo"],
        display["wifi"],
        display["touchpad"],
        display["light"],
        display["sound"],
        display["battery"],
        display["date"],
        display["fcitx5"]
    )
    os.system(cmd)

if __name__ == "__main__":
    init()
    while True:
        sed = timer()
        gen()
        time.sleep(60 - sed)
