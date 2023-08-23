'''
Author: SpenserCai
Date: 2023-08-23 23:12:27
version: 
LastEditors: SpenserCai
LastEditTime: 2023-08-23 23:41:29
Description: file content
'''
import os
import modules.scripts as scripts
import requests
import sys
import tarfile

def get_my_dir():
    if os.path.isdir("extensions/sd-webui-discord-ex"):
        return "extensions/sd-webui-discord-ex"
    return scripts.basedir()

def check_bin():
    bin_path = os.path.join(get_my_dir(), "bin")
    print(bin_path)
    # 如果是windows系统，判断bin_path下是否有sd-webui-discord.exe，如果是linux系统，判断bin_path下是否有sd-webui-discord
    if sys.platform == "win32":
        if os.path.isfile(os.path.join(bin_path, "sd-webui-discord.exe")):
            return True
    elif sys.platform == "linux":
        if os.path.isfile(os.path.join(bin_path, "sd-webui-discord")):
            return True
    return False

def download_bin():
    bin_path = os.path.join(get_my_dir(), "bin")
    api_url = "https://api.github.com/repos/SpenserCai/sd-webui-discord/releases/latest"

    response = requests.get(api_url)
    data = response.json()
    tag_name = data["tag_name"]

    download_url = f"https://github.com/SpenserCai/sd-webui-discord/releases/download/{tag_name}/sd-webui-discord-release-{tag_name}.tar.gz"
    response = requests.get(download_url)
    release_path = os.path.join(bin_path, f"sd-webui-discord-{tag_name}.tar.gz")
    with open(release_path, "wb") as file:
        file.write(response.content)

    with tarfile.open(release_path, "r:gz") as tar:
        members = [m for m in tar.getmembers() if m.name.startswith("release")]
        tar.extractall(path=bin_path, members=members)
    os.remove(release_path)

    with open(os.path.join(bin_path, ".version"), "w") as file:
        file.write(tag_name)
    

    