from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def discover_configs(home: Path) -> list[str]:
    """Return sorted config names from $HOME/.envrc.* files."""
    configs = [p.suffix.removeprefix(".") for p in home.glob(".envrc.*") if p.is_file()]
    return sorted(configs)
