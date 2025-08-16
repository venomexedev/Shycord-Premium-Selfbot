import os
os.system("pip install --upgrade pip")
import json
import string
import discord, aiohttp
from discord.ext import commands, tasks
import requests
from colorama import Fore, Style
import qrcode
import asyncio
import requests
import sys
import random
from flask import Flask
from threading import Thread
import threading
import subprocess
import requests
import time
from discord import Color, Embed
import colorama
import urllib.parse
import urllib.request
import re
from pystyle import Center, Colorate, Colors
from io import BytesIO
import webbrowser
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from discord import Member
import openai
from dateutil import parser
from collections import deque
from googletrans import Translator, LANGUAGES
import image
import re

colorama.init()

intents = discord.Intents.all()

category_messages = {}
active_tasks = {}
sent_channels = set()

def load_config(config_file_path):
    with open(config_file_path, 'r') as config_file:
        config = json.load(config_file)
    return config


if __name__ == "__main__":
    config_file_path = "config.json"
    config = load_config(config_file_path)

#=== Welcome ===
prefix = config.get('prefix')
token = config.get('token')
api_key = config.get('apikey')
ltc_priv_key = config.get('ltckey')
ltc_addy = config.get("LTC_ADDY")
I2C_Rate = config.get("I2C_Rate")
C2I_Rate = config.get("C2I_Rate")
LTC = config.get("LTC_ADDY")
Upi = config.get("Upi")
upi_id = config.get("Upi")
Qr = config.get("Qr")
User_Id = config.get("User_Id")
SERVER_Link = config.get("SERVER_Link")
#===================================

savvy = commands.Bot(description='SELFBOT CREATED BY venom.json',
                           command_prefix=prefix,
                           self_bot=True,
                           intents=intents)
status_task = None

savvy.remove_command('help')

savvy.whitelisted_users = {}

savvy.antiraid = False

red = "\033[91m"
yellow = "\033[93m"
green = "\033[92m"
blue = "\033[36m"
pretty = "\033[95m"
magenta = "\033[35m"
lightblue = "\033[94m"
cyan = "\033[96m"
gray = "\033[37m"
reset = "\033[0m"
pink = "\033[95m"
dark_green = "\033[92m"
yellow_bg = "\033[43m"
clear_line = "\033[K"

@savvy.event
async def on_ready():
      print(
        Center.XCenter(
            Colorate.Vertical(
                Colors.green_to_yellow,
            f"""[=]-------------------------------------------------------------------------------------------[=]
[  SHYCORD  VERSION  1  |  MADED  BY  :-  venom.json  |  LOGINED  AS  :-  {savvy.user.name}  ]
[=]-------------------------------------------------------------------------------------------[=]
""",
                1,
            )
        )
    )


def load_config(config_file_path):
    with open(config_file_path, 'r') as config_file:
        config = json.load(config_file)
    return config


if __name__ == "__main__":
    config_file_path = "config.json"
    config = load_config(config_file_path)

#=== Welcome ===
prefix = config.get('prefix')
token = config.get('token')
api_key = config.get('apikey')
ltc_priv_key = config.get('ltckey')
ltc_addy = config.get("LTC_ADDY")
I2C_Rate = config.get("I2C_Rate")
C2I_Rate = config.get("C2I_Rate")
LTC = config.get("LTC_ADDY")
Upi = config.get("Upi")
Upi2 = config.get("Upi2")
upi_id = config.get("Upi")
Qr = config.get("Qr")
Qr2 = config.get("Qr2")
User_Id = config.get("User_Id")
SERVER_Link = config.get("SERVER_Link")
cg_id = config.get("slot_category_id")
LTC2 = config.get("LTC_ADDY2")
BID = config.get("BINANCE_ID")
#===================================

def get_time_rn():
    date = datetime.now()
    hour = date.hour
    minute = date.minute
    second = date.second
    timee = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
    return date

time_rn = get_time_rn()

@savvy.event
async def on_message(message):
    if message.author.bot:
        return

    # Auto-response handling
    with open('ar.json', 'r') as file:
        auto_responses = json.load(file)

    if message.content in auto_responses:
        await message.channel.send(auto_responses[message.content])

    await savvy.process_commands(message)
    
    # Auto-message handling
def load_auto_messages():
    try:
        with open("am.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_auto_messages(data):
    with open("am.json", "w") as f:
        json.dump(data, f, indent=4)
        
#Discord Status Changer Class
class DiscordStatusChanger:
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Authorization": token,
            "User-Agent": "DiscordBot (https://discordapp.com, v1.0)",
            "Content-Type": "application/json",
            "Accept": "*/*"
        }

    def change_status(self, status, message, emoji_name, emoji_id):
        jsonData = {
            "status": status,
            "custom_status": {
                "text": message,
                "emoji_name": emoji_name,
                "emoji_id": emoji_id,
            }
        }
        r = requests.patch("https://discord.com/api/v9/users/@me/settings", headers=self.headers, json=jsonData)
        return r.status_code


class StatusRotator(commands.Cog):
    def __init__(self, savvy, token):
        self.bot = savvy
        self.token = config.get('token')
        self.discord_status_changer = DiscordStatusChanger(self.token)
        self.is_rotating = False
        self.statuses = []  # List to store statuses

    @commands.command()
    async def rotate(self, ctx, *, statuses: str):
        if not self.is_rotating:
            self.is_rotating = True
            self.statuses = [s.strip() for s in statuses.split('/')]  # Split statuses by '/'
            if not self.statuses:
                await ctx.send("No valid statuses provided. Use the format: `.start_rotation <emoji, status> / <emoji, status>`")
                return
            await ctx.send("**Starting status rotation...**")
            await self.run_rotation(ctx)
        else:
            await ctx.send("**Status rotation is already running.**")

    @commands.command()
    async def stop_rotate(self, ctx):
        if self.is_rotating:
            self.is_rotating = False
            await ctx.send("Stopping status rotation...")
        else:
            await ctx.send("Status rotation is not currently running.")

    async def run_rotation(self, ctx):
        while self.is_rotating:
            try:
                for status in self.statuses:
                    if not self.is_rotating:  # Exit if rotation stops
                        break

                    parts = status.split(',')
                    if len(parts) >= 2:
                        emoji_name = parts[0].strip()
                        status_text = parts[1].strip()
                        emoji_id = None

                        # Check if emoji is an ID
                        if emoji_name.isdigit():
                            emoji_id = emoji_name
                            emoji_name = ""

                        # Change the status
                        status_code = self.discord_status_changer.change_status("dnd", status_text, emoji_name, emoji_id)
                        if status_code == 200:
                            print(f"Changed to: {status_text}")
                        else:
                            print("Failed to change status.")
                        
                        # Wait before changing to the next status
                        await asyncio.sleep(10)
            except Exception as e:
                print(f"An error occurred: {e}")
                await asyncio.sleep(10)  # Retry after 10 seconds
                
TOKEN = config.get('token')
savvy.add_cog(StatusRotator(savvy, TOKEN))

class AFK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.afk_data = {}
        self.user_cooldowns = {}

    def save_afk_data(self):
        with open("afk.json", "w") as f:
            json.dump(self.afk_data, f)

    def load_afk_data(self):
        try:
            with open("afk.json", "r") as f:
                self.afk_data = json.load(f)
        except FileNotFoundError:
            self.afk_data = {}

    @commands.command()
    async def afk(self, ctx, *, reason="busy so don't ping"):
        user_id = str(ctx.author.id)
        self.afk_data[user_id] = reason
        await ctx.send(f"🍷 **You are now AFK..**")
        self.save_afk_data()

    @commands.command()
    async def unafk(self, ctx):
        user_id = str(ctx.author.id)
        if user_id in self.afk_data:
            del self.afk_data[user_id]
            await ctx.send(f"🍷 **You are no longer AFK**")
            self.save_afk_data()
        else:
            await ctx.send(f"{ctx.author.mention}, 🍷 **you are not AFK**")
            
    async def ignore_user_for_duration(self, user_id, duration):
        self.user_cooldowns[user_id] = True
        await asyncio.sleep(duration)
        del self.user_cooldowns[user_id]            

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
            
        if isinstance(message.channel, discord.DMChannel):
            pass  
                    
        for user_id, reason in self.afk_data.items():
            if f"<@{user_id}>" in message.content:
                if message.author.id not in self.user_cooldowns:
                    await message.channel.send(f"{message.author.mention}, **I am afk rn**., **{reason}**")
                    await self.ignore_user_for_duration(message.author.id, 30)
                break
            elif message.reference and message.reference.cached_message:
                replied_to_user = message.reference.cached_message.author
                if str(replied_to_user.id) == user_id:
                    if message.author.id not in self.user_cooldowns:
                        await message.channel.send(f"{message.author.mention}, **I am afk rn**., **{reason}**")
                        await self.ignore_user_for_duration(message.author.id, 30)

savvy.add_cog(AFK(savvy))

#task
tasks_dict = {}

