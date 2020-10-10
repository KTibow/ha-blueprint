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
    prettier_ignore_existed = ".prettierignore" in "".join(glob.glob("**/*", recursive=True))
    prev_ignore = ""
    if prettier_ignore_existed:
        prev_ignore = open(".prettierignore", "r").read()
        with open(".prettierignore", "a") as prettier_ignore:
            prettier_ignore.write("\ndist/")
    else:
        with open(".prettierignore", "w") as prettier_ignore:
            prettier_ignore.write("dist/\n")
    os.system("npx prettier --write **/*.{js,ts}")
    if prettier_ignore_existed:
        with open(".prettierignore", "w") as prettier_ignore:
            prettier_ignore.write(prev_ignore)
    else:
        os.remove(".prettierignore")
    endgroup()
else:
    print("No JS files found, not running prettier.")
