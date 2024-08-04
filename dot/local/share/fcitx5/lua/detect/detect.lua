local fcitx = require("fcitx")

fcitx.watchEvent(fcitx.EventType.FocusIn, "notify")
fcitx.watchEvent(fcitx.EventType.SwitchInputMethod, "notify")

local now = fcitx.currentInputMethod() == "flypy" and 1 or 0
h = io.popen("echo 'F;" .. now .. "' >> /tmp/dwm.fifo")
function notify()
    local z = fcitx.currentInputMethod() == "flypy" and 1 or 0
    if z ~= now then
        h = io.popen("echo 'F;" .. z .. "' >> /tmp/dwm.fifo")
        now = z
    end
end
