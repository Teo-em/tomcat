import discord

from src.constant import PATH_DATA
from src.constant import PATH_IMG
from src.constant import PATH_SCRIPT
from src.constant import PATH_SRC
from src.constant import PATH_TEMP
from src.constant import TOKEN

import locale
import datetime
import os.path
import re
import requests
import random
import subprocess
from urllib.request import urlopen



def run_command(command):
    return subprocess.run(command.split(), capture_output=True, text=True, universal_newlines=True).stdout


def run_script(script, params=""):
    command = PATH_SCRIPT + script
    if params:
        command += " " + params
    return run_command(command)


def get_user(self, name):
    if name.startswith("<@"):
        user = self.get_user(int(name[2:-1]))
    else:
        user = discord.utils.get(self.get_all_members(), name=name)
    return user


async def get_audio(self, message):
    if len(message.content.split()) < 3:
        await message.channel.send("Error: No se pasó ningún link para descargar. Try **tom --help**.")
    address = message.content.split()[2]
    file = run_script("download_audio.sh", address)
    if file.startswith("Error"):
        await message.channel.send(file)
        return
    await message.channel.send(file=discord.File(file))
    run_command("rm " + file)
    return


async def get_avatar(self, message):
    user = get_user(self, message.content.split()[2])
    if user:
        url = user.avatar
        await message.channel.send(url)


async def cara_cruz(self, message):
    result = bool(random.getrandbits(1))
    if result:
        await message.channel.send("**CARA**", file=discord.File(PATH_IMG + "cara.png"))
    else:
         await message.channel.send("**CRUZ**", file=discord.File(PATH_IMG + "cruz.png"))



def cumple_add(self, message):
    content = message.content.split()
    guild_id = message.channel.guild.id
    content = " ".join(content[3:])
    numbers = re.split('\W+', content)
    correct_date = False
    date = datetime.datetime(1,1,1)
    try:
        date = datetime.datetime(int(numbers[2]),int(numbers[1]),int(numbers[0]))
        correct_date = True
    except ValueError:
        correct_date = False
    if not correct_date:
        return "No ingresaste una fecha válida."

    with open(PATH_DATA+"cumples.txt", 'a+') as file:
        file.seek(0)
        text = file.read()
        if str(guild_id)+" "+str(message.author.id) in text:
            return "Ya estabas registrado para este servidor."
        file.write(f"{guild_id} {message.author.id} 0 <{content}\n")
    return "Te registraste correctamente para la fecha: "+date.strftime("%d %B")


def cumple_delete(self, message): 
    content = message.content.split()
    guild_id = message.channel.guild.id
    content = " ".join(content[3:])
    exists = False
    with open(PATH_DATA+"cumples.txt", 'r+') as file:
        lines = file.readlines()
        result = ''
        for line in lines:
            if not str(message.author.id) in line:
                result += line
            else:
                exists = True
        if exists:
            file.seek(0)
            file.write(result)
            file.truncate()
    if exists:
        return "Se eliminó el recordatorio."
    else:
        return "No estabas registrado en el recordatorio."


async def check_cumple(self):
    if not os.path.isfile(PATH_DATA+"cumples.txt"):
        return
    with open(PATH_DATA+"cumples.txt", 'r+') as file:
        file.seek(0)
        lines = file.readlines()
        result = ''
        for line in lines:
            if line.split()[2] == "0":
                numbers = re.split('\W+', line.split('<')[1])
                date = datetime.datetime(int(numbers[2]),int(numbers[1]),int(numbers[0]))
                if datetime.datetime.now().month == date.month and datetime.datetime.now().day == date.day:
                    guild = self.get_guild(int(line.split()[0]))
                    for channel in guild.channels:
                        if channel.name == 'general' and channel.type.name == "text":
                            await channel.send("Hoy es el cumple de <@"+str(line.split()[1])+">")
                    result += f"{line.split()[0]} {line.split()[1]} 1 <{line.split('<')[1]}"
                else:
                    result += line
            else:
                numbers = re.split('\W+', line.split('<')[1])
                date = datetime.datetime(int(numbers[2]),int(numbers[1]),int(numbers[0]))
                if not (datetime.datetime.now().month == date.month and datetime.datetime.now().day == date.day):
                    result += f"{line.split()[0]} {line.split()[1]} 0 <{line.split('<')[1]}"
                    
        file.seek(0)
        file.write(result)



async def cumple(self, message):
    content = message.content.split()
    if len(content) == 2:
        #channel send help
        return
    guild_id = message.channel.guild.id
    if not guild_id:
        await message.channel.send("que hace flaco")
        return
    if content[2] == "add":
        await message.channel.send(cumple_add(self,message))
    elif content[2] == "delete":
        await message.channel.send(cumple_delete(self,message))
    return 


async def get_dolar(self, message):
    url = "https://dolarhoy.com/cotizaciondolarblue"
    page = urlopen(url)
    html = page.read().decode("utf-8")
	
    pattern = "<div class=\"value\">.*?</div>"
    matches = re.findall(pattern, html, re.IGNORECASE)
    title = re.sub("<.*?>", "", matches[1])
    result = "**Dólar blue:** "+ str(title)[:-3]
    await message.channel.send(result)


async def print_help(self, message):
    await message.channel.send(run_command("cat " + PATH_DATA + "help.txt"))


async def message_to(self, message):
    name = message.content.split(' ')[2]
    message_text = ' '.join(message.content.split()[3:])
    user = get_user(self, name)
    send = True
    response = ""
    if not message_text:
        response += "No puedo enviar un mensaje vacío. "
        send = False
    if not user:
        response += "No puedo encontrar al usuario **" + name + "**"
        send = False
    if send:
        await user.send(message_text)
        response = "**Mensaje enviado:** " + message_text + "\n**Usuario: **" + "<@"+str(user.id)+">"
    await message.author.send(response)
    return


async def teo_status(self, message):
#    run_script("teostatus.sh")
#    await message.channel.send(file=discord.File(PATH_TEMP + "img.png"))
    await message.channel.send(file=discord.File(PATH_IMG + "idk.png"))
    return


async def translate(self, message):
    text = ' '.join(message.content.split()[2:])
    text = "\""+text+"\""
    await message.channel.send(run_script("translate.sh", text))


async def raw_run(self, message):
    if message.author.id == 305483295833980938:
        command = ' '.join(message.content.split()[1:])
        response = run_command(command)
        if response:
            await message.channel.send(response)
        return


async def not_command(self, message):
    await message.channel.send("Usa **\"tom --help\"** para ver comandos y ejemplos.")





commands = {
    "tom -a": [get_audio],
    "tom --audio": [get_audio],
    "tom --avatar": [get_avatar],
    "tom -c": [cara_cruz],
    "tom --cara-o-cruz": [cara_cruz],
    "tom --cumple": [cumple],
    "tom -d": [get_dolar],
    "tom --dolar": [get_dolar],
    "tom -h": [print_help],
    "tom --help": [print_help],
    "tom -m": [message_to],
    "tom --mensaje": [message_to],
    "tom -q": [teo_status],
    "tom --que-hace-teo?": [teo_status],
    "tom -t": [translate],
    "tom --traducir": [translate],
    "exec": [raw_run],

    
# Old commands
    "que hace teo?": [not_command,teo_status],
    "cara o ceca": [not_command, cara_cruz],
    "cara o cruz": [not_command, cara_cruz],
    "avd": [not_command, get_dolar],
    "tvd": [not_command, get_dolar],
}


class TomCat(discord.Client):

    async def on_ready(self):
        print(f'A darle atomos! {self.user}')
        await check_cumple(self)

    async def on_message(self, message):
        if message.author == self.user:
            return

        for prefix, functions in commands.items():
            if message.content.lower().startswith(prefix):
                for function in functions:
                    await function(self, message)
                break



intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

client = TomCat(intents=intents)
client.run(TOKEN)
