# ha-blueprint
This is a GitHub Action for advanced Home Assistant CI:
- With formatting (black + isort for python, prettier for js)
- With lint (ESLint for js, wemake-python-styleguide with flake8 for python)

Thanks [https://github.com/custom-components/blueprint] for the blueprint.
Add this file to `.github/workflows/combined.yaml`:
```
name: "Custom Component CI"
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
      - uses: KTibow/ha-blueprint@main
        name: CI
        with:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```
Some notes:
- Change the CATEGORY to plugin if it's a JS card or plugin instead of an integration.
