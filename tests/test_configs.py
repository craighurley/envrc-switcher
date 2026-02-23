from typing import TYPE_CHECKING

from envrc_switcher.configs import discover_configs

if TYPE_CHECKING:
    from pathlib import Path


def test_returns_empty_when_no_configs(tmp_path: Path) -> None:
    assert discover_configs(tmp_path) == []


def test_discovers_single_config(tmp_path: Path) -> None:
    (tmp_path / ".envrc.foo").write_text("export foobar=foo")
    assert discover_configs(tmp_path) == ["foo"]


def test_discovers_multiple_configs_sorted(tmp_path: Path) -> None:
    (tmp_path / ".envrc.bar").write_text("export foobar=bar")
    (tmp_path / ".envrc.foo").write_text("export foobar=foo")
    assert discover_configs(tmp_path) == ["bar", "foo"]


def test_ignores_directories(tmp_path: Path) -> None:
    (tmp_path / ".envrc.foo").mkdir()
    assert discover_configs(tmp_path) == []


def test_ignores_plain_envrc(tmp_path: Path) -> None:
    (tmp_path / ".envrc").write_text("export barfoo=oof")
    (tmp_path / ".envrc.foo").write_text("export foobar=foo")
    assert discover_configs(tmp_path) == ["foo"]