@savvy.command()
async def help(ctx, helpcategory="none"):
    await ctx.message.delete()  
    helpcategory = helpcategory.lower().replace("[", "").replace("]", "")
    if helpcategory == "none":
        description = """# 👑 __SHYCORD V4__ 👑
🎊 **ALL IN ONE BEST AND SAFE SELFBOT**

> **📗 HELP MODULES**
> 
> 🥤 **GENERAL SECTION** :- `.help gnrl`
> 🥂 **CONFIG SECTION** :- `.help config`
> 💸 **UPI SECTION** :- `.help upi`
> 🪙 **CRYPTO SECTION** :- `.help crypto`
> 🍭 **MESSAGE SECTION** :- `.help msg`
> 🍷 **STATUS SECTION** :- `.help status`
> 🍩 **CALCULATE SECTION** :- `.help calc`
> 🍸 **AUTO MSG SECTION** :- `.help auto`
> 💳 **VOUCH SECTION** :- `.help vouch`
> 🛡️ **MODERATION SECTION** :- `.help mod`
> 🧃 **AFK SECTION** :- `.help afk`
> 📕 **CHECKER SECTION** :- `.help checker`
> 🏞️ **IMAGE SECTION** :- `.help image`
> 🗒️ **FUN SECTION** :- `.help fun`
> 🍿 **VC SECTION** :- `.help vc`
> 📔 **USER SECTION** :- `.help user`
> 🍑 **NSFW SECTION** :- `.help nsfw`

> 🍬 **SET PREFIX** :- `.prefix <prefix>`
> 🎗️ **DEVELOPER** :- `venom.json`
"""

    elif "config" in helpcategory:
        description = """👑 **Config Section** 👑

🥂 **Set Upi** :- `.setupi <upi_id>`
🥂 **Set Upi 2** :- `.setupi2 <upi_id2>`
🥂 **Set Qr** :- `.setqr <qr_code>`
🥂 **Set Qr 2** :- `.setqr2 <qr_code2>`
🥂 **Set Server Link** :- `.setsrvlink <link>`
🥂 **Set User Id** :- `.setuserid <id>`
🥂 **Set Ltc Addy** :- `.setaddy <addy>`
🥂 **Set Ltc Addy 2** :- `.setaddy2 <addy2>`
🥂 **Set Binance Id** :- `.setbinid <id>`
🥂 **Set Ltc Key** :- `.setltckey <ltc_key>`"""

    elif "gnrl" in helpcategory:
        description = """👑 **General Section** 👑

🥤 **Show Allcmds** :- `.allcmds`
🥤 **Srv Clone** :- `.csrv <copy id> <target id>`
🥤 **Restart Bot** :- `.restart`
🥤 **Server Info** :- `.srvinfo`
🥤 **Selfbot Info** :- `.selfbot`
🥤 **User Info** :- `.user_info <@user>`
🥤 **Yt Search** :- `.yt <title-search>`
🥤 **Abuse** :- `.abuse <user>`"""

    elif "crypto" in helpcategory:
        description = """👑 **Crypto Section** 👑

💰 **Send Ltc** :- `.send <addy> <amount>`
💰 **Check Balance** :- `.bal <addy>`
💰 **Check Mybal** :- `.mybal`
💰 **Second Check Mybal** :- `.mybal2`
💰 **Ltc Addy** :- `.addy`
💰 **Second Ltc Addy** :- `.addy2`
💰 **Ltc Custom Qr** :- `.ltcqr <addy> <usd_amt>`
💰 **Ltc Price In Usd** :- `.ltc`
💰 **Sol Price In Usd** :- `.sol`
💰 **Btc Price In Usd** :- `.btc`
💰 **Usdt Price In Usd** :- `.usdt`
💰 **Xrp Price In Usd** :- `.xrp`
"""

    elif "msg" in helpcategory:
        description = """👑 **Message Section** 👑

🍭 **Spam Msg** :- `.spam <amount> <msg>`
🍭 **Clear Msg** :- `.clear <amount>`
🍭 **Direct Msg** :- `.dm <@user> <msg>`
🍭 **Send Msg Ticket Create** :- `.sc <cg-id> <msg>`
🍭 **Remove Msg Ticket Create** :- `.stopsc <cg-id>`
🍭 **translate Msg** :- `.translate <from> <to> <msg>`
🍭 **Dm All In Server** :- `.dmall <msg>`
🍭 **Mass Dm Friends** :- `.massdmfrnds <msg>`"""

    elif "status" in helpcategory:
        description = """👑 **Rotation Section** 👑

🍷 **Status Rotator** :- `.rotate <emoji id , msg> / <emoji id , msg> / <repeat again>`
🍷 **Stop Rotator** :- `.stop_rotate`
🍷 **Stream Status** :- `.stream <title>`
🍷 **Playing Status** :- `.play <title>`
🍷 **Watching Status** :- `.play <title>`
🍷 **Listening Status** :- `.listen <title>`
🍷 **Remove Status** :- `.stopactivity`"""

    elif "calc" in helpcategory:
        description = """👑 **Calculate Section** 👑

🍩 **Calculate** :- `.math <equation>`
🍩 **Inr To Crypto** :- `.i2c <inr amount>`
🍩 **Crypto To Inr** :- `.c2i <crypto amount>`
🍩 **Ltc To Usd** :- `.l2u <ltc amount>`
🍩 **Usd To Ltc** :- `.u2l <usd amount>`
🍩 **Euro To Usd** :- `.e2u <euro amount>`
🍩 **Usd To Euro** :- `.u2e <usd amount>`"""

    elif "auto" in helpcategory:
        description = """👑 **Auto Sender Section** 👑

🍸 **AutoRespond** :- `.ar <trigger>, <response>`
🍸 **Remove Respond** :- `.removear <triger>`
🍸 **AutoRespond List** :- `.ar_list`
🍸 **AutoMsg** :- `.am <time> <chnl_id> <msg>`
🍸 **Stop AutoMsg** :- `.am_stop <chnl_id>`
🍸 **AutoMsg List** :- `.am_list`"""

    elif "afk" in helpcategory:
        description = """👑 **Afk Section** 👑

🧃 **Afk** :- `.afk <reason>`
🧃 **Remove Afk** :- `.unafk`"""

    elif "checker" in helpcategory:
        description = """👑 **Checker Section** 👑

📕 **Check Promo** :- `.checkpromo <promo>`
📕 **Check Token** :- `.checktoken <token>`"""

    elif "image" in helpcategory:
        description = """👑 **Image Section** 👑

🏞️ **Get Avatar** :- `.avatar <@user>`
🏞️ **Get Icon Of Server** :- `.icon`
🏞️ **Get Image** :- `.get_image <query>`"""

    elif "upi" in helpcategory:
        description = """👑 **Upi Section** 👑

💸 **Upi Id** :- `.upi`
💸 **Second Upi Id** :- `.upi2`
💸 **Qr Code** :- `.qr`
💸 **Second Qr Code** :- `.qr2`
💸 **Custom Qr** :- `.cqr <amt> <note>`"""

    elif "mod" in helpcategory:
        description = """👑 **Moderation Section** 👑

🛡️ **Ban** :- `.ban <user>`
🛡️ **Kick** :- `.kick <user>`
🛡️ **Ban Id** :- `.banid <userid>`
🛡️ **Unban Id** :- `.unban <userid>`
🛡️ **Nuke Channel** :- `.nuke`
🛡️ **Nuke Server** :- `.nukesrv`
🛡️ **Hide** :- `.hide`
🛡️ **Unhide** :- `.unhide`
🛡️ **Create Channel** :- `.chnl <chnl-name>`
🛡️ **Create Role** :- `.role <role-name>`"""

    elif "fun" in helpcategory:
        description = """👑 **Fun Section** 👑

🗒️ **Rizz** :- `.rizz <user>`
🗒️ **Gen Joke** :- `.joke`
🗒️ **Gen Meme** :- `.meme`
🗒️ **Name** :- `.name <name>`
🗒️ **Fake Nitro** :- `.nitro`
🗒️ **Impersonate Msg** :- `.impresonate <user>`
🗒️ **Check Profile** :- `.checkprofile <user>`
🗒️ **Blurpify** :- `.blurpify <user>`
🗒️ **Deepfry** :- `.deepfry <user>`
🗒️ **Fake Captcha** :- `.captcha <user>`
🗒️ **Threat** :- `.threat <user>`
🗒️ **Fake Iphone Gift** :- `.iphone <user>`
🗒️ **Fake Shipping** :- `.ship <user>`"""

    elif "vc" in helpcategory:
        description = """👑 **Vc Section** 👑

🍿 **Vc Kick** :- `.vckick <user>`
🍿 **Vc Move All** :- `.vcmoveall <from chnl id> <to chnl id>`
🍿 **Vc Mute** :- `.vcmute <user>`
🍿 **Vc Unmute** :- `..vcunmute <user>`
🍿 **Vc Deafen** :- `.vcdeafen <user>`
🍿 **Vc Undeafen** :- `.vcundeafen <user>`
🍿 **Vc Move** :- `.vcmove <user> <channelid>`
🍿 **Vc Join** :- `.vcjoin <channelid>`
🍿 **Vc leave** :- `.vcleave`
🍿 **Vc Set Limit** :- `.vclimit <limit> <channel-id>`"""

    elif "user" in helpcategory:
        description = """👑 **User Section** 👑

📔 **Leave All groups** :- `.leaveallgroups`
📔 **Delete Friends** :- `.delallfriends`
📔 **Close All Dms** :- `.closealldms`
📔 **Transcript** :- `.transcript <amt of msg>`"""

    elif "nsfw" in helpcategory:
        description = """👑 **User Section** 👑

🍑 **Hass** :- `.hass`
🍑 **Ass** :- `.ass`
🍑 **Boobs** :- `.boobs`
🍑 **lewdneko** :- `.lewdneko`
🍑 **Blowjob** :- `.blowjob`
🍑 **Hentai** :- `.hentai`"""

    elif "vouch" in helpcategory:
        description = """👑 **Vouch Section** 👑

💳 **Vouch** :- `.vouch <product for much>`
💳 **Exchange Vouch** :- `.exch <This To This>`
💳 **I2c Vouch** :- `.i2cvouch <inr amt> <ltc amt>`
💳 **C2i Vouch** :- `..c2ivouch <ltc amt> <inr amt>`"""
    await ctx.send(description)


@savvy.command()
async def upi(ctx):
    message = (f"💸 💸 💸 💸 💸 **UPI** 💸 💸 💸 💸 💸")
    message2 = (f"{Upi}")
    message3 = (f"**MUST SEND SCREENSHOT AFTER PAYMENT**")
    await ctx.send(message)
    await ctx.send(message2)
    await ctx.send(message3)
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}UPI SENT SUCCESFULLY✅ ")
    await ctx.message.delete()

@savvy.command()
async def upi2(ctx):
    message = (f"💸 💸 💸 💸 💸 **UPI** 💸 💸 💸 💸 💸")
    message2 = (f"{Upi2}")
    message3 = (f"**MUST SEND SCREENSHOT AFTER PAYMENT**")
    await ctx.send(message)
    await ctx.send(message2)
    await ctx.send(message3)
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}UPI SENT SUCCESFULLY✅ ")
    await ctx.message.delete()
    
@savvy.command()
async def qr(ctx):
    message = (f"{Qr}")
    message2 = (f"**MUST SEND SCREENSHOT AFTER PAYMENT**")
    await ctx.send(message)
    await ctx.send(message2)
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}QR SENT SUCCESFULLY✅ ")
    await ctx.message.delete()

