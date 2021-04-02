@echo off

:start
cls

python ./get-pip.py

pip install os
pip install requests
pip install urllib.parse
pip install datetime
pip install time
pip install pytz
pip install PySimpleGUI
pip install json

python ./find_vaccines.py
pause
exit