#!/bin/bash
temp="${HOME}/AX/venv/bot/temp/img.png"

if [ -e "$temp" ]; then
	rm $temp
fi
scrot -p $temp
notify-send "funado"