@savvy.command()
async def qr2(ctx):
    message = (f"{Qr2}")
    message2 = (f"**MUST SEND SCREENSHOT AFTER PAYMENT**")
    await ctx.send(message)
    await ctx.send(message2)
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}QR SENT SUCCESFULLY✅ ")
    await ctx.message.delete()
    
@savvy.command()
async def addy(ctx):
    message = (f"🪙 🪙 🪙 🪙 **LTC ADDY** 🪙 🪙 🪙 🪙 ")
    message2 = (f"{LTC}")
    message3 = (f"**MUST SEND SCREENSHOT AND BLOCKCHAIN AFTER PAYMENT**")
    await ctx.send(message)
    await ctx.send(message2)
    await ctx.send(message3)
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}ADDY SENT SUCCESFULLY✅ ")
    await ctx.message.delete()

@savvy.command()
async def addy2(ctx):
    message = (f"🪙 🪙 🪙 **BINANCE LTC ADDY** 🪙 🪙 🪙 ")
    message2 = (f"{LTC2}")
    message3 = (f"**MUST SEND SCREENSHOT AND BLOCKCHAIN AFTER PAYMENT**")
    await ctx.send(message)
    await ctx.send(message2)
    await ctx.send(message3)
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}BINANCE ADDY SENT SUCCESFULLY✅ ")
    await ctx.message.delete()

@savvy.command()
async def bid(ctx):
    message = (f"<:crypto:1317032618222682142> **BINANCE ID** <:crypto:1317032618222682142>")
    message2 = (f"{BID}")
    message3 = (f"**MUST SEND SCREENSHOT AFTER PAYMENT**")
    await ctx.send(message)
    await ctx.send(message2)
    await ctx.send(message3)
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}BINANCE ID SENT SUCCESFULLY✅ ")
    await ctx.message.delete()
    
# MATHS
api_endpoint = 'https://api.mathjs.org/v4/'
@savvy.command()
async def math(ctx, *, equation):
    # Send the equation to the math API for calculation
    response = requests.get(api_endpoint, params={'expr': equation})

    if response.status_code == 200:
        result = response.text
        await ctx.send(f'🍷 **EQUATION**: `{equation}`\n\n🍷 **Result**: `{result}`')
        await ctx.message.delete()
    else:
        await ctx.reply('🍷 **Failed**')
        
@savvy.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def i2c(ctx, amount: str):
    amount = float(amount.replace('₹', ''))
    inr_amount = amount / I2C_Rate
    await ctx.send(f"🍷 **EQUATION**: `{amount}/{I2C_Rate}`\n\n🍷 **Result** : `${inr_amount:.2f}`")
    await ctx.message.delete()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}I2C DONE ✅ ")
    
@savvy.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def c2i(ctx, amount: str):
    amount = float(amount.replace('$', ''))
    usd_amount = amount * C2I_Rate
    await ctx.send(f"🍷 **EQUATION**: `{amount}*{C2I_Rate}`\n\n🍷 **Result** : `₹{usd_amount:.2f}`")
    await ctx.message.delete()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}C2I DONE ✅ ")
    
spamming_flag = True
# SPAM 
@savvy.command()
async def spam(ctx, times: int, *, message):
    for _ in range(times):
        await ctx.send(message)
        await asyncio.sleep(0.1)      
    print("{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty} {Fore.GREEN}SPAMMING SUCCESFULLY✅ ")
    
@savvy.command(aliases=[])
async def mybal(ctx):
    response = requests.get(f'https://api.blockcypher.com/v1/ltc/main/addrs/{LTC}/balance')

    if response.status_code == 200:
        data = response.json()
        balance = data['balance'] / 10**8
        total_balance = data['total_received'] / 10**8
        unconfirmed_balance = data['unconfirmed_balance'] / 10**8
    else:
        await ctx.reply("🍷 `Failed`")
        return

    cg_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')

    if cg_response.status_code == 200:
        usd_price = cg_response.json()['litecoin']['usd']
    else:
        await ctx.reply("🍷 `Failed`")
        return

    usd_balance = balance * usd_price
    usd_total_balance = total_balance * usd_price
    usd_unconfirmed_balance = unconfirmed_balance * usd_price
    
    message = f"🪙 **ADDY**: `{LTC}` 🪙\n"
    message += f"🪙 **CURRENT LTC BALANCE** : `{usd_balance:.2f}$ USD` 🪙\n"
    message += f"🪙 **TOTAL LTC RECEIVED** : `{usd_total_balance:.2f}$ USD` 🪙\n"
    message += f"🪙 **UNCONFIRMED LTC** : `{usd_unconfirmed_balance:.2f}$ USD` 🪙\n\n"

    await ctx.send(message)
    await ctx.message.delete()

@savvy.command(aliases=[])
async def mybal2(ctx):
    response = requests.get(f'https://api.blockcypher.com/v1/ltc/main/addrs/{LTC2}/balance')

    if response.status_code == 200:
        data = response.json()
        balance = data['balance'] / 10**8
        total_balance = data['total_received'] / 10**8
        unconfirmed_balance = data['unconfirmed_balance'] / 10**8
    else:
        await ctx.reply("🍷 `Failed`")
        return

    cg_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')

    if cg_response.status_code == 200:
        usd_price = cg_response.json()['litecoin']['usd']
    else:
        await ctx.reply("🍷 `Failed`")
        return

    usd_balance = balance * usd_price
    usd_total_balance = total_balance * usd_price
    usd_unconfirmed_balance = unconfirmed_balance * usd_price
    
    message = f"🪙 **ADDY**: `{LTC2}` 🪙\n"
    message += f"🪙 **CURRENT LTC BALANCE** : `{usd_balance:.2f}$ USD` 🪙\n"
    message += f"🪙 **TOTAL LTC RECEIVED** : `{usd_total_balance:.2f}$ USD` 🪙\n"
    message += f"🪙 **UNCONFIRMED LTC** : `{usd_unconfirmed_balance:.2f}$ USD` 🪙\n\n"

    await ctx.send(message)
    await ctx.message.delete()
    
@savvy.command(aliases=['ltcbal'])
async def bal(ctx, ltcaddress):
    response = requests.get(f'https://api.blockcypher.com/v1/ltc/main/addrs/{ltcaddress}/balance')

    if response.status_code == 200:
        data = response.json()
        balance = data['balance'] / 10**8
        total_balance = data['total_received'] / 10**8
        unconfirmed_balance = data['unconfirmed_balance'] / 10**8
    else:
        await ctx.reply("🍷 `Failed`")
        return

    cg_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')

    if cg_response.status_code == 200:
        usd_price = cg_response.json()['litecoin']['usd']
    else:
        await ctx.reply("🍷 `Failed`")
        return

    usd_balance = balance * usd_price
    usd_total_balance = total_balance * usd_price
    usd_unconfirmed_balance = unconfirmed_balance * usd_price
    
    message = f"🪙 **ADDY**: `{ltcaddress}` 🪙\n"
    message += f"🪙 **CURRENT LTC BALANCE** : `{usd_balance:.2f}$ USD` 🪙\n"
    message += f"🪙 **TOTAL LTC RECEIVED** : `{usd_total_balance:.2f}$ USD` 🪙\n"
    message += f"🪙 **UNCONFIRMED LTC** : `{usd_unconfirmed_balance:.2f}$ USD` 🪙\n\n"

    await ctx.send(message)
    await ctx.message.delete()
          
@savvy.command(aliases=["streaming"])
async def stream(ctx, *, message):
    stream = discord.Streaming(
        name=message,
        url="https://twitch.tv/https://Wallibear",
    )
    await savvy.change_presence(activity=stream)
    await ctx.send(f"🍷 **Stream Created** : `{message}`")
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}STREAM SUCCESFULLY CREATED✅ ")
    await ctx.message.delete()

@savvy.command(aliases=["playing"])
async def play(ctx, *, message):
    game = discord.Game(name=message)
    await savvy.change_presence(activity=game)
    await ctx.send(f"🍷 **Status For PLAYZ Created** : `{message}`")
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}PLAYING SUCCESFULLY CREATED✅ ")
    await ctx.message.delete()

@savvy.command(aliases=["watch"])
async def watching(ctx, *, message):
    await savvy.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name=message,
    ))
    await ctx.send(f"🍷 **Watching Created**: `{message}`")
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}WATCH SUCCESFULLY CREATED✅ ")
    await ctx.message.delete()

@savvy.command(aliases=["listen"])
async def listening(ctx, *, message):
    await savvy.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening,
        name=message,
    ))
    await ctx.reply(f"🍷 **Listening Created**: `{message}`")
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}STATUS SUCCESFULLY CREATED✅ ")
    await ctx.message.delete()

@savvy.command(aliases=[
    "stopstreaming", "stopstatus", "stoplistening", "stopplaying",
    "stopwatching"
])
async def stopactivity(ctx):
    await ctx.message.delete()
    await savvy.change_presence(activity=None, status=discord.Status.dnd)
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}!{gray}) {pretty}{Fore.RED}STREAM SUCCESFULLY STOPED⚠️ ")

@savvy.command()
async def exch(ctx, *, text):
    await ctx.message.delete()
    main = text
    await ctx.send(f'+rep {User_Id} {main}')
    await ctx.send(f'{SERVER_Link}')
    await ctx.send(f'**PLEASE VOUCH ME HERE**')
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} EXCH VOUCH✅ ")

@savvy.command()
async def vouch(ctx, *, text):
    await ctx.message.delete()
    main = text
    await ctx.send(f'+rep {User_Id} {main}')
    await ctx.send(f'{SERVER_Link}')
    await ctx.send(f'**PLEASE VOUCH ME HERE**')
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} VOUCH SENT✅ ")

@savvy.command()
async def i2cvouch(ctx, inr, inr2):
    await ctx.message.delete()
    main = inr
    main2 = inr2
    await ctx.send(f'+rep {User_Id} {main} UPI TO {main2} LTC ')
    await ctx.send(f'{SERVER_Link}')
    await ctx.send(f'**PLEASE VOUCH ME HERE**')
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} I2C VOUCH SENT✅ ")

