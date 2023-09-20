import os as OS
import sys as SYS

# List of every Demucs model supported natively in Demucs 4.
DEMUCS_MODELS = [
    ["Demucs 4 HT (Default)", "htdemucs_ft"],
    ["Demucs 4 HT (Default)", "htdemucs_ft"],
    ["Demucs 4", "htdemucs"],
    ["Demucs 4 6 Stem", "htdemucs_6s"],
    ["Demucs MDX Extra Q", "mdx_extra_q"],
    ["Demucs MDX Extra", "mdx_extra"],
    ["Demucs MDX", "mdx"],
    ["Hybrid Demucs 3 MMI", "hdemucs_mmi"],
    ["4 Lane Drum Stems", "modelo_final"]
]
""" List of every Demucs model supported natively in Demucs 4. """

# The devices Demucs can use.
DEMUCS_DEVICES = [
    ['CUDA (GPU)', 'cuda'],
    ['CUDA (GPU)', 'cuda'],
    ['CPU', 'cpu']
]
""" The devices Demucs can use. """

# Audio output types.
AUDIO_OUT_TYPES = [
    ["WAV (Default)", ''],
    ["WAV (Default)", ''],
    ["MP3", '--mp3'],
    ["FLAC", '--flac']
]
""" Audio output formats that Demucs can export to. """

# Relative path function.
def resource_path(relative_path: str) -> str:
    """
    Get the absolute path to a given resource. Used for compatibility with Python scripts compiled to EXEs using PyInstaller whose files have been embedded into the EXE itself.

    Tries at first to use `sys._MEIPASS`, which is used for relative paths. In the event it doesn't work, it will use the absolute path, and join it with the relative path given by the function's arguments.
    
    Arguments
    ---------
    `relative_path` : `str` >> The relative path to convert to an actual path.

    Returns
    -------
    `str` >> The actual path to the given resource.

    Example of Use
    --------------
    The actual output value will vary from device to device. In the below example, `~\` refers to `\"C:\\Users\\Your Username\"`.

    >>> print(resource_path(\"res/icon.ico\"))
    \"~\\Desktop\\GHWT DE Mod Development IDE\\res/icon.ico\"
    """
    # Try and use the actual path, if it exists.
    try:
        base_path = SYS._MEIPASS

    # In the event it doesn't, use the absolute path.
    except Exception:
        base_path = OS.path.abspath(".")

    # Join the paths together!
    print(f"path is {OS.path.join(base_path, relative_path)}")
    return OS.path.join(base_path, relative_path)