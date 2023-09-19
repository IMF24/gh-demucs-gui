# - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = - #
#       ___              ___  __               ___  __      ___        _____    #
#      / _ \ /\  /\     /   \/__\/\/\  /\ /\  / __\/ _\    / _ \/\ /\  \_   \   #
#     / /_\// /_/ /    / /\ /_\ /    \/ / \ \/ /   \ \    / /_\/ / \ \  / /\/   #
#    / /_\\/ __  /    / /_///__/ /\/\ \ \_/ / /___ _\ \  / /_\\\ \_/ /\/ /_     #
#    \____/\/ /_/    /___,'\__/\/    \/\___/\____/ \__/  \____/ \___/\____/     #
#                                                                               #
#     MADE BY IMF24                          DEMUCS BY META PLATFORMS, INC.     #
# - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = - #
# Import required modules.
from gui_functions import *
from gui_constants import *
from tkinter import *
from tkinter import ttk as TTK
from tkinter import filedialog as FD, messagebox as MSG
from PIL import Image, ImageTk
from tktooltip import ToolTip
import os as OS
import sys as SYS
import shutil as SHUT
import subprocess as SUB
import demucs.separate
import shlex

# Add output message.
def add_output_msg(msg: str) -> None:
    outputText.config(state = 'normal')
    outputText.insert(END, "\n" + msg)
    outputText.config(state = 'disabled')
    root.update_idletasks()

# Split an audio track into the way the user wants them.
def split_audio() -> None:
    outputText.config(state = 'normal')
    outputText.delete(1.0, END)
    outputText.config(state = 'disabled')

    """ Uses Demucs' main split method to split an audio track in the way the user wanted. """
    # SANITY CHECKS
    if (not audioSource.get()):
        MSG.showerror("No Audio File Given", "You didn't specify an audio file to split out!")
        return
    
    if (not audioOutPath.get()):
        MSG.showerror("No Destination Given", "You didn't specify the directory to output the files into!")
        return

    add_output_msg(f"Audio being split: {audioSource.get()}\nUsing model {model.get()}, outputting in {audioFormat.get()}, using device {device.get()}")
    add_output_msg(f"Shift trick set to {shift.get()}, overlap is set to {int(float(overlap.get()) * 100)}%")
    add_output_msg("Separating audio tracks; BE PATIENT, THIS WILL TAKE A WHILE...")

    useModel = ""
    for (opt, cs) in (DEMUCS_MODELS):
        if (model.get() == opt):
            useModel = cs
            break
    else: useModel = 'htdemucs'

    useDevice = ""
    for (opt, cs) in (DEMUCS_DEVICES):
        if (device.get() == opt):
            useDevice = cs
            break
    else: useDevice = 'cpu'

    useFormat = ""
    for (opt, cs) in (AUDIO_OUT_TYPES):
        if (audioFormat.get() == opt):
            useFormat = cs
            break
    else: useFormat = ""

    # NOW SPLIT IT OUT!
    tempDir = OS.path.join(audioOutPath.get(), "_GHDMGUI_StemTemp")
    cmd = f"-n {useModel} -d {useDevice} {useFormat} --shifts {shift.get()} --overlap {overlap.get()} -o \"{tempDir}\" \"{audioSource.get()}\""

    print(f"demucs command:\n{cmd}")

    demucs.separate.main(shlex.split(cmd))

    if (splitDrums.get()):
        add_output_msg("Splitting drum track to 4 lane...")

        if (useFormat == ""): origExtension = ".wav"
        else: origExtension = f".{useFormat.split('--')[-1]}"

        folderOutName = OS.path.splitext(audioSource.get().split('/')[-1])[0]
        drumTrackName = f"{tempDir}/{useModel}/{folderOutName}/drums{origExtension}"

        cmdSplitDrums = f"--repo \"{resource_path('res/drum_split')}\" -n modelo_final -d {useDevice} {useFormat} --shifts {shift.get()} --overlap {overlap.get()} -o \"{tempDir}\" \"{drumTrackName}\""

        print(f"stem extension: {origExtension}")
        print(f"original file name (for stem folder): {folderOutName}")
        print(f"name of the drum track file: {drumTrackName}")
        print(f"split drums command:\n{cmdSplitDrums}")

        demucs.separate.main(shlex.split(cmdSplitDrums))

    resultPath = OS.path.join(tempDir, f"{useModel}/{folderOutName}")
    if (useGHNames.get()):
        add_output_msg("Renaming audio files to their Guitar Hero names...")

        # Rename the 'other' track to 'guitar'.
        OS.chdir(resultPath)

        for (file) in (OS.listdir(".")):
            if (OS.path.isfile(file)) and (file == f"other{origExtension}"):
                if (model.get() == "Demucs 4 6 Stem"): OS.rename(file, f"song{origExtension}")
                else: OS.rename(file, f"guitar{origExtension}")
                break

        # Rename the drum tracks?
        if (splitDrums.get()):
            OS.chdir(f"../../modelo_final/drums")

            wrongDrumNames = [f"bombo{origExtension}", f"redoblante{origExtension}", f"toms{origExtension}", f"platillos{origExtension}"]

            for (file) in (OS.listdir(".")):
                for (x, name) in (enumerate(wrongDrumNames)):
                    if (file == name): OS.rename(file, f"drums_{x + 1}{origExtension}")

        OS.chdir(OWD)

    add_output_msg("Moving audio files to original output directory...")

    SHUT.copytree(resultPath, audioOutPath.get(), dirs_exist_ok = True)
    SHUT.copytree(f"{tempDir}/modelo_final/drums", audioOutPath.get(), dirs_exist_ok = True)

    add_output_msg("Cleaning Demucs folders...")

    SHUT.rmtree(f"{tempDir}/{useModel}", True)
    SHUT.rmtree(f"{tempDir}/modelo_final", True)

    if (splitDrums.get()) and (excludeOrigDrums.get()):
        add_output_msg("Excluding original drums file...")
        OS.remove(f"{audioOutPath.get()}/drums{origExtension}")
    
    add_output_msg("!! -- AT LAST, ALL DONE! -- !!")
    print("!! - AT LAST, ALL DONE! - !!")
    OS.startfile(audioOutPath.get())

