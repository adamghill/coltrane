1. `poetry lock && poetry install --extras docs --extras deploy --extras json5 --extras compressor`
1. `poe t`
1. `poetry version major|minor|patch`
1. Update CHANGELOG.md
1. `poe docs`
1. Commit changes
1. Tag commit with new version
1. Push `git push --tags origin main`
1. `poe publish`
1. Update [GitHub Releases](https://github.com/adamghill/coltrane/releases/new)
