![](res/logo.png)
![](res/imf_okt_logo.png)

# GH Demucs GUI

This is a graphical program intended for Guitar Hero charters to split out audio files into guitar, bass, drums, and vocals. It also supports 4 lane drum stemming, and it can rename the files dynamically to the correct layout for Guitar Hero (or similar rhythm games).

# Installation

I have a video tutorial for this setup process if you prefer to watch through video rather than text. [Check it out here!](https://youtu.be/wjRu35c_JsY)

Installing this program is NOT plug-and-play. It will require some setup on your part to get it to work properly.

[You need Python 3.8 or later](https://python.org/downloads) to run both this program and Demucs. **When you install Python, on the very first screen that appears, check the box labelled "Add Python to PATH".**

To set up everything for use, **run the** `install.bat` **file in the folder FIRST.** Wait for the installation to completely finish, and then you can run the `run.bat` file.

**You will need to say Yes (type "Y" or "y") to the uninstall prompt for Torch!** You need that if you want to use CUDA (your graphics card) for splitting audio.

**If you want the drum splitting to work, you need to install** `drumsep` **separately!** To add in `drumsep` for use with the program:
1. Create a `drum_split` folder in the `res` folder.
2. [Download the model file from this link](https://drive.google.com/uc?export=download&id=1g9dD68Fhn-fvTFHRApgFy8bsHUsYJD9o) and place it inside of the `drum_split` folder.

### More documentation coming soon...

# Credits
- Made by [IMF24](https://youtube.com/@IMF24), Help from [Oktoberfest](https://youtube.com/@oktoberfesttheenthusiast)
- [Demucs Audio Separation](https://github.com/facebookresearch/demucs) by [Meta Platforms, Inc.](https://meta.com), [MIT License](./LICENSE)
- [drumsep](https://github.com/inagoy/drumsep) Separation Model by [inagoy](https://github.com/inagoy)