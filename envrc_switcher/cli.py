import argparse
import sys
from pathlib import Path

import questionary

from envrc_switcher.configs import discover_configs
from envrc_switcher.switcher import switch


def get_version() -> str:
    try:
        from importlib.metadata import version

        return version("envrc-switcher")
    except Exception:
        return "0.0.1-dev"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Switch envrc configuration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        color=False,
        epilog="""
Examples:
  %(prog)s
  %(prog)s ~/
  %(prog)s ../
        """,
    )
    parser.add_argument("directory", nargs="?", type=Path, default=None)
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {get_version()}")
    args = parser.parse_args()

    home = args.directory.resolve() if args.directory else Path.cwd()

    if not home.is_dir():
        print(f"Error: {home} is not a directory", file=sys.stderr)
        sys.exit(1)

    configs = discover_configs(home)

    if not configs:
        print(
            "No configs found.\n"
            f"Create config files in {home} named .envrc.<example>, "
            "e.g. .envrc.foo, .envrc.bar"
        )
        sys.exit(1)

    try:
        choice = questionary.select("Select config:", choices=configs).ask()
    except KeyboardInterrupt:
        sys.exit(0)

    if choice is None:
        # User cancelled via questionary (e.g. Ctrl+C handled internally)
        sys.exit(0)

    try:
        switch(choice, home)
        print(f"Switched to config: {choice}")
    except PermissionError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
