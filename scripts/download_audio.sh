#!/bin/sh
temp="/home/goodman/AX/venv/bot/temp/"
name=$(yt-dlp --output "%(title)s" -x --print filename $1)
yt-dlp --output "${temp}%(title)s" -x $1 &> /dev/null
newname=$(echo -n $name | tr ' ' '_')
name=$(ls $temp | grep "$(echo $name | awk -F'.' '{print $1}')" )
ffmpeg -i "${temp}${name}" -ab 320k "${temp}${newname}.mp3" &> /dev/null
rm "${temp}${name}"

echo -n "${temp}${newname}.mp3"