# Get the path to an audio file.
def get_audio_source() -> None:
    """ Opens a file dialog box and adds an audio file from a specified path. """
    sourcePath = FD.askopenfilename(title = "Select Audio File to Split", filetypes = (("Audio Files", ".mp3 .wav .ogg .flac"), ("MP3 Files", ".mp3"), ("WAV Files", ".wav"), ("OGG Vorbis Files", ".ogg"), ("FLAC Files", ".flac")))

    if (not sourcePath): return

    audioSource.delete(0, END)
    audioSource.insert(END, sourcePath)

def set_output_dir() -> None:
    setOutDir = FD.askdirectory(title = "Select Directory to Output Files")

    if (not setOutDir): return

    audioOutPath.delete(0, END)
    audioOutPath.insert(END, setOutDir)

def allow_exclude_drums() -> None:
    if (splitDrums.get()): updateState = 'normal'
    else:
        updateState = 'disabled'
        excludeOrigDrums.set(False)
    
    excludeOrigDrumsOption.config(state = updateState)

# --------------------------------------
# SET UP ROOT
# --------------------------------------
root = Tk()
root.title(f"Guitar Hero Demucs Audio Splitter - V{VERSION}")
root.iconbitmap(resource_path('res/icon.ico'))
root.config(bg = BG_COLOR)
root.geometry("640x760")
root.resizable(False, False)

# Update TTK styling.
TTK.Style().configure('TEntry', background = BG_COLOR)
TTK.Style().configure('TButton', background = BG_COLOR)
TTK.Style().configure("TCheckbutton", background = BG_COLOR, foreground = FG_COLOR, font = FONT_INFO)

LOGO_IMAGE = ImageTk.PhotoImage(Image.open(resource_path('res/logo.png')))
LOGO_IMAGE_IMF = ImageTk.PhotoImage(Image.open(resource_path('res/imf_logo.png')))

AV_IMF = ImageTk.PhotoImage(Image.open(resource_path('res/imf24.png')))
AV_OKT = ImageTk.PhotoImage(Image.open(resource_path('res/okt.jpg')))

logoImage = Label(root, bg = BG_COLOR, image = LOGO_IMAGE, justify = 'center', anchor = 'n')
logoImage.pack(pady = 5)

headCredits = Label(root, text = "Made by IMF24, Help from Oktoberfest\nDemucs by Meta Platforms, Inc.\ndrumsep Model by inagoy", bg = BG_COLOR, fg = FG_COLOR, font = FONT_INFO_HEADER, justify = 'center', anchor = 'n')
headCredits.pack(pady = 5)

logoIMF = Label(root, bg = BG_COLOR, image = AV_IMF, justify = 'center')
logoIMF.place(x = 110, y = 85)

logoOkt = Label(root, bg = BG_COLOR, image = AV_OKT, justify = 'center')
logoOkt.place(x = 465, y = 85)



# This frame is where all of our widgets will go.
mainFrame = Frame(root, bg = BG_COLOR)
mainFrame.pack(fill = 'both', expand = 1)

# --------------------------------------
# SETUP OPTIONS, AUDIO FILE PATHS
# --------------------------------------
audioSetupHeader = Label(mainFrame, text = " Audio File Setup: Set up the audio file for how it should be split out.", font = FONT_INFO_HEADER, bg = BG_COLOR, fg = FG_COLOR)
audioSetupHeader.grid(row = 0, column = 0, columnspan = 999, pady = 5, sticky = 'w')

