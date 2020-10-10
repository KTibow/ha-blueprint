import glob
import os
import shutil


def startgroup(text):
    os.system("echo ::group::" + text)


def endgroup():
    os.system("echo ::endgroup::")


if len(glob.glob("**/*.py", recursive=True)) > 0:
    startgroup("Hassfest")
    os.system("echo hey1")
    os.system(
        """docker run --name hassfest_instance --workdir /github/workspace --rm """
        + """-e pythonLocation -e INPUT_GITHUB_TOKEN -e INPUT_CATEGORY -e HOME -e GITHUB_JOB -e GITHUB_REF -e GITHUB_SHA -e GITHUB_REPOSITORY """
        + """-e ACTIONS_RUNTIME_TOKEN -e ACTIONS_CACHE_URL -e GITHUB_ACTIONS=true -e CI=true -v "/var/run/docker.sock":"/var/run/docker.sock" """
        + """-v "/home/runner/work/_temp/_github_home":"/github/home" -v "/home/runner/work/_temp/_github_workflow":"/github/workflow" """
        + """-v "/home/runner/work/_temp/_runner_file_commands":"/github/file_commands" -v "/home/runner/work/blueprinttest/blueprinttest":"/github/workspace" hassfest"""
    )
    #    """-e GITHUB_REPOSITORY_OWNER -e GITHUB_RUN_ID -e GITHUB_RUN_NUMBER -e GITHUB_RETENTION_DAYS -e GITHUB_ACTOR -e GITHUB_WORKFLOW -e GITHUB_HEAD_REF """ +
    #    """-e GITHUB_BASE_REF -e GITHUB_EVENT_NAME -e GITHUB_SERVER_URL -e GITHUB_API_URL -e GITHUB_GRAPHQL_URL -e GITHUB_WORKSPACE -e GITHUB_ACTION """ +
    #    """-e GITHUB_EVENT_PATH -e GITHUB_PATH -e GITHUB_ENV -e RUNNER_OS -e RUNNER_TOOL_CACHE -e RUNNER_TEMP -e RUNNER_WORKSPACE -e ACTIONS_RUNTIME_URL """ +
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
