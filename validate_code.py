import glob
import os
import shutil


def startgroup(text):
    os.system("echo ::group::" + text)


def endgroup():
    os.system("echo ::endgroup::")


if len(glob.glob("**/*.py", recursive=True)) > 0:
    startgroup("Hassfest")
    repo_name = os.getenv("GITHUB_REPOSITORY").split("/")[1].lower()
    errors = os.system(
        """docker run --name hassfest_instance --workdir /github/workspace --rm """
        + f"""-v "/home/runner/work/{repo_name}/{repo_name}":"/github/workspace" hassfest"""
    )
    if errors != 0:
        raise Exception("Integration is invalid, according to hassfest")
    endgroup()
    errors = os.system(
        "flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics"
    )
    if errors != 0:
        raise Exception("Python is invalid, according to flake8")
    flake8_format = "${blue_bold}%(path)s:%(row)d:${green_bold}%(col)d ${purple_bold}%(code)s${reset} %(text)s"
    flake8_start = (
        "flake8 . --inline-quotes double --count --exit-zero --max-complexity=15"
        + f" --max-line-length=90 --statistics --format '{flake8_format}' "
    )
    startgroup("Flake8: Docstrings")
    os.system(flake8_start + "--select=D,DAR")
    endgroup()
    startgroup("Flake8: Small tweaks that might help")
    os.system(flake8_start + r"--select=WPS323,WPS420,WPS336,WPS305,E800\:,WPS421")
    # Using print() (wrong function call), try (wrong keyword), explicit string concat,
    # f string, commented out code, and % formatting
    endgroup()
    startgroup("Flake8: Trailing commas and isort")
    os.system(flake8_start + "--select=I,C81")
    endgroup()
    startgroup("Flake8: Overcomplex code")
    os.system(flake8_start + "--select=WPS214,WPS229,WPS226")
    endgroup()
    startgroup("Flake8: Bandit")
    os.system(flake8_start + "--select=S")
    endgroup()
    startgroup("Flake8: Everything else")
    os.system(
        flake8_start
        + "--ignore=D,DAR,WPS323,WPS420,WPS336,WPS305,E800\:,WPS421,I,C81,WPS214,WPS229,WPS226,S"
    )
    endgroup()
else:
    print("No python files found, not running hassfest and flake8.")
if len(glob.glob("**/*.js", recursive=True)) > 0:
    startgroup("ESLint")
    if os.path.isfile(".eslintrc"):
        os.remove(".eslintrc")
    shutil.copyfile(
        "/home/runner/work/myaction/.eslintrc.js",
        ".eslintrc.js",
    )
    errors = os.system("npx eslint . -f summary --quiet --ext js,ts")
    if errors != 0:
        raise Exception("JS is invalid, according to eslint")
    endgroup()
else:
    print("No JS files found, not running eslint.")
