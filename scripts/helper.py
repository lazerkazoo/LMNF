import json
from os import listdir, makedirs, remove
from os.path import dirname
from shutil import copy, copytree
from zipfile import ZipFile

import requests

from scripts.constants import ADDONS_DIR, DOWNLOADS, MODPACKS_DIR, MODPACKS_FILE

session = requests.session()


def download_file(url: str, dest: str):
    makedirs(dirname(dest), exist_ok=True)
    download = session.get(url).content
    with open(dest, "wb") as f:
        f.write(download)


def choose(ls: list):
    for i, j in enumerate(ls):
        print(f"[{i + 1}] {j}")

    return ls[int(input("choose -> ")) - 1]


def confirm(txt="r u sure"):
    return input(f"{txt} (y/n) -> ").lower() in ["y", ""]


def load_json(path: str):
    with open(path, "r") as f:
        return json.load(f)


def save_json(path: str, js):
    with open(path, "w") as f:
        json.dump(js, f, indent=4)


def extract_pack(pack: str, dir=DOWNLOADS):
    with ZipFile(f"{dir}/{pack}", "r") as z:
        z.extractall("/tmp/modpack")


def install_modpack(file2copy: str):
    modpacks = load_json(MODPACKS_FILE)
    index = load_json("/tmp/modpack/modrinth.index.json")
    name = index["name"]
    files = index["files"]
    mc = index["dependencies"]["minecraft"]
    dir = f"{MODPACKS_DIR}/{name.lower()}"

    makedirs(f"{dir}/addons", exist_ok=True)
    makedirs(f"{dir}/fabric", exist_ok=True)

    for num, i in enumerate(files):
        url = i["downloads"][0]
        dest = f"{dir}/fabric/{mc}/{i['path']}"
        print(
            f"[{dirname(dest).split('/')[-1]}] [{num + 1}/{len(files)}] downloading {dest.split('/')[-1]}"
        )
        download_file(url, dest)

    modpacks["packs"][name.lower()] = {
        "name": name,
        "version": mc,
        "modLoader": "fabric",
    }

    if confirm("copy addons from other modpacks"):
        copytree(ADDONS_DIR, f"{dir}/addons", dirs_exist_ok=True)
        if "optifine.jar" in listdir(f"{dir}/addons"):
            remove(f"{dir}/addons/optifine.jar")

    if file2copy is not None:
        copy(file2copy, f"{dir}")

    save_json(MODPACKS_FILE, modpacks)


def get_downloads():
    ls = []
    for i in listdir(DOWNLOADS):
        if i.endswith(".mrpack"):
            ls.append(i)
    return ls
