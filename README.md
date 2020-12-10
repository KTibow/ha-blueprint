# ha-blueprint
This is a GitHub Action for advanced Home Assistant CI. Whenever you push to your repo, this will happen:
- It'll format it (black + isort for python, prettier for js)
  - It'll go ahead and pull it, format it, and amend the changes to the last commit.
- It'll lint it
  - JS: Run ESLint to catch syntax errors
  - Python: It runs Hassfest (to catch invalid integrations), HACS (to catch invalid HACS integrations), and flake8 (to catch invalid python).

Thanks [https://github.com/custom-components/blueprint] for the blueprint.
Add this file to `.github/workflows/combined.yaml`:
```
name: "Validation And Formatting"
on:
  push:
  pull_request:
  schedule:
    - cron: '0 0 * * *'
jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
        name: Download repo
        with:
          fetch-depth: 0
      - uses: actions/setup-python@v2
        name: Setup Python
      - uses: actions/cache@v2
        name: Cache
        with:
          path: |
            ~/.cache/pip
          key: custom-component-ci
      - uses: hacs/action@main
        with:
          CATEGORY: integration
      - uses: KTibow/ha-blueprint@stable
        name: CI
        with:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```
## Some notes:
- Change the CATEGORY to plugin if it's a JS card or plugin instead of an integration.
- Remove this block to disable HACS validation:
```
      - uses: hacs/action@main
        with:
          CATEGORY: integration
```
- Change
```
      - uses: KTibow/ha-blueprint@stable
        name: CI
        with:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```
to
```
      - uses: KTibow/ha-blueprint@stable
        name: CI
        with:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          FORMAT_CODE: DISABLED
```
to disable code formatting.

Here's an example log run: https://github.com/KTibow/ha-blueprint/runs/1244330084?check_suite_focus=true

<details><summary>you don't need to click and expand this</summary>

need a badge? no worries.  
https://img.shields.io/github/workflow/status/KTibow/ha-blueprint/Validation%20And%20Formatting?logoColor=white&label=way%20too%20much%20validation&logo=github-actions&style=flat-square&logoWidth=25&labelColor=black  
  
change `KTibow/ha-blueprint/Validation%20And%20Formatting` to the name of your repo and workflow.  
  
link back in markdown if you want.  

give me a thanks [here](https://saythanks.io/to/kendell.r%40outlook.com)  
  
give me a heart [here](https://community.home-assistant.io/t/235041?u=ktibow)  

or just give me a star  

i'm going to assume you've done that and thank you for letting me know that this is a worthwile thing.  

</details>
