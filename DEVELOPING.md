# Developing

## Initial setup

1. Install `just`: https://just.systems/man/en/packages.html
1. `just fetch` to get default `justfile` from https://github.com/adamghill/dotfiles/
1. `just boostrap` to install base tools

## Bump version

1. Update version in `pyproject.toml`
1. Update CHANGELOG.md
1. `just update` to install the package and all extras
1. `just test` to run tests
1. `just docs-build` to build documentation
1. Commit changes
1. Tag commit with new version
1. Push `git push --tags origin main`
1. `just publish`
1. Update [GitHub Releases](https://github.com/adamghill/coltrane/releases/new)
