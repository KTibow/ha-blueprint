# ha-blueprint
This is a GitHub Action for advanced Home Assistant CI.
- With formatting (black + isort for python, prettier for js)
- With lint
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
      - uses: hacs/integration/action@main
        with:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          CATEGORY: integration
      - uses: KTibow/ha-blueprint@stable
        name: CI
        with:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```
Some notes:
- Change the CATEGORY to plugin if it's a JS card or plugin instead of an integration.
- Change
```
        with:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```
to
```
        with:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          FORMAT_CODE: DISABLED
```
to disable code formatting.

Here's an example log run: https://github.com/KTibow/ha-blueprint/runs/1244330084?check_suite_focus=true
