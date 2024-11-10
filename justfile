import? 'adamghill.justfile'
import? '../dotfiles/just/justfile'

# Grab default `adamghill.justfile` from GitHub
fetch:
  curl https://raw.githubusercontent.com/adamghill/dotfiles/master/just/justfile > adamghill.justfile

src := "coltrane"

install:
  just sync
  uv pip install .[docs, deploy, json5, compressor, angles, unicorn]

serve:
  uv run --all-extras python3 example_standalone/app.py runserver 0:8045

serve-integrated:
  uv run --all-extras python3 example_integrated/app.py runserver 0:8046

serve-prod:
  uv run --all-extras gunicorn -b localhost:8045 example_standalone.app:wsgi