@savvy.command()
async def c2ivouch(ctx, inr, inr2):
    await ctx.message.delete()
    main = inr
    main2 = inr2
    await ctx.send(f'+rep {User_Id} {main} LTC TO {main2} UPI ')
    await ctx.send(f'{SERVER_Link}')
    await ctx.send(f'**PLEASE VOUCH ME HERE**')
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} C2I VOUCH SENT✅ ")
    
@savvy.command(aliases=['cltc'])
async def ltc(ctx):
    url = 'https://api.coingecko.com/api/v3/coins/litecoin'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        price = data['market_data']['current_price']['usd']
        await ctx.send(f"🍷 **The Price Of Ltc Is :** `{price:.2f}`")
        await ctx.message.delete()
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} LTC PRICE SENT✅ ")
    else:
        await ctx.send("**🍷 Failed To Fetch**")

@savvy.command(aliases=['csol'])
async def sol(ctx):
    url = 'https://api.coingecko.com/api/v3/coins/solana'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        price = data['market_data']['current_price']['usd']
        await ctx.send(f"🍷 **The Price Of Sol Is :** `{price:.2f}`")
        await ctx.message.delete()
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} SOL PRICE SENT✅ ")
    else:
        await ctx.send("**🍷 Failed To Fetch**")

@savvy.command(aliases=['cusdt'])
async def usdt(ctx):
    url = 'https://api.coingecko.com/api/v3/coins/tether'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        price = data['market_data']['current_price']['usd']
        await ctx.send(f"🍷 **The Price Of Usdt Is :** `{price:.2f}`")
        await ctx.message.delete()
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} USDT PRICE SENT✅ ")
    else:
        await ctx.send("**🍷 Failed To Fetch**")

@savvy.command(aliases=['cbtc'])
async def btc(ctx):
    url = 'https://api.coingecko.com/api/v3/coins/bitcoin'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        price = data['market_data']['current_price']['usd']
        await ctx.send(f"🍷 **The Price Of Btc Is :** `{price:.2f}`")
        await ctx.message.delete()
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} BTC PRICE SENT✅ ")
    else:
        await ctx.send("**🍷 Failed To Fetch**")

@savvy.command(aliases=['cxrp'])
async def xrp(ctx):
    url = 'https://api.coingecko.com/api/v3/coins/ripple'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        price = data['market_data']['current_price']['usd']
        await ctx.send(f"🍷 **The Price Of Xrp Is :** `{price:.2f}`")
        await ctx.message.delete()
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} XRP PRICE SENT✅ ")
    else:
        await ctx.send("**🍷 Failed To Fetch**")
        
@savvy.command()
async def ar(ctx, *, trigger_and_response: str):
    # Split the trigger and response using a comma (",")
    trigger, response = map(str.strip, trigger_and_response.split(','))

    with open('ar.json', 'r') as file:
        data = json.load(file)

    data[trigger] = response

    with open('ar.json', 'w') as file:
        json.dump(data, file, indent=4)

    await ctx.send(f'🍷 **Auto Response Has Added.. !** **{trigger}** - **{response}**')
    await ctx.message.delete()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} AUTO RESPOND ADDED✅ ")



@savvy.command()
async def removear(ctx, trigger: str):
    with open('ar.json', 'r') as file:
        data = json.load(file)

    if trigger in data:
        del data[trigger]

        with open('ar.json', 'w') as file:
            json.dump(data, file, indent=4)

        await ctx.send(f'🍷 **Auto Response Has Removed** **{trigger}**')
        await ctx.message.delete()
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} AUTO RESPOND REMOVE✅ ")
    else:
        await ctx.send(f'🍷 **Auto Response Not Found** **{trigger}**')
        
@savvy.command()
async def ar_list(ctx):
    with open ("ar.json" , "r") as f:
        data = f.read()
    await ctx.send(data)
    await ctx.message.delete()
    print("[+] ar_list Command Used")

@savvy.command()
async def am_list(ctx):
    with open ("am.json" , "r") as f:
        data = f.read()
    await ctx.send(data)
    await ctx.message.delete()
    print("[+] am_list Command Used")

@savvy.command()
async def csrv(ctx, source_guild_id: int, target_guild_id: int):
    source_guild = savvy.get_guild(source_guild_id)
    target_guild = savvy.get_guild(target_guild_id)

    if not source_guild or not target_guild:
        await ctx.send("🍷 **Guild Not Found**")
        return

    # Delete all channels in the target guild
    for channel in target_guild.channels:
        try:
            await channel.delete()
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} CHANNEL {channel.name} HAS BEEN DELETED ON THE TARGET GUILD")
            await asyncio.sleep(2)
        except Exception as e:
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}!{gray}) {pretty}{Fore.RED} ERROR DELETING CHANNEL {channel.name}: {e}")

    # Delete all roles in the target guild except for roles named "here" and "@everyone"
    for role in target_guild.roles:
        if role.name not in ["here", "@everyone"]:
            try:
                await role.delete()
                print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} ROLE {role.name} HAS BEEN DELETED ON THE TARGET GUILD")
                await asyncio.sleep(2)
            except Exception as e:
                print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}!{gray}) {pretty}{Fore.RED} ERROR DELETING ROLE {role.name}: {e}")

    # Clone roles from source to target
    roles = sorted(source_guild.roles, key=lambda role: role.position)

    for role in roles:
        try:
            new_role = await target_guild.create_role(name=role.name, permissions=role.permissions, color=role.color, hoist=role.hoist, mentionable=role.mentionable)
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} {role.name} HAS BEEN CREATED ON THE TARGET GUILD")
            await asyncio.sleep(2)

            # Update role permissions after creating the role
            for perm, value in role.permissions:
                await new_role.edit_permissions(target_guild.default_role, **{perm: value})
        except Exception as e:
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}!{gray}) {pretty}{Fore.RED} ERROR CREATING ROLE {role.name}: {e}")

    # Clone channels from source to target
    text_channels = sorted(source_guild.text_channels, key=lambda channel: channel.position)
    voice_channels = sorted(source_guild.voice_channels, key=lambda channel: channel.position)
    category_mapping = {}  # to store mapping between source and target categories

    for channel in text_channels + voice_channels:
        try:
            if channel.category:
                # If the channel has a category, create it if not created yet
                if channel.category.id not in category_mapping:
                    category_perms = channel.category.overwrites
                    new_category = await target_guild.create_category_channel(name=channel.category.name, overwrites=category_perms)
                    category_mapping[channel.category.id] = new_category

                # Create the channel within the category
                if isinstance(channel, discord.TextChannel):
                    new_channel = await new_category.create_text_channel(name=channel.name)
                elif isinstance(channel, discord.VoiceChannel):
                    # Check if the voice channel already exists in the category
                    existing_channels = [c for c in new_category.channels if isinstance(c, discord.VoiceChannel) and c.name == channel.name]
                    if existing_channels:
                        new_channel = existing_channels[0]
                    else:
                        new_channel = await new_category.create_voice_channel(name=channel.name)

                print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} CHANNEL {channel.name} HAS BEEN CREATED ON THE TARGET GUILD")

                # Update channel permissions after creating the channel
                for overwrite in channel.overwrites:
                    if isinstance(overwrite.target, discord.Role):
                        target_role = target_guild.get_role(overwrite.target.id)
                        if target_role:
                            await new_channel.set_permissions(target_role, overwrite=discord.PermissionOverwrite(allow=overwrite.allow, deny=overwrite.deny))
                    elif isinstance(overwrite.target, discord.Member):
                        target_member = target_guild.get_member(overwrite.target.id)
                        if target_member:
                            await new_channel.set_permissions(target_member, overwrite=discord.PermissionOverwrite(allow=overwrite.allow, deny=overwrite.deny))

                await asyncio.sleep(2)  # Add delay here
            else:
                # Create channels without a category
                if isinstance(channel, discord.TextChannel):
                    new_channel = await target_guild.create_text_channel(name=channel.name)
                elif isinstance(channel, discord.VoiceChannel):
                    new_channel = await target_guild.create_voice_channel(name=channel.name)

                    # Update channel permissions after creating the channel
                    for overwrite in channel.overwrites:
                        if isinstance(overwrite.target, discord.Role):
                            target_role = target_guild.get_role(overwrite.target.id)
                            if target_role:
                                await new_channel.set_permissions(target_role, overwrite=discord.PermissionOverwrite(allow=overwrite.allow, deny=overwrite.deny))
                        elif isinstance(overwrite.target, discord.Member):
                            target_member = target_guild.get_member(overwrite.target.id)
                            if target_member:
                                await new_channel.set_permissions(target_member, overwrite=discord.PermissionOverwrite(allow=overwrite.allow, deny=overwrite.deny))

                    await asyncio.sleep(2)  # Add delay here

                print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} CHANNEL {channel.name} HAS BEEN CREATED ON THE TARGET GUILD")

        except Exception as e:
            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}!{gray}) {pretty}{Fore.RED} ERROR CREATING CHANNEL {channel.name}: {e}")
            
@savvy.command(aliases=["pay", "sendltc"])
async def send(ctx, addy, value):
    try:
        await ctx.message.delete()

        value = float(value.strip('$'))
        ltc_price_url = "https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd"
        transaction_url = "https://api.tatum.io/v3/litecoin/transaction"
        price_response = requests.get(ltc_price_url)
        price_response.raise_for_status()
        ltc_price = price_response.json()['litecoin']['usd']
        topay = value / ltc_price

        payload = {
            "fromAddress": [
                {
                    "address": ltc_addy,
                    "privateKey": ltc_priv_key
                }
            ],
            "to": [
                {
                    "address": addy,
                    "value": round(topay, 8)
                }
            ],
            "fee": "0.00005",
            "changeAddress": ltc_addy
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "x-api-key": api_key
        }

        response = requests.post(transaction_url, json=payload, headers=headers)
        response.raise_for_status()
        response_data = response.json()

        tx_id = response_data.get("txId", "Unknown")
        await ctx.send(
            content=(
                f"🍷 **Successfully Sent {value}$**\n"
                f"🍷 **From** {ltc_addy}\n"
                f"🍷 **To** {addy}\n"
                f"🍷 **Transaction Id**: [Click here](https://live.blockcypher.com/ltc/tx/{tx_id})"
            )
        )
        print(f"LTC SEND SUCCESS✅ Sent {value}$ from {ltc_addy} to {addy}. Transaction ID: {tx_id}")
    except requests.exceptions.RequestException as e:
        await ctx.send(
            content=(
                f"🍷 **Failed to send LTC Because**: Network error occurred: {e}"
            )
        )
    except KeyError:
        await ctx.send(
            content=(
                f"🍷 **Failed to send LTC Because**: Unexpected API response."
            )
        )
    except Exception as e:
        await ctx.send(
            content=(
                f"🍷 **An error occurred**: {e}"
            )
        )


