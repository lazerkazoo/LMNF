from os.path import expanduser, join
from sys import platform

HOME = expanduser("~")
DOWNLOADS = join(HOME, "Downloads")
LABY_DIR = (
    join(HOME, ".minecraft", "labymod-neo")
    if platform == "linux"
    else join(HOME, "AppData", "Roaming", ".minecraft")
)
MODPACKS_DIR = join(LABY_DIR, "modpacks")
ADDONS_DIR = join(LABY_DIR, "addons")

MODPACKS_FILE = join(MODPACKS_DIR, "modpacks.json")