# -------------- Audio File Source -------------- #
audioSourceLabel = Label(mainFrame, text = "Audio Source: ", anchor = 'e', justify = 'right', bg = BG_COLOR, fg = FG_COLOR, width = 15)
audioSourceLabel.grid(row = 1, column = 0, padx = 5, sticky = 'e')

audioSource = TTK.Entry(mainFrame, width = 70)
audioSource.grid(row = 1, column = 1, padx = 5, sticky = 'w')

audioSourcePointPath = TTK.Button(mainFrame, text = '...', width = 3, command = get_audio_source)
audioSourcePointPath.grid(row = 1, column = 2, padx = 5)

audioSourceReset = TTK.Button(mainFrame, text = '\u27F2', width = 3, command = lambda: audioSource.delete(0, END))
audioSourceReset.grid(row = 1, column = 3)

# -------------- Audio Output Path -------------- #
audioOutPathLabel = Label(mainFrame, text = "Output Path: ", anchor = 'e', justify = 'right', bg = BG_COLOR, fg = FG_COLOR, width = 15)
audioOutPathLabel.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = 'e')

audioOutPath = TTK.Entry(mainFrame, width = 70)
audioOutPath.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = 'w')

audioOutPathPointPath = TTK.Button(mainFrame, text = '...', width = 3, command = set_output_dir)
audioOutPathPointPath.grid(row = 2, column = 2, padx = 5, pady = 5)

audioOutPathReset = TTK.Button(mainFrame, text = '\u27F2', width = 3, command = lambda: audioOutPath.delete(0, END))
audioOutPathReset.grid(row = 2, column = 3)

modelDeviceFrame = Frame(mainFrame, bg = BG_COLOR)
modelDeviceFrame.grid(row = 3, column = 0, columnspan = 999, pady = 25)

model = StringVar()
device = StringVar()
audioFormat = StringVar()

# -------------- Splitting Model -------------- #
modelLabel = Label(modelDeviceFrame, text = "Demucs Model: ", bg = BG_COLOR, fg = FG_COLOR, justify = 'right', anchor = 'e')
modelLabel.grid(row = 0, column = 0, padx = 5)

modelSelection = TTK.OptionMenu(modelDeviceFrame, model, *[md[0] for md in DEMUCS_MODELS])
modelSelection.config(width = 25)
modelSelection.grid(row = 0, column = 1, padx = 5)

modelDeviceSpacer = Label(modelDeviceFrame, text = " " * 26, bg = BG_COLOR)
modelDeviceSpacer.grid(row = 0, column = 2)

# -------------- CUDA / CPU -------------- #
deviceLabel = Label(modelDeviceFrame, text = "Job Device: ", bg = BG_COLOR, fg = FG_COLOR, justify = 'right', anchor = 'e')
deviceLabel.grid(row = 0, column = 3, padx = 5)

deviceSelection = TTK.OptionMenu(modelDeviceFrame, device, *[md[0] for md in DEMUCS_DEVICES])
deviceSelection.config(width = 13)
deviceSelection.grid(row = 0, column = 4, padx = 5)

shift = StringVar()
overlap = StringVar()
shift.set("1")
overlap.set("0.25")

shiftValueLabel = Label(mainFrame, text = "Shift Trick: ", bg = BG_COLOR, fg = FG_COLOR, justify = 'right', anchor = 'e')
shiftValueLabel.place(x = 460, y = 160)

shiftValue = TTK.Spinbox(mainFrame, from_ = 0, to = 10, increment = 1, textvariable = shift, width = 5)
shiftValue.place(x = 530, y = 162)

overlapValueLabel = Label(mainFrame, text = "Overlap: ", bg = BG_COLOR, fg = FG_COLOR, justify = 'right', anchor = 'e')
overlapValueLabel.place(x = 460, y = 190)

overlapValue = TTK.Spinbox(mainFrame, from_ = 0.0, to = 1.0, increment = 0.01, textvariable = overlap, width = 5)
overlapValue.place(x = 530, y = 192)

# -------------- Output Options -------------- #
# Use Guitar Hero track names?
useGHNames = BooleanVar()
useGHNamesOption = TTK.Checkbutton(mainFrame, text = "Use Guitar Hero Track Names", onvalue = True, offvalue = False, width = 30, variable = useGHNames)
useGHNamesOption.grid(row = 4, column = 0, columnspan = 2, padx = 40, sticky = 'w')
useGHNames.set(False)

