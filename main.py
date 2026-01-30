from shutil import rmtree

from scripts.constants import DOWNLOADS
from scripts.helper import choose, extract_pack, get_downloads, install_modpack


def main():
    pack = choose(get_downloads())
    extract_pack(pack)
    install_modpack(f"{DOWNLOADS}/{pack}")
    rmtree("tmp", ignore_errors=True)


if __name__ == "__main__":
    main()
