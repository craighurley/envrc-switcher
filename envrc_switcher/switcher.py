import shutil
import subprocess
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def switch(config: str, home: Path) -> None:
    """Copy .envrc.<config> to .envrc and run direnv allow."""
    source = home / f".envrc.{config}"
    dest = home / ".envrc"

    try:
        shutil.copy2(source, dest)
    except PermissionError as e:
        raise PermissionError(f"Cannot write to {dest}: {e}") from e

    _run_direnv_allow(home)


def _run_direnv_allow(home: Path) -> None:
    try:
        subprocess.run(["direnv", "allow", str(home)], check=True, capture_output=True)
    except FileNotFoundError:
        print("Warning: direnv not found on PATH - config file copied but not activated")
    except subprocess.CalledProcessError as e:
        print(f"Warning: direnv allow failed: {e.stderr.decode().strip()}")