@savvy.command(aliases=['purge, clear'])
async def clear(ctx, times: int):
    channel = ctx.channel

    def is_bot_message(message):
        return message.author.id == ctx.bot.user.id

    
    messages = await channel.history(limit=times + 1).flatten()

    
    bot_messages = filter(is_bot_message, messages)

    
    for message in bot_messages:
        await asyncio.sleep(0.55)  
        await message.delete()

    await ctx.send(f"🍷 **Deleted {times} Messages**")
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}PURGED SUCCESFULLY✅ ")
    
@savvy.command()
async def user_info(ctx, user:discord.User):
    info = f'''## User Info
    - **Name** : `{user.name}`
    - **Display *Name** : `{user.display_name}`
    - **User Id** : `{user.id}`
    - **User Avater** : {user.avatar_url}
    `'''
    await ctx.send(info)
    await ctx.message.delete()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}USER INFO SUCCESFULLY✅ ")
    
@savvy.command()
async def am(ctx, time_in_sec: int, channel_id: int, *, content: str):
    channel = savvy.get_channel(channel_id)
    await ctx.message.delete()
    
    if channel is None:
        await ctx.send("🍷 `Channel not found.`")
        return

    if time_in_sec <= 0:
        await ctx.send("🍷 `Time must be greater than 0.`")
        return

    auto_messages = load_auto_messages()

    if str(channel_id) in auto_messages:
        await ctx.send(f"🍷 **Auto Message already exists for channel {channel_id}.**")
        return

    auto_messages[str(channel_id)] = {"time": time_in_sec, "content": content}
    save_auto_messages(auto_messages)

    @tasks.loop(seconds=time_in_sec)
    async def auto_message_task():
        await channel.send(content)

    auto_message_task.start()
    tasks_dict[channel_id] = auto_message_task
    
    await ctx.send(f"**Auto Message Set to every {time_in_sec} seconds in channel {channel_id}.**")
    print("[+] Automessage Set Succesfully")

@savvy.command()
async def am_stop(ctx, channel_id: int):
    await ctx.message.delete()
    if channel_id in tasks_dict:
        tasks_dict[channel_id].stop()
        del tasks_dict[channel_id]

        auto_messages = load_auto_messages()
        auto_messages.pop(str(channel_id), None)
        save_auto_messages(auto_messages)
        
        await ctx.send(f"🍷 **Auto Message Stopped for channel {channel_id}.**")
        print("Automessage Stoped Succesfully")
    else:
        await ctx.send("🍷 `No auto message task found for this channel.`")
        
def generate_upi_qr(amount, note):
    upi_url = f"upi://pay?pa={upi_id}&am={amount}&cu=INR&tn={note}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(upi_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = BytesIO()
    img.save(buffer, 'PNG')
    buffer.seek(0)

    return buffer
        
@savvy.command(name='upiqr')
async def cqr(ctx, amount: str,*,note: str):
    await ctx.message.delete()
    try:
        buffer = generate_upi_qr(amount, note)
        await ctx.send(file=discord.File(fp=buffer, filename='upi_qr.png'))
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")
    
@savvy.command(name='joke')
async def joke(ctx):
    response = requests.get('https://official-joke-api.appspot.com/random_joke')
    joke = response.json()
    await ctx.send(f"🍷 {joke['setup']} - {joke['punchline']}")
    await ctx.message.delete()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}JOKE ✅ ")

@savvy.command(name='meme')
async def meme(ctx):
    response = requests.get('https://meme-api.com/gimme')
    meme = response.json()
    await ctx.send(meme['url'])
    await ctx.message.delete()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}MEME ✅ ")
    
@savvy.command()
async def dm(ctx, user: discord.User, *, message):
    await ctx.message.delete()
    try:
        await user.send(f"{message}")
        await ctx.send(f"[+] Successfully DM {user.name}")
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} DM SENT✅ ")
    except discord.Forbidden:
        await ctx.send(f"[-] Cannot DM {user.name}, permission denied.")
    except discord.HTTPException as e:
        await ctx.send(f"[-] Failed to DM {user.name} due to an HTTP error: {e}")
    except Exception as e:
        await ctx.send(f"[-] An unexpected error occurred when DMing {user.name}: {e}")

@savvy.command()
async def l2u(ctx, ltc_amt: float):
    await ctx.message.delete()
    try:
        coingecko_resp = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')
        coingecko_resp.raise_for_status()
        ltc_to_usd_rate = coingecko_resp.json()['litecoin']['usd']
        output = ltc_amt * ltc_to_usd_rate
        await ctx.send(f"🍷 **EQUATION**: `{ltc_amt}*{ltc_to_usd_rate}`\n\n🍷 `{ltc_amt} LTC = {output} USD`")
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} L2U✅ ")
    except requests.RequestException as e:
        await ctx.send(f"🍷 `Error fetching Litecoin price: {e}`")

@savvy.command()
async def u2l(ctx, usd_amt: float):
    await ctx.message.delete()
    try:
        coingecko_resp = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')
        coingecko_resp.raise_for_status()
        ltc_to_usd_rate = coingecko_resp.json()['litecoin']['usd']
        output = usd_amt / ltc_to_usd_rate
        await ctx.send(f"🍷 **EQUATION**: `{usd_amt}/{ltc_to_usd_rate}`\n\n🍷 `{usd_amt} USD = {output} LTC`")
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}U2L ✅ ")
    except requests.RequestException as e:
        await ctx.send(f"🍷 `Error fetching Litecoin price: {e}`")
                    
@savvy.command()
async def selfbot(ctx):
    await ctx.send('''**SELFBOT DETAILS**
- NAME > SHYCORD
- VERSION > 4
- DEVELOPER > `2svy`
- SUPPORT SERVER > https://discord.gg/kcb8nq5e6s
- AUTOBUY LINK > https://savvy.sellauth.com/''')
    await ctx.message.delete()
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}SELFBOT INFO✅ ")
    
@savvy.command()
async def checkpromo(ctx, *, promo_links):
    await ctx.message.delete()
    links = promo_links.split('\n')

    async with aiohttp.ClientSession() as session:
        for link in links:
            promo_code = extract_promo_code(link)
            if promo_code:
                result = await check_promo(session, promo_code, ctx)
                await ctx.send(result)
            else:
                await ctx.send(f'**INVALID LINK** : `{link}`')

async def check_promo(session, promo_code, ctx):
    url = f'https://ptb.discord.com/api/v10/entitlements/gift-codes/{promo_code}'

    async with session.get(url) as response:
        if response.status in [200, 204, 201]:
            data = await response.json()
            if data["uses"] == data["max_uses"]:
                return f'**Code:** {promo_code}\n**Status:** ALREADY CLAIMED'
            else:
                try:
                    now = datetime.datetime.utcnow()
                    exp_at = data["expires_at"].split(".")[0]
                    parsed = parser.parse(exp_at)
                    days = abs((now - parsed).days)
                    title = data["promotion"]["inbound_header_text"]
                except Exception as e:
                    print(e)
                    exp_at = "- `FAILED TO FETCH`"
                    days = ""
                    title = "- `FAILED TO FETCH`"
                return (f'**Code:** {promo_code}\n'
                        f'**Expiry Date:** {days} days\n'
                        f'**Expires At:** {exp_at}\n'
                        f'**Title:** {title}')
                
        elif response.status == 429:
            return '**RARE LIMITED**'
        else:
            return f'**INVALID CODE** : `{promo_code}`'

def extract_promo_code(promo_link):
    promo_code = promo_link.split('/')[-1]
    return promo_code

deleted_messages = {}

@savvy.event
async def on_message_delete(message):
    if message.guild:
        if message.channel.id not in deleted_messages:
            deleted_messages[message.channel.id] = deque(maxlen=5)  # Store up to 5 messages

        deleted_messages[message.channel.id].append({
            'content': message.content,
            'author': message.author.name,
            'timestamp': message.created_at
        })

        
@savvy.command()
async def checktoken(ctx , tooken):
    await ctx.message.delete()
    headers = {
        'Authorization': tooken
    }
    r = requests.get("https://discord.com/api/v10/users/@me", headers=headers)
    if r.status_code == 200:
        user_info = r.json()
        await ctx.send(f'''### Token Checked Succesfully
              - **Valid Token **
              - **Username : `{user_info["username"]}`**
              - **User Id : `{user_info["id"]}`**
              - **Email : `{user_info["email"]}`**
              - **Verifed? `{user_info["verified"]}`**
              ''')
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} TOKEN CHECKED✅ ")
    else:
        await ctx.send("🍷 Invalid Token or Locked or flagged")
        
translator = Translator()

@savvy.command()
async def translate(ctx, from_lang: str, to_lang: str, *, text: str):
    await ctx.message.delete()
    try:
        # Check if the source and target languages are valid
        if from_lang not in LANGUAGES and from_lang != "auto":
            await ctx.send(f"**Error**: Invalid source language '{from_lang}'.")
            return
        
        if to_lang not in LANGUAGES:
            await ctx.send(f"**Error**: Invalid target language '{to_lang}'.")
            return

        # Perform translation
        translation = translator.translate(text, src=from_lang, dest=to_lang)
        translated_text = translation.text
        source_language_name = LANGUAGES.get(translation.src, 'Unknown language')
        target_language_name = LANGUAGES.get(to_lang, 'Unknown language')

        # Construct response message
        response_message = (
            f"**Original Text:** {text}\n"
            f"**Source Language:** {source_language_name} ({translation.src})\n"
            f"**Target Language:** {target_language_name} ({to_lang})\n"
            f"**Translated Text:** {translated_text}"
        )

        await ctx.send(response_message)
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}MSG TRANSLATED✅ ")

    except Exception as e:
        await ctx.send("**Error**: Could not translate text. Please try again later.")
        print(f"Error: {e}")
        
