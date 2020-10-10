import glob
import os
import shutil


def startgroup(text):
    os.system("echo ::group::" + text)


def endgroup():
    os.system("echo ::endgroup::")


if len(glob.glob("**/*.py", recursive=True)) > 0:
    startgroup("Hassfest")
    os.system("echo hey5")
    os.system("echo " + os.getenv("GITHUB_REPOSITORY").split("/")[1].lower())
    os.system(
        """docker run --name hassfest_instance --workdir /github/workspace --rm """
        + """-v "/home/runner/work/blueprinttest/blueprinttest":"/github/workspace" hassfest"""
    )
    endgroup()
    startgroup("Flake8: Unused stuff and docstrings")
    os.system("flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics")
    flake8start = """flake8 . --inline-quotes '"' --count --exit-zero --max-complexity=15 --max-line-length=90 --statistics """
    os.system(flake8start + "--select=D,DAR")
    os.system(flake8start + "--select=F")
    endgroup()
    startgroup("Flake8: Other random stuff")
    os.system(flake8start + "--select=I,P,WPS305,C812,E203,W503,E800")
    os.system(flake8start + "--ignore=I,P,WPS305,C812,E203,W503,E800,D,DAR,F")
    endgroup()
else:
    print("No python files found, not running hassfest and flake8.")
if len(glob.glob("**/*.js", recursive=True)) > 0:
    startgroup("ESLint")
    os.system("npx eslint . -f summary --ext js,ts || true")
    endgroup()
else:
    print("No JS files found, not running eslint.")