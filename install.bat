@echo off
echo ----------------------------------
echo Setting things up! Be patient, make yourself a cup of tea...
echo ----------------------------------

pip install --upgrade demucs PySoundFile
pip uninstall torch
pip install torch -f https://download.pytorch.org/whl/torch_stable.html

pip install --upgrade tkinter-tooltip
pip install --upgrade Pillow

echo ----------------------------------
echo All done; things should be good to go!
echo ----------------------------------
pause