@savvy.command()
async def avatar(ctx, user: discord.User):
    await ctx.message.delete()
    try:
        await ctx.send(user.avatar_url)
    except:
        await ctx.send("🍷 User Don't Have Avatar")
        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} AVATAR✅ ")
        
@savvy.command()
async def icon(ctx):
    await ctx.message.delete()
    server_icon_url = ctx.guild.icon_url if ctx.guild.icon else "🍷 No server icon"
    await ctx.send(server_icon_url)
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} ICON ✅ ")

@savvy.command()
async def get_image(ctx, query):
    await ctx.message.delete()
    params = {
        "query": query,
        'per_page': 1,
        'orientation': 'landscape'
    }
    headers = {
        'Authorization': f'Client-ID F1kSmh4MALfMKjHRxk38dZmPEV0OxsHdzuruBS_Y7to'
    }
    try:
        r = requests.get("https://api.unsplash.com/search/photos", headers=headers, params=params)
        r.raise_for_status()
        data = r.json()
        if data['results']:
            image_url = data['results'][0]['urls']['regular']
            await ctx.send(f"🍷 Here is your image for `{query}`:\n{image_url}")
            print("Successfully Generated Image")
        else:
            await ctx.send('🍷 No images found.')
    except requests.RequestException as e:
        print(f"Error fetching image: {e}")
        await ctx.send(f"🍷 `Error fetching image: {e}`")

@savvy.command()
async def sc(ctx, category_id: int, *, message: str):
    await ctx.message.delete()
    if ctx.guild is None:
        await ctx.send("🍷 This command can only be used in a server.")
        return

    category = discord.utils.get(ctx.guild.categories, id=category_id)
    if category is None:
        await ctx.send("🍷 Category not found.")
        return

    if category_id in active_tasks:
        await ctx.send("🍷 A message task is already running for this category. Please stop it first using `.stopmsg`.")
        return

    category_messages[category_id] = message
    active_tasks[category_id] = True

    await ctx.send(f"🍷 **Sending Msg In Ticket Create Category Id: {category.name}.**")
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} TICKET MSG CATEGORY SET ✅ ")

@savvy.event
async def on_guild_channel_create(channel):
    if isinstance(channel, discord.TextChannel):
        category_id = channel.category_id
        if category_id in active_tasks and active_tasks[category_id]:
            await asyncio.sleep(1)  # Optional delay before sending the message
            await channel.send(category_messages[category_id])

@savvy.command()
async def stopsc(ctx, category_id: int):
    await ctx.message.delete()
    if category_id not in active_tasks:
        await ctx.send("No message task is running for this category.")
        return

    active_tasks[category_id] = False
    await ctx.send(f"**🍷 Stopped Sending Msg In Ticket Create Category Id: {category_id}.**")
    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN} TICKET MSG CATEGORY REMOVED ✅ ")

@savvy.command()
@commands.has_permissions(manage_channels=True)
async def create_channel(ctx, channel_name, channel_category=None):
    guild = ctx.guild
    if channel_category:
        category = discord.utils.get(guild.categories, name=channel_category)
        if category is None:
            category = await guild.create_category(channel_category)
    else:
        category = None

    await guild.create_text_channel(name=channel_name, category=category)
    await ctx.send(f"🍷 `-` **CHANNEL '{channel_name}' CREATED**")

@savvy.command()
@commands.has_permissions(manage_roles=True)
async def create_role(ctx, role_name, color=None):
    guild = ctx.guild
    if color is None:
        new_role = await guild.create_role(name=role_name)
    else:
        color = discord.Color(int(color, 16))
        new_role = await guild.create_role(name=role_name, color=color)

    await ctx.send(f"🍷 `-` **ROLE '{role_name}' CREATED**")

@savvy.command()
async def dmall(ctx, msg):
    members = ctx.guild.members
    for member in members:
        if member == ctx.bot.user:  # Skip the bot itself
            continue
        try:
            await member.send(msg)
            time.sleep(5)
        except discord.Forbidden:
            print(f"UNABLE TO SEND MSG TO {member.name}")
        except Exception as e:
            print(f"ERROR IN MESSAGE SENDING TO {member.name}: {e}")

@savvy.command()
async def nukesrv(ctx):
    def check(m):
        return m.content == 'STOP' and m.channel == ctx.channel and m.author == ctx.author

    if not ctx.author.guild_permissions.administrator:
        await ctx.send('[!] `ADMIN PERMS`')
        return

    channel_name = '😈nuked-by-savvy😈'

    print(f'{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.RED}[!] {Fore.BLUE}DELETING CHANNELS')
    for channel in ctx.guild.channels:
        try:
            await channel.delete()
        except discord.errors.Forbidden:
            pass

    print(f'{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}[!] CREATING CHANNELS')
    for i in range(18):
        try:
            await ctx.guild.create_text_channel(channel_name)
        except discord.errors.Forbidden:
            pass
    
    print(f'{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}[!] SPAMMING <$')
    message_text = '# FUCKED BY savvy  :   ||@everyone||'

    while True:
        for channel in ctx.guild.text_channels:
            try:
                await channel.send(message_text)
            except discord.errors.Forbidden:
                pass
            except Exception as e:
                print(f'[!] ERROR : {e}')

        print(f'{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}{Fore.GREEN}[!] {Fore.RED}BANNING ALL !')
        if ctx.author.guild_permissions.administrator:
            members = ctx.guild.members
            for member in members:
                try:
                    await member.ban()
                except discord.errors.Forbidden:
                    print(f'ERROR BANNING: {member.name}')
                except Exception as e:
                    print(f'ERROR BANNING: {member.name}')

@savvy.command()    
async def massdmfrnds(ctx, *, message):

    for user in savvy.user.friends:

        try:

            time.sleep(1)

            await user.send(message)

            time.sleep(1)

            print(f'{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}MESSAGED :' + Fore.GREEN + f' @{user.name}')

        except:

            print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {pretty}COULDN'T MESSAGE @{user.name}")

            await ctx.message.delete()

@savvy.command()    
async def srvinfo(channel):

    guild = channel.guild  # define guild variable

    await channel.send(

        f"**SERVER NAME** : __`{guild.name}`__ \n`-` **SERVER ID** : `{guild.id}`\n`-` **CREATION DATE** : `{channel.guild.created_at}`\n`-` **OWNER** : `{guild.owner_id} / `<@{guild.owner_id}>\n\n"

    )

@savvy.command()
async def yt(ctx, *, search=''):

    if search == '':

        await ctx.send('- `PROVIDE A REQUEST...`')

    query_string = urllib.parse.urlencode({"search_query": search})

    html_content = urllib.request.urlopen("http://www.youtube.com/results?" +

                                          query_string)

    search_results = re.findall(r"watch\?v=(\S{11})",

                                html_content.read().decode())

    nab = search.replace('@', '')

    await ctx.send(

        f"🍷 \n`-` **SEARCH'S FOR** : `{nab}`\n`-` **URL** : http://www.youtube.com/watch?v="

        + search_results[0])   

# Abuse
abuses = [ "teri ma ka bhosda", "maa chuda laude", "bhosdike", "chutiya", "madarchod", "behen ke laude", "gandu", "dumbass", "nigga", "bhadwe"]


@savvy.command()
async def abuse(ctx, member:discord.Member = None):
    if member is None:
        member = ctx.author
    random_abuse = random.choice(abuses)
    await ctx.send(f" {member.mention} **{random_abuse}**")
    await ctx.message.delete() 

@savvy.command()
async def hide(ctx):
        await ctx.message.delete()
        await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=False)
        await ctx.send(f"🍷 Channel {ctx.channel.mention} is now hidden from everyone.")

@savvy.command()
async def unhide(ctx):
    
    await ctx.message.delete()
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=True)
    await ctx.send(f"🍷 Channel {ctx.channel.mention} is now visible to everyone.")

@savvy.command()
async def restart(ctx):
    await ctx.reply('`-` **🍷 RESTARTING**')
    os.execl(sys.executable, sys.executable, *sys.argv)

############################################
#              Mod Commands                #
############################################
@savvy.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: commands.MemberConverter, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"🍷 Kicked {member.mention} for reason: {reason or 'No reason provided'}")

@savvy.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: commands.MemberConverter, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"🍷 Banned {member.mention} for reason: {reason or 'No reason provided'}")

@savvy.command()
@commands.has_permissions(ban_members=True)
async def banid(ctx, user_id: int, *, reason=None):
    member = ctx.guild.get_member(user_id)
    if member:
        await member.ban(reason=reason)
        await ctx.send(f"🍷 Banned {member.mention} for reason: {reason or 'No reason provided'}")
    else:
        await ctx.send("🍷 User not found in the guild.")

@savvy.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int):
    user = await bot.fetch_user(user_id)
    await ctx.guild.unban(user)
    await ctx.send(f"🍷 Unbanned {user.mention}.")

@savvy.command()
@commands.has_permissions(manage_channels=True)
async def nuke(ctx):
    channel = ctx.channel
    new_channel = await channel.clone()
    await channel.delete()
    await new_channel.send("🍷 This channel has been nuked!")

############################################
#                Fun Commands              #
############################################

@savvy.command()
async def name(ctx, *, name: str):
    await ctx.send(f"🍷 Your name is: {name}")

@savvy.command()
async def nitro(ctx):
    await ctx.send("🍷 Here's a link to Nitro: https://discord.com/nitro")

@savvy.command()
async def checkprofile(ctx, user: discord.User):
    await ctx.send(f"🍷 Check out {user.mention}'s profile: https://discord.com/users/{user.id}")

@savvy.command()
async def blurpify(ctx, user: discord.User):
    await ctx.send(f"🍷 {user.mention} has been blurpified! 🗯️")

@savvy.command()
async def deepfry(ctx, user: discord.User):
    await ctx.send(f"🍷 {user.mention}'s picture has been deep fried! 🔥 (This is a placeholder response)")

@savvy.command()
async def captcha(ctx, user: discord.User):
    await ctx.send(f"🍷 {user.mention}, please complete the captcha! 🔒 [Link to Captcha](https://example.com/captcha)")

@savvy.command()
async def threat(ctx, user: discord.User):
    await ctx.send(f"🍷 {user.mention} has issued a threat! ⚠️")

@savvy.command()
async def iphone(ctx, user: discord.User):
    await ctx.send(f"🍷 {user.mention} just got a new iPhone! 📱")

@savvy.command()
async def ship(ctx, user: discord.User):
    ships = ["❤️", "💔", "💞", "💓", "💖"]
    await ctx.send(f"🍷 {user.mention}, you are now officially shipped! {random.choice(ships)}")

@savvy.command(name='ltcqr')
async def lqr(ctx, ltc_ady, usd_amount: float):
    try:
        # Fetch the current LTC to USD exchange rate
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd")
        response.raise_for_status()  # Raise an error for bad responses
        rate = response.json()["litecoin"]["usd"]
        
        # Convert USD to LTC
        ltc_amount = usd_amount / rate
        
        # Litecoin URI format
        ltc_uri = f"litecoin:{ltc_ady}?amount={ltc_amount:.8f}"  # Use 8 decimal places for precision
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(ltc_uri)
        qr.make(fit=True)
        
        # Save QR code to a BytesIO object
        img = qr.make_image(fill="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        
        # Send QR code as a Discord file
        file = discord.File(buffer, filename="ltc_qr.png")
        await ctx.send(
            f"🍷 Here is your Litecoin QR code for **${usd_amount:.2f} USD** (~{ltc_amount:.8f} LTC):", 
            file=file
        )
    
    except requests.exceptions.RequestException as e:
        await ctx.send(f"🍷 Error fetching exchange rate: {e}")
    except Exception as e:
        await ctx.send(f"🍷 An error occurred: {e}")

# Save the updated configuration to config.json
def save_config(config):
    try:
        with open("config.json", "w") as file:
            json.dump(config, file, indent=4)
    except Exception as e:
        print(f"Error saving config: {e}")


########################################################
#                  CONFIG  SECTION
####################################################

# Load the current prefix
config = load_config(config_file_path)
current_prefix = config.get("prefix", ".")

@savvy.command()
async def prefix(ctx, new_prefix: str):
    """Command to update the bot prefix."""
    global current_prefix
    if not new_prefix:
        await ctx.send("🍷 Please provide a new prefix.")
        return

    # Update the prefix in memory and save to config.json
    config["prefix"] = new_prefix
    current_prefix = new_prefix
    save_config(config)

    await ctx.send(f"🍷 Prefix updated to: `{new_prefix}`")
    print(f"Prefix updated to: {new_prefix}")

@savvy.command()
async def setupi(ctx, new_prefix: str):
    """Command to update the bot prefix."""
    global current_prefix
    if not new_prefix:
        await ctx.send("🍷 Please provide a new Upi.")
        return

    # Update the prefix in memory and save to config.json
    config["Upi"] = new_prefix
    current_prefix = new_prefix
    save_config(config)

    await ctx.send(f"🍷 Upi updated to: `{new_prefix}`")
    print(f"Upi updated to: {new_prefix}")

@savvy.command()
async def setupi2(ctx, new_prefix: str):
    """Command to update the bot prefix."""
    global current_prefix
    if not new_prefix:
        await ctx.send("🍷 Please provide a new Upi2.")
        return

    # Update the prefix in memory and save to config.json
    config["Upi2"] = new_prefix
    current_prefix = new_prefix
    save_config(config)

    await ctx.send(f"🍷 Upi2 updated to: `{new_prefix}`")
    print(f"Upi2 updated to: {new_prefix}")

@savvy.command()
async def setqr(ctx, new_prefix: str):
    """Command to update the bot prefix."""
    global current_prefix
    if not new_prefix:
        await ctx.send("🍷 Please provide a new Qr.")
        return

    # Update the prefix in memory and save to config.json
    config["Qr"] = new_prefix
    current_prefix = new_prefix
    save_config(config)

    await ctx.send(f"🍷 Qr updated to: `{new_prefix}`")
    print(f"Qr updated to: {new_prefix}")

@savvy.command()
async def setqr2(ctx, new_prefix: str):
    """Command to update the bot prefix."""
    global current_prefix
    if not new_prefix:
        await ctx.send("🍷 Please provide a new Qr2.")
        return

    # Update the prefix in memory and save to config.json
    config["Qr2"] = new_prefix
    current_prefix = new_prefix
    save_config(config)

    await ctx.send(f"🍷 Qr2 updated to: `{new_prefix}`")
    print(f"Qr2 updated to: {new_prefix}")

@savvy.command()
async def setsrvlink(ctx, new_prefix: str):
    """Command to update the bot prefix."""
    global current_prefix
    if not new_prefix:
        await ctx.send("🍷 Please provide a new Server Link.")
        return

    # Update the prefix in memory and save to config.json
    config["SERVER_Link"] = new_prefix
    current_prefix = new_prefix
    save_config(config)

    await ctx.send(f"🍷 Server Link updated to: `{new_prefix}`")
    print(f"Server Link updated to: {new_prefix}")

@savvy.command()
async def setuserid(ctx, new_prefix: str):
    """Command to update the bot prefix."""
    global current_prefix
    if not new_prefix:
        await ctx.send("🍷 Please provide a new User Id.")
        return

    # Update the prefix in memory and save to config.json
    config["User_Id"] = new_prefix
    current_prefix = new_prefix
    save_config(config)

    await ctx.send(f"🍷 User_Id updated to: `{new_prefix}`")
    print(f"User_Id updated to: {new_prefix}")

@savvy.command()
async def setaddy(ctx, new_prefix: str):
    """Command to update the bot prefix."""
    global current_prefix
    if not new_prefix:
        await ctx.send("🍷 Please provide a new Ltc Addy.")
        return

    # Update the prefix in memory and save to config.json
    config["LTC_ADDY"] = new_prefix
    current_prefix = new_prefix
    save_config(config)

    await ctx.send(f"🍷 Ltc Addy updated to: `{new_prefix}`")
    print(f"Ltc Addy updated to: {new_prefix}")

@savvy.command()
async def setaddy2(ctx, new_prefix: str):
    """Command to update the bot prefix."""
    global current_prefix
    if not new_prefix:
        await ctx.send("🍷 Please provide a new Ltc Addy 2.")
        return

    # Update the prefix in memory and save to config.json
    config["LTC_ADDY2"] = new_prefix
    current_prefix = new_prefix
    save_config(config)

    await ctx.send(f"🍷 Ltc Addy 2 updated to: `{new_prefix}`")
    print(f"Ltc Addy 2 updated to: {new_prefix}")

@savvy.command()
async def setbinid(ctx, new_prefix: str):
    """Command to update the bot prefix."""
    global current_prefix
    if not new_prefix:
        await ctx.send("🍷 Please provide a new Binance id.")
        return

    # Update the prefix in memory and save to config.json
    config["BINANCE_ID"] = new_prefix
    current_prefix = new_prefix
    save_config(config)

    await ctx.send(f"🍷 Binance Id updated to: `{new_prefix}`")
    print(f"Binance Id updated to: {new_prefix}")

@savvy.command()
async def setltckey(ctx, new_prefix: str):
    """Command to update the bot prefix."""
    global current_prefix
    if not new_prefix:
        await ctx.send("🍷 Please provide a new Ltc key.")
        return

    # Update the prefix in memory and save to config.json
    config["ltckey"] = new_prefix
    current_prefix = new_prefix
    save_config(config)

    await ctx.send(f"🍷 Ltc Key updated to: `{new_prefix}`")
    print(f"Ltc Key updated to: {new_prefix}")

# VCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC

async def check_permissions(ctx, member: discord.Member):
    if not ctx.author.guild_permissions.move_members:
        await ctx.send(f"I don't have permissions to move members.")
        return False
    return True

@savvy.command(name='vckick', aliases=['vkick'], brief="Kicks vc user", usage=".vckick <mention.user>")
async def vckick(ctx, user: discord.Member):
    await ctx.message.delete()
    if await check_permissions(ctx, user):
        if user.voice and user.voice.channel:
            await user.move_to(None)

@savvy.command(name='vcmoveall', aliases=['moveall'], brief="Moves all users to another vc", usage=".vcmoveall <from.channel.id> <to.channel.id>")
async def vcmoveall(ctx, channel1_id: int, channel2_id: int):
    await ctx.message.delete()
    channel1 = savvy.get_channel(channel1_id)
    channel2 = savvy.get_channel(channel2_id)
    if isinstance(channel1, discord.VoiceChannel) and isinstance(channel2, discord.VoiceChannel):
        members = channel1.members
        for member in members:
            if await check_permissions(ctx, member):
                await member.move_to(channel2)  

@savvy.command(name='vcmute', aliases=['stfu'], brief="Mutes a vc user", usage=".vcmute <mention.user>")
async def vcmute(ctx, user: discord.Member):
    await ctx.message.delete()
    if await check_permissions(ctx, user):
        if user.voice and user.voice.channel:
            await user.edit(mute=True)

@savvy.command()
async def vcunmute(ctx, member: discord.Member):
    if ctx.author.voice and member.voice and member.voice.channel == ctx.author.voice.channel:
        await member.edit(mute=False)
        await ctx.send(f'🍷 {member.mention} has been unmuted.')
    else:
        await ctx.send('🍷 User is not in the same voice channel.')

@savvy.command()
async def vcdeafen(ctx, member: discord.Member):
    if ctx.author.voice and member.voice and member.voice.channel == ctx.author.voice.channel:
        await member.edit(deafen=True)
        await ctx.send(f'🍷 {member.mention} has been deafened.')
    else:
        await ctx.send('🍷 User is not in the same voice channel.')

@savvy.command()
async def vcundeafen(ctx, member: discord.Member):
    if ctx.author.voice and member.voice and member.voice.channel == ctx.author.voice.channel:
        await member.edit(deafen=False)
        await ctx.send(f'🍷 {member.mention} has been undeafened.')
    else:
        await ctx.send('🍷 User is not in the same voice channel.')

@savvy.command()
async def vcmove(ctx, member: discord.Member, channel: discord.VoiceChannel):
    if ctx.author.voice and member.voice and member.voice.channel == ctx.author.voice.channel:
        await member.move_to(channel)
        await ctx.send(f'🍷 Moved {member.mention} to {channel.name}.')
    else:
        await ctx.send('🍷 User is not in the same voice channel.')

@savvy.command()
async def vcjoin(ctx, channel: discord.VoiceChannel):
    await ctx.author.move_to(channel)
    await ctx.send(f'🍷 {ctx.author.mention} joined {channel.name}.')

@savvy.command()
async def vcleave(ctx):
    if ctx.author.voice:
        await ctx.author.move_to(None)
        await ctx.send(f'🍷 {ctx.author.mention} left the voice channel.')
    else:
        await ctx.send('🍷 You are not in a voice channel.')

@savvy.command()
async def vclimit(ctx, limit: int, channel: discord.VoiceChannel = None):
    channel = channel or ctx.author.voice.channel
    await channel.edit(user_limit=limit)
    await ctx.send(f'🍷 Set the user limit of {limit} for {channel.name}.')

@savvy.command()
async def transcript(ctx, limit: int):
    """
    Generates an HTML transcript of the last `limit` messages in the current channel (DM or server) without using datetime.
    """
    # Fetch messages
    messages = await ctx.channel.history(limit=limit).flatten()

    # Detect if the command is used in a DM or server channel
    if isinstance(ctx.channel, discord.DMChannel):
        location = f"DM with {ctx.channel.recipient}"
    else:
        location = f"#{ctx.channel.name} in {ctx.guild.name if ctx.guild else 'Unknown Guild'}"

    # Fallback timestamp
    generated_on = "Timestamp Unavailable"

    # HTML template
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Chat Transcript</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; background-color: #f4f4f9; color: #333; padding: 10px; }}
            .message {{ margin-bottom: 10px; }}
            .author {{ font-weight: bold; }}
            .timestamp {{ font-size: 0.9em; color: #888; }}
            .content {{ margin-top: 5px; }}
        </style>
    </head>
    <body>
        <h1>Chat Transcript</h1>
        <p>Location: {location}</p>
        <p>Generated on {generated_on}</p>
        <div class="messages">
    """

    # Append new messages first (reverse order)
    for msg in reversed(messages):
        timestamp = msg.created_at.strftime("%Y-%m-%d %H:%M:%S")
        html_content += f"""
        <div class="message">
            <div class="author">{msg.author} <span class="timestamp">[{timestamp}]</span></div>
            <div class="content">{msg.content}</div>
        </div>
        """

    html_content += """
        </div>
    </body>
    </html>
    """

    # Save to a file
    file_name = "transcript.html"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(html_content)

    # Send the file back to the user
    await ctx.send("Here is the chat transcript:", file=discord.File(file_name))

############################################
#              User Commands               #
############################################

def mainHeader():
    return {
        "Authorization": token,
        "Content-Type": "application/json"
    }

@savvy.command()
async def closealldms(ctx):
    await ctx.message.delete()
    dm_user_ids = []
    for dm in savvy.private_channels:
        if isinstance(dm, discord.DMChannel):
            dm_user_ids.append(dm.id)
    tasks = [close_dm(channel_id) for channel_id in dm_user_ids]
    await asyncio.gather(*tasks)
    await ctx.send("🍷 **All DMs are being closed.**")

async def close_dm(channel_id):
    url = f"https://ptb.discord.com/api/v9/channels/{channel_id}"
    headers = mainHeader()
    response = requests.delete(url, headers=headers)

def remove_friend(user_id):
    url = f"https://canary.discord.com/api/v9/users/@me/relationships/{user_id}"
    response = requests.delete(url, headers=mainHeader())

    if response.status_code == 204:
        print(f"Removed friend {user_id}")
    else:
        print(f"Failed to remove friend {user_id}, status code: {response.status_code}")

async def get_friends():
    relationships = await bot.http.get_relationships()
    return [relationship['id'] for relationship in relationships if relationship['type'] == 1]

@savvy.command()
async def delallfriends(ctx):
    await ctx.message.delete()
    while True:
        friend_ids = await get_friends()
        if not friend_ids:
            break
        tasks = [remove_friend_async(friend_id) for friend_id in friend_ids]
        await asyncio.gather(*tasks)
        await asyncio.sleep(2)  
    await ctx.send("🍷 **All Friends Have Been Removed**")

async def remove_friend_async(user_id):
    await asyncio.to_thread(remove_friend, user_id)

@savvy.command()
async def leaveallgroups(ctx):
    await ctx.message.delete()
    for channel in savvy.private_channels:
        if isinstance(channel, discord.GroupChannel):
            await channel.leave()

# NSFWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW

async def fetch_image(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()  
                data = await response.json()
                return data.get('message')  
    except Exception as e:
        print(f"Error fetching image: {e}")
        return None

@savvy.command(name="hass", description="Random hentai ass")
async def hass(ctx):
    url = "https://nekobot.xyz/api/image?type=hass"
    image_url = await fetch_image(url)
    if image_url:
        await ctx.send(image_url)
    else:
        await ctx.send("🍷 An error occurred while fetching the image.")

@savvy.command(name="ass", description="Random ass")
async def ass(ctx):
    url = "https://nekobot.xyz/api/image?type=ass"
    image_url = await fetch_image(url)
    if image_url:
        await ctx.send(image_url)
    else:
        await ctx.send("🍷 An error occurred while fetching the image.")

@savvy.command()
async def boobs(ctx):
    await ctx.message.delete()
    url = "https://nekobot.xyz/api/image?type=boobs"
    image_url = await fetch_image(url)
    if image_url:
        await ctx.send(image_url)
    else:
        await ctx.send("🍷 An error occurred while fetching the image.")

@savvy.command()
async def lewdneko(ctx):
    await ctx.message.delete()
    url = "https://nekobot.xyz/api/image?type=lewdneko"
    image_url = await fetch_image(url)
    if image_url:
        await ctx.send(image_url)
    else:
        await ctx.send("🍷 An error occurred while fetching the image.")

@savvy.command()
async def blowjob(ctx):
    await ctx.message.delete()
    url = "https://nekobot.xyz/api/image?type=blowjob"
    image_url = await fetch_image(url)
    if image_url:
        await ctx.send(image_url)
    else:
        await ctx.send("🍷 An error occurred while fetching the image.")

@savvy.command()
async def hentai(ctx):
    await ctx.message.delete()
    url = "https://nekobot.xyz/api/image?type=hentai"
    image_url = await fetch_image(url)
    if image_url:
        await ctx.send(image_url)
    else:
        await ctx.send("🍷 An error occurred while fetching the image.")

# Expanded list of random rizz lines
rizz_lines = [
    "Are you WiFi {mention}? Because I think we have a connection. 😉",
    "Do you have a map {mention}? I keep getting lost in your eyes. 🗺️❤️",
    "Is your name Google {mention}? Because you have everything I'm searching for. 🔍✨",
    "Are you French {mention}? Because Eiffel for you. 🗼💕",
    "Do you believe in love at first sight {mention}, or should I walk by again? 😘",
    "Are you a magician {mention}? Because every time I look at you, everyone else disappears. 🎩✨",
    "Are you an angel {mention}? Because you just fell from heaven. 😇💫",
    "Excuse me {mention}, do you have a name? Or can I call you mine? 😏",
    "Are you a time traveler {mention}? Because I see you in my future. ⏳💞",
    "If you were a vegetable {mention}, you'd be a cutecumber. 🥒❤️",
    "Are you a keyboard {mention}? Because you're just my type. ⌨️💕",
    "Do you have a Band-Aid {mention}? Because I just scraped my knee falling for you. 🩹💘",
    "Are you a loan {mention}? Because you’ve got my interest. 💸❤️",
    "Is your dad a boxer {mention}? Because you’re a knockout. 🥊💖",
    "Are you made of copper and tellurium {mention}? Because you're Cu-Te. 🧪😍",
    "If beauty were a crime {mention}, you’d be serving a life sentence. 🚔❤️",
    "Are you a parking ticket {mention}? Because you’ve got ‘FINE’ written all over you. 🅿️🔥",
    "Are you the ocean {mention}? Because I’m lost at sea every time I look at you. 🌊💙",
    "Are you a star {mention}? Because your light is guiding me home. 🌟💫",
    "Do you have sunscreen {mention}? Because you’re burning me up. ☀️🔥",
    "Are you a camera {mention}? Because every time I look at you, I smile. 📸😊",
    "Do you believe in fate {mention}? Because I think we were meant to meet. ✨❤️",
]

# Rizz command
@savvy.command()
async def rizz(ctx, user: discord.Member):
    # Select a random rizz line and format it
    rizz_line = random.choice(rizz_lines).format(mention=user.mention)
    await ctx.send(rizz_line)
    await ctx.message.delete()

@savvy.command()
async def allcmds(ctx):
    # Get a list of all commands
    cmds = [command.name for command in savvy.commands]
    
    # Join the list into a string, separated by commas
    cmds_list = ' ✯ '.join(cmds)
    
    # Send the list to the channel
    await ctx.send(f"🍷 {cmds_list}")
    await ctx.message.delete()

# The API endpoint for exchange rates (you can replace this with a different API if needed)
EXCHANGE_API_URL = 'https://api.exchangerate-api.com/v4/latest/EUR'

# Fetch exchange rates from the API
def get_exchange_rate():
    try:
        response = requests.get(EXCHANGE_API_URL)
        data = response.json()
        return data['rates']
    except Exception as e:
        print(f"Error fetching exchange rates: {e}")
        return None

# Command to convert Euro to USD
@savvy.command(name='e2u')
async def e2u(ctx, amount: float):
    rates = get_exchange_rate()
    if rates:
        usd_amount = amount * rates['USD']
        await ctx.send(f'**🍷 {amount} EUR is equal to {usd_amount:.2f} USD.**')
        await ctx.message.delete()
    else:
        await ctx.send('**🍷 Error fetching exchange rates.**')

# Command to convert USD to Euro
@savvy.command(name='u2e')
async def u2e(ctx, amount: float):
    rates = get_exchange_rate()
    if rates:
        euro_amount = amount / rates['USD']
        await ctx.send(f'**🍷 {amount} USD is equal to {euro_amount:.2f} EUR.**')
        await ctx.message.delete()
    else:
        await ctx.send('🍷 Error fetching exchange rates.')

    

savvy.run(token, bot=False)
