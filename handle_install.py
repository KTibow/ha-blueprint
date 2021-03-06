import glob
import os
import shutil
import sys


def startgroup(text):
    print("::group::" + text)
    sys.stdout.flush()


def endgroup():
    print("::endgroup::")
    sys.stdout.flush()


print("\033[34mInstalling dependencies.\033[39m")
sys.stdout.flush()
os.system("python -m pip install --upgrade colorama")

if len(glob.glob("**/*.py", recursive=True)) > 0:
    os.system("sh /home/runner/work/myaction/python_setup.sh")
else:
    print("No python files found, not installing hassfest and flake8.")
if len(glob.glob("**/*.js", recursive=True)) > 0:
    startgroup("ESLint setup")
    os.system("npm install")
    os.system(
        "npm install eslint eslint-formatter-summary typescript @typescript-eslint/parser prettier"
    )
    endgroup()
else:
    print("No JS files found, not installing eslint and prettier.")
