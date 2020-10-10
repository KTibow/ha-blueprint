import glob
import os
import shutil


def startgroup(text):
    os.system("echo ::group::" + text)


def endgroup():
    os.system("echo ::endgroup::")


if len(glob.glob("**/*.py", recursive=True)) > 0:
    startgroup("Python format")
    os.system("sh /home/runner/work/_actions/KTibow/ha-blueprint/main/python_format.sh")
    endgroup()
else:
    print("No python files found, not running isort and black.")
if len(glob.glob("**/*.js", recursive=True)) > 0:
    startgroup("JS format")
    os.system("npx prettier --write")
    endgroup()
else:
    print("No JS files found, not running prettier.")
