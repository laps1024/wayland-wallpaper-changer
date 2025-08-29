import os
import random
import subprocess
import time
from argparse import ArgumentParser
import asyncio

parser = ArgumentParser()
parser.add_argument("-t", "--time", help="Interval", default="30m")
parser.add_argument("-p", "--path", help="Images directory path")
args = parser.parse_args()
if "m" in args.time:
    update_time = int(args.time[:-1]) * 60
else: update_time = int(args.time) * 60
wallpapers_path = os.path.expanduser(args.path)
wallpapers = []
current_wallpaper = None

if wallpapers_path is None or wallpapers_path.strip() == "":
    raise FileNotFoundError("[ERROR] Wallpaper directory not found")

def check_launch():
    result = subprocess.run("ps aux | grep '[s]www-daemon'",shell=True,capture_output=True,text=True)
    if not result.stdout.strip():
        subprocess.Popen("swww-daemon",shell=True)
    print("[LOG] swww launched successfully")

async def check_wallpapers():
    extensions = [".png", ".jpg", ".jpeg"]
    print("[LOG] Checking wallpapers")
    global wallpapers
    if not os.path.exists(wallpapers_path):
        raise FileNotFoundError("[ERROR] Wallpaper directory not found")
    files = os.listdir(wallpapers_path)
    if files:
        while True:
            files = os.listdir(wallpapers_path)
            random.shuffle(files)
            if len(wallpapers) != 0 and len(files) > len(wallpapers):
                new_files = [os.path.join(wallpapers_path, f) for f in files if os.path.join(wallpapers_path, f) not in wallpapers]
                print(f"[LOG] New file detected: {new_files}")
            wallpapers = [os.path.join(wallpapers_path,file) for file in files if any(extension in file.lower() for extension in extensions)]
            if len(wallpapers) < 2:
                raise ValueError("[ERROR] At least 2 files needed")
            await asyncio.sleep(20)
    else:
        raise FileNotFoundError("[ERROR] Wallpaper directory is empty")

def get_unique_wallpaper():
    while True:
        choice = random.choice(wallpapers)
        if choice != current_wallpaper:
            return choice


async def change_wallpaper(wallpaper):
    global current_wallpaper
    await asyncio.to_thread(subprocess.run, f"swww img {wallpaper}", shell=True)
    print(f"[LOG] {time.strftime("%H:%M",time.localtime())}: Changed wallpaper to {wallpaper}")
    current_wallpaper = wallpaper

async def start_timer():
    while not wallpapers:
        await asyncio.sleep(0.1)
    while True:
        wallpaper = get_unique_wallpaper()
        await change_wallpaper(wallpaper)
        await asyncio.sleep(update_time)

async def main():
    check_launch()
    asyncio.create_task(check_wallpapers())
    await start_timer()

if __name__ == "__main__":
    asyncio.run(main())
