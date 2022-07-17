#!/bin/sh


# ⎜   ↳ HID 256c:006e stylus                    	id=23	[slave  pointer  (2)]
# ⎜   ↳ HID 256c:006e Pad pad                   	id=24	[slave  pointer  (2)]
# ⎜   ↳ HID 256c:006e Touch Strip pad           	id=25	[slave  pointer  (2)]
PAD="HID 256c:006e Pad pad"
STYLUS="HID 256c:006e stylus"
STRIP="HID 256c:006e Touch Strip pad"

# small delay to wait for all devices to be registered when called from udev rule
sleep 2

xsetwacom set "$STYLUS" MapToOutput HDMI-A-0
xsetwacom set "$STRIP" Button 1 "3"

xsetwacom set "$PAD" "Button" "1" "key ctrl z" # Button 5
xsetwacom set "$PAD" "Button" "2" "key ctrl y" # Button 6
xsetwacom set "$PAD" "Button" "3" "key ctrl lshift r"
# Unsupported buttons
# xsetwacom set "$PAD" "Button" "4" "button +1"
# xsetwacom set "$PAD" "Button" "5" "button +1"
# xsetwacom set "$PAD" "Button" "6" "button +1"
# xsetwacom set "$PAD" "Button" "7" "button +1"
xsetwacom set "$PAD" "Button" "8" "key ctrl lshift g" # Button 4
xsetwacom set "$PAD" "Button" "9" "key ctrl lshift p"
xsetwacom set "$PAD" "Button" "10" "key ctrl lshift e"
xsetwacom set "$PAD" "Button" "11" "key ctrl lshift a" # Button 7
xsetwacom set "$PAD" "Button" "12" "" # Button 8
xsetwacom set "$PAD" "Button" "13" "" # Button 9
xsetwacom set "$PAD" "Button" "14" "" # Button 10
xsetwacom set "$PAD" "Button" "15" "" # Button 11
xsetwacom set "$PAD" "Button" "16" "" # Button 12

# what is this button?
xsetwacom set "$PAD" "Button" "17" "button" # Button 13

notify-send --icon /usr/share/icons/gnome/256x256/devices/input-tablet.png Touchpad 'Touchpad configured!'