# Split drum tracks?
splitDrums = BooleanVar()
splitDrumsOption = TTK.Checkbutton(mainFrame, text = "Split Drum Track to 4 Tracks", onvalue = True, offvalue = False, width = 30, variable = splitDrums, command = allow_exclude_drums)
splitDrumsOption.grid(row = 5, column = 0, columnspan = 2, padx = 40, pady = 10, sticky = 'w')
splitDrums.set(False)

# Exclude original drum track if 4 tracks are made?
excludeOrigDrums = BooleanVar()
excludeOrigDrumsOption = TTK.Checkbutton(mainFrame, text = "Exclude Full Drum Track", onvalue = True, offvalue = False, width = 30, variable = excludeOrigDrums)
excludeOrigDrumsOption.grid(row = 6, column = 0, columnspan = 2, padx = 40, sticky = 'w')
excludeOrigDrums.set(False)
excludeOrigDrumsOption.config(state = 'disabled')

# -------------- Output Format -------------- #
outputFormatLabel = Label(modelDeviceFrame, text = "Output Format: ", bg = BG_COLOR, fg = FG_COLOR, justify = 'right', anchor = 'e')
outputFormatLabel.grid(row = 1, column = 0, padx = 5, pady = 10)

outputFormatSelection = TTK.OptionMenu(modelDeviceFrame, audioFormat, *[md[0] for md in AUDIO_OUT_TYPES])
outputFormatSelection.config(width = 13)
outputFormatSelection.grid(row = 1, column = 1, padx = 5, pady = 10, sticky = 'w')

beginSplit = TTK.Button(root, text = "Split Audio File", width = 30, command = split_audio)
beginSplit.place(x = 445, y = 728)

# -------------- Program Output Window -------------- #

outputTextHeader = Label(mainFrame, text = " Output Log:", font = FONT_INFO_HEADER, bg = BG_COLOR, fg = FG_COLOR)
outputTextHeader.grid(row = 7, column = 0, columnspan = 999, pady = 5, sticky = 'w')

outputText = Text(mainFrame, relief = 'sunken', bd = 1, width = 106, height = 16, bg = BG_COLOR, fg = FG_COLOR, selectbackground = BG_COLOR, font = FONT_INFO, wrap = 'word')
outputText.grid(row = 8, column = 0, columnspan = 999, sticky = 'w')
outputText.config(state = 'disabled')

# --------------------------------------
# SET TOOLTIPS AND RUN PROGRAM
# --------------------------------------
ToolTip(audioSourceLabel, msg = "The source audio file to split out.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
ToolTip(audioSource, msg = "The source audio file to split out.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
ToolTip(audioSourcePointPath, msg = "Select an audio file on the disk.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
ToolTip(audioSourceReset, msg = "Reset the source audio path.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

ToolTip(audioOutPathLabel, msg = "The destination the files will be saved to.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
ToolTip(audioOutPath, msg = "The destination the files will be saved to.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
ToolTip(audioOutPathPointPath, msg = "Select a destination on the disk.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
ToolTip(audioOutPathReset, msg = "Reset the destination path.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

ToolTip(modelLabel, msg = "Type of pre-trained model that Demucs will use when stemming audio.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
ToolTip(modelSelection, msg = "Type of pre-trained model that Demucs will use when stemming audio.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

ToolTip(deviceLabel, msg = "The device Demucs will use to stem the audio. CUDA will use your graphics card, but if the device has no GPU, then your CPU will be used.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
ToolTip(deviceSelection, msg = "The device Demucs will use to stem the audio. CUDA will use your graphics card, but if the device has no GPU, then your CPU will be used.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

ToolTip(outputFormatLabel, msg = "The type of file Demucs will output.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
ToolTip(outputFormatSelection, msg = "The type of file Demucs will output.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

ToolTip(useGHNamesOption, msg = "Do you want the tracks to be named ready for use in Guitar Hero?", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
ToolTip(splitDrumsOption, msg = "Do you want the drums track split out into individual lane tracks? Uses the drumsep model (not an official Demucs model).", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
ToolTip(excludeOrigDrumsOption, msg = "When using 4 lane drum splitting, do you want to exclude the full drum track from the end result?", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

ToolTip(shiftValueLabel, msg = "The number of random shifts for equivariant stabilization. This increases separation time, but improves the output result.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
ToolTip(shiftValue, msg = "The number of random shifts for equivariant stabilization. This increases separation time, but improves the output result.", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

ToolTip(overlapValueLabel, msg = "Adjust the amount of overlap between prediction windows. 0.25 is default, but it can most likely be reduced to 0.1 to improve speed (not tested!)", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)
ToolTip(overlapValue, msg = "Adjust the amount of overlap between prediction windows. 0.25 is default, but it can most likely be reduced to 0.1 to improve speed (not tested!)", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

ToolTip(beginSplit, msg = "Run Demucs on the given audio track!", delay = HOVER_DELAY, follow = False, width = TOOLTIP_WIDTH)

root.mainloop()