@echo off
echo ----------------------------------
echo Setting things up! Be patient, make yourself a cup of tea...
echo ----------------------------------

python -m pip install --upgrade demucs PySoundFile
python -m pip uninstall torch
python -m pip install torch -f https://download.pytorch.org/whl/torch_stable.html

python -m pip install --upgrade tkinter-tooltip
python -m pip install --upgrade Pillow

echo ----------------------------------
echo All done; things should be good to go!
echo ----------------------------------
pause