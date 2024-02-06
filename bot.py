import discord

from src.constant import PATH_DATA
from src.constant import PATH_IMG
from src.constant import PATH_SCRIPT
from src.constant import PATH_SRC
from src.constant import PATH_TEMP
from src.constant import TOKEN

import re
import random
import subprocess
from urllib.request import urlopen



def run_command(command):
    return subprocess.run(command.split(), stdout=subprocess.PIPE).stdout.decode()


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
    address = message.content.split()[2]
    file = run_script("download_audio.sh", address)
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


async def frieren(self, message):
    pass
    

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
    run_script("teostatus.sh")
    await message.channel.send(file=discord.File(PATH_TEMP + "img.png"))
#    await message.channel.send(file=discord.File(PATH_IMG + "idk.png"))
    return


async def raw_run(self, message):
    if message.author.name == 'teo.730':
        command = ' '.join(message.content.split()[1:])
        response = run_command(command)
        if response:
            await message.author.send(response)
        return


async def not_command(self, message):
    await message.channel.send("El comando está **obsoleto**, consulta la documentación \"tom --help\" para aprender a usar correctamente el bot.")



commands = {
    "tom -a": [get_audio],
    "tom --audio": [get_audio],
    "tom --avatar": [get_avatar],
    "tom -c": [cara_cruz],
    "tom --cara-o-cruz": [cara_cruz],
    "tom -d": [get_dolar],
    "tom --dolar": [get_dolar],
    "tom -f": [frieren],
    "tom --frieren": [frieren],
    "tom -h": [print_help],
    "tom --help": [print_help],
    "tom -m": [message_to],
    "tom --mensaje": [message_to],
    "tom -q": [teo_status],
    "tom --que-hace-teo?": [teo_status],
#    "tom -r": responde,
#    "tom --responde": responde,
    "exec": [raw_run],
    "que hace teo?": [not_command,teo_status],
    "cara o ceca": [not_command, cara_cruz],
    "cara o cruz": [not_command, cara_cruz],
    "avd": [not_command, get_dolar],
    "tvd": [not_command, get_dolar],
}

class TomCat(discord.Client):

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        for prefix, functions in commands.items():
            if message.content.lower().startswith(prefix):
                for function in functions:
                    print(message.content)
                    await function(self, message)
                break

    async def on_voice_state_update(self, user, before, after):
        guild = self.get_guild(289528008027406337)
        if user.id == 496099123695583253 and (before.channel == None or before.channel != after.channel) and after.self_mute and after.channel != None:
            print("deleted juampa")
            await user.move_to(discord.utils.get(guild.voice_channels, name='AFK'))



intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

client = TomCat(intents=intents)
client.run(TOKEN)
