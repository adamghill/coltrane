import? 'adamghill.justfile'
import? '../dotfiles/just/justfile'

src := "src/coltrane"

# List commands
_default:
    just --list --unsorted --justfile {{ justfile() }} --list-heading $'Available commands:\n'

# Grab default `adamghill.justfile` from GitHub
fetch:
  curl https://raw.githubusercontent.com/adamghill/dotfiles/master/just/justfile > adamghill.justfile

serve:
  uv run --all-extras python3 example_standalone/app.py runserver 0:8045

serve-integrated:
  uv run --all-extras python3 example_integrated/app.py runserver 0:8046

serve-sites:
  uv run --all-extras python3 example_sites_standalone/sites/app.py runserver 0:8047

serve-multi-sites:
  echo "8050 8051" | xargs -n 1 -P 2 -I {} uv run --all-extras python3 example_multiple_sites/sites/app.py runserver 0:{}

serve-prod:
  uv run --all-extras gunicorn -b localhost:8045 example_standalone.app:wsgi
