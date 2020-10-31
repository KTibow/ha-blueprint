import glob
import os
import shutil
from colorama import init, Fore


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
    errors = os.system("flake8 . --select=E9,F63,F7,F82 --show-source --statistics")
    if errors != 0:
        raise Exception("Python is invalid, according to flake8")
    flake8_format = "${blue_bold}%(path)s:%(row)d:${green_bold}%(col)d ${purple_bold}%(code)s${reset} %(text)s"
    flake8_start = (
        "flake8 . --inline-quotes double --count --exit-zero --max-complexity=15"
        + f" --max-line-length=90 --statistics --format '{flake8_format}' "
    )
    lint_categories = {
        "Docstrings": "D,DAR",
        "Small tweaks that might help, but might conflict or be inconvenient": r"WPS323,WPS336,WPS305,WPS420,WPS440,WPS441,WPS515,E800\:,WPS421,W503,WPS412",
        "Trailing commas and isort": "I,C81",
        "Overcomplex code": "WPS214,WPS221,WPS229,WPS226",
        "Useless stuff": "WPS507,F401,WPS504",
        "Bandit": "S",
        "Clarity and quality improvements": "WPS432,WPS110,WPS111,WPS322,E501",
    }
    for name, codes in lint_categories.items():
        startgroup(f"Flake8: {name}")
        os.system(flake8_start + f"--select={codes}")
        endgroup()
    # Small tweaks that might help, but might conflict or be inconvenient:
    # Using print() (wrong function call), try (wrong keyword), explicit string concat,
    # f string, commented out code, and % formatting
    startgroup("Flake8: Everything else")
    os.system(flake8_start + "--ignore=" + ",".join(list(lint_categories.values())))
    endgroup()
    print(Fore.MAGENTA + "Looking for what these warnings mean?")
    print(Fore.MAGENTA + "If it starts with WPS, look here (remove the WPS part first):")
    print(Fore.BLUE + "https://wemake-python-stylegui.de/en/latest/search.html")
    print(Fore.MAGENTA + 'Else just search for it with the keywords "flake8 python".')
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
