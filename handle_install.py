import glob
import os
import shutil


def startgroup(text):
    os.system("echo ::group::" + text)


def endgroup():
    os.system("echo ::endgroup::")


if len(glob.glob("**/*.py", recursive=True)) > 0:
    os.system("sh /home/runner/work/_actions/KTibow/ha-blueprint/main/python_setup.sh")
else:
    print("No python files found, not running hassfest and flake8.")
if len(glob.glob("**/*.js", recursive=True)) > 0:
    startgroup("ESLint setup")
    os.system("npm install")
    os.system("npm install eslint eslint-formatter-summary prettier")
    endgroup()
else:
    print("No JS files found, not running eslint.")
