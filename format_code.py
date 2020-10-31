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


if os.getenv("FORMAT_CODE") != "DISABLED":
    startgroup("Pulling code")
    os.system("sh /home/runner/work/myaction/pull_code.sh")
    endgroup()
    if len(glob.glob("**/*.py", recursive=True)) > 0:
        startgroup("Python format")
        os.system("sh /home/runner/work/myaction/python_format.sh")
        endgroup()
    else:
        print("No python files found, not running isort and black.")
    if len(glob.glob("**/*.js", recursive=True)) > 0:
        startgroup("JS format")
        prettier_ignore_existed = ".prettierignore" in "".join(
            glob.glob("**/*", recursive=True)
        )
        prev_ignore = ""
        if prettier_ignore_existed:
            prev_ignore = open(".prettierignore", "r").read()
            with open(".prettierignore", "a") as prettier_ignore:
                prettier_ignore.write("\ndist\n*.config.js/")
        else:
            with open(".prettierignore", "w") as prettier_ignore:
                prettier_ignore.write("dist/\n*.config.js\n")
        os.system("npx prettier --write **/*.{js,ts}")
        if prettier_ignore_existed:
            with open(".prettierignore", "w") as prettier_ignore:
                prettier_ignore.write(prev_ignore)
        else:
            os.remove(".prettierignore")
        endgroup()
    else:
        print("No JS files found, not running prettier.")
    startgroup("Pushing code")
    os.system("sh /home/runner/work/myaction/push_code.sh")
    endgroup()
else:
    print("Formatting disabled, not running anything.")
