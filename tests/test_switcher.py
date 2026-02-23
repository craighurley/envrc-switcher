import subprocess
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path

from envrc_switcher.switcher import switch


@pytest.fixture
def home(tmp_path: Path) -> Path:
    (tmp_path / ".envrc.foo").write_text("export ANTHROPIC_API_KEY=test")
    return tmp_path


def test_copies_config_to_envrc(home: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("envrc_switcher.switcher.subprocess.run", lambda *args, **kwargs: None)
    switch("foo", home)
    assert (home / ".envrc").read_text() == "export ANTHROPIC_API_KEY=test"


def test_runs_direnv_allow(home: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[tuple] = []
    monkeypatch.setattr(
        "envrc_switcher.switcher.subprocess.run",
        lambda *args, **kwargs: calls.append((args, kwargs)),
    )
    switch("foo", home)
    assert calls == [((["direnv", "allow", str(home)],), {"check": True, "capture_output": True})]


def test_warns_when_direnv_not_found(
    home: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    def raise_not_found(*args, **kwargs):
        raise FileNotFoundError

    monkeypatch.setattr("envrc_switcher.switcher.subprocess.run", raise_not_found)
    switch("foo", home)
    assert "direnv not found" in capsys.readouterr().out


def test_warns_on_direnv_error(
    home: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    def raise_process_error(*args, **kwargs):
        raise subprocess.CalledProcessError(1, "direnv", stderr=b"permission denied")

    monkeypatch.setattr("envrc_switcher.switcher.subprocess.run", raise_process_error)
    switch("foo", home)
    assert "direnv allow failed" in capsys.readouterr().out


def test_raises_on_permission_error(home: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def raise_permission_error(*args, **kwargs):
        raise PermissionError("denied")

    monkeypatch.setattr("envrc_switcher.switcher.shutil.copy2", raise_permission_error)
    with pytest.raises(PermissionError, match="Cannot write to"):
        switch("foo", home)
