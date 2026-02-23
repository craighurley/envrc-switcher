# envrc-switcher

CLI tool (`envrc-switcher`) that switches envrc file by copying `.envrc.<example>` to `.envrc` in the current directory (or a specified directory) and running `direnv allow`.

## Architecture

Three modules with a single responsibility each:

- `envrc_switcher/configs.py` — discovers configs by globbing `~/.envrc.*`
- `envrc_switcher/switcher.py` — copies the selected file and calls `direnv allow`
- `envrc_switcher/cli.py` — presents the questionary menu and wires the two together

Config names are derived using `Path.suffix.lstrip(".")`, so `.envrc.foo` → `foo`. Multi-segment suffixes like `.envrc.my.thing` would yield `thing`, not `my.thing` — avoid dots in config names.

## Gotchas

**Config discovery uses `home` as a parameter, not `Path.home()`** — `cli.py` resolves `Path.home()` and passes it in. Tests inject a `tmp_path` fixture. Do not call `Path.home()` inside `configs.py` or `switcher.py`.

**`direnv allow` takes a directory, not a file** — `subprocess.run(["direnv", "allow", str(home)])` is correct. Passing the `.envrc` path directly would fail silently or error depending on direnv version.

**`direnv` errors are non-fatal** — `_run_direnv_allow` warns and continues because the file copy has already succeeded. This is intentional; do not convert these to raised exceptions.

## Development

### Commands

This project uses Taskfile instead of Make.

```shell
# Format
task format

# Lint
task lint

# Run tests
task test
```

Run without installing (from project root)

```shell
python -m envrc_switcher
```
