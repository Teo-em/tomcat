#!/bin/sh

if [ $# -eq 0 ]
then
    echo "Error: Mal uso del comando -a, --audio.\nNo se pasó un link."
    exit 1
fi

temp="${HOME}/AX/venv/bots/tomcat/temp/"
name=$(yt-dlp --output "%(title)s" -x --print filename $1) 

if [ $? -ne 0 ]
then
    echo "Error: No se encontró un video para el 'link': ${1}"
    exit 2
fi

yt-dlp --output "${temp}%(title)s" -x $1 &> /dev/null
newname=$(echo -n $name | tr ' ' '_')
name=$(ls $temp | grep "$(echo $name | awk -F'.' '{print $1}')" )
ffmpeg -i "${temp}${name}" -ab 320k "${temp}${newname}.mp3" &> /dev/null
rm "${temp}${name}"

echo -n "${temp}${newname}.mp3"
