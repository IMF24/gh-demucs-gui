import os as OS

# Color constants.
BLACK = "\033[0;30m"
RED = "\033[0;31m"
GREEN = "\033[0;32m"
BROWN = "\033[0;33m"
BLUE = "\033[0;34m"
PURPLE = "\033[0;35m"
CYAN = "\033[0;36m"
WHITE = "\033[0;37m"
DARK_GRAY = "\033[1;30m"
LIGHT_RED = "\033[1;31m"
LIGHT_GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
LIGHT_BLUE = "\033[1;34m"
LIGHT_PURPLE = "\033[1;35m"
LIGHT_CYAN = "\033[1;36m"
LIGHT_WHITE = "\033[1;37m"
BOLD_CMD = "\033[1m"
FAINT_CMD = "\033[2m"
ITALIC_CMD = "\033[3m"
UNDERLINE_CMD = "\033[4m"
BLINK_CMD = "\033[5m"
NEGATIVE_CMD = "\033[7m"
CROSSED_CMD = "\033[9m"
END_CMD = "\033[0m"

print(f"{LIGHT_CYAN}----------------------------------")
print(f"{CYAN}Setting things up! Be patient, make yourself a cup of tea...")
print(f"{LIGHT_CYAN}----------------------------------{WHITE}\n")

OS.system('python -m pip install --upgrade demucs PySoundFile')
OS.system('python -m pip install --upgrade Pillow tkinter-tooltip')

print(f"{RED}\n----------------------------------")
if (input(f"{LIGHT_RED}\nIs your GPU manufactured by NVIDIA?\n{WHITE}If it's not OR if you have no GPU, type N. (Y/N): ").upper() == "Y"):
    print(f"\n{YELLOW}All right, now we'll install CUDA. This allows Demucs to work with your computer's dedicated GPU.\nAnswer Yes (\"Y\" or \"y\") to the uninstall prompt!\n{WHITE}")
    OS.system('python -m pip uninstall torch')
    OS.system('python -m pip install torch -f https://download.pytorch.org/whl/torch_stable.html')

print(f"{LIGHT_GREEN}\nAll done; things should be good to go!")

input(f"\n{LIGHT_BLUE}? {WHITE}Press ENTER to exit the installer. {DARK_GRAY}\u00BB {WHITE}")