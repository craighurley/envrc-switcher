# envrc-switcher

Switch between different .envrc files using an interactive menu.

## How it works

Create a envrc file in your home directory for each configuration, named `.envrc.<example>`. Running `envrc-switcher` presents an arrow-key menu of available configs. Selecting one copies that file to `~/.envrc` and runs `direnv allow` to activate it.

## Installation

Install from PyPi:

```shell
pip install -U envrc-switcher
```

Alternatively you can run directly using `uvx`:

```shell
uvx envrc-switcher
```

## Setup

**1. Create config files** in `~/`:

```sh
# ~/.envrc.foo
export foobar=foo
export foo=foo

# ~/.envrc.bar
export foobar=bar
export bar=bar
```

Config names are derived from the file suffix, so `.envrc.foo` appears as `foo` in the menu.

**2. Ensure direnv is installed and configured** to load `~/.envrc`:

```sh
brew install direnv
# Add 'eval "$(direnv hook zsh)"' to ~/.zshrc
```

## Usage

```sh
envrc-switcher [directory]
```

The optional `directory` argument specifies where to look for `.envrc.*` files. Defaults to the current directory.

```
? Select config:
> foo
  bar
```

After selecting, `.envrc` in the target directory is updated and `direnv allow` is run. Open a new shell or run `direnv reload` if the environment does not update immediately.

## Requirements

- Python 3.14+
- [direnv](https://direnv.net)
