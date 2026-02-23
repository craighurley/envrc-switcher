import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from envrc_switcher.cli import main


def _run(
    monkeypatch: pytest.MonkeyPatch, argv: list[str], configs: list[str], choice: str | None = "foo"
) -> None:
    monkeypatch.setattr(sys, "argv", ["envrc-switcher", *argv])
    monkeypatch.setattr("envrc_switcher.cli.discover_configs", lambda _: configs)
    monkeypatch.setattr("envrc_switcher.cli.switch", MagicMock())
    mock_select = MagicMock()
    mock_select.return_value.ask.return_value = choice
    monkeypatch.setattr("envrc_switcher.cli.questionary.select", mock_select)


def test_defaults_to_cwd_when_no_arg(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    captured_home: list[Path] = []

    def capture_discover(home: Path) -> list[str]:
        captured_home.append(home)
        return ["foo"]

    monkeypatch.setattr(sys, "argv", ["envrc-switcher"])
    monkeypatch.setattr("envrc_switcher.cli.discover_configs", capture_discover)
    monkeypatch.setattr("envrc_switcher.cli.switch", MagicMock())
    mock_select = MagicMock()
    mock_select.return_value.ask.return_value = "foo"
    monkeypatch.setattr("envrc_switcher.cli.questionary.select", mock_select)

    main()

    assert captured_home[0] == Path.cwd()


def test_uses_supplied_directory(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    captured_home: list[Path] = []

    def capture_discover(home: Path) -> list[str]:
        captured_home.append(home)
        return ["foo"]

    monkeypatch.setattr(sys, "argv", ["envrc-switcher", str(tmp_path)])
    monkeypatch.setattr("envrc_switcher.cli.discover_configs", capture_discover)
    monkeypatch.setattr("envrc_switcher.cli.switch", MagicMock())
    mock_select = MagicMock()
    mock_select.return_value.ask.return_value = "foo"
    monkeypatch.setattr("envrc_switcher.cli.questionary.select", mock_select)

    main()

    assert captured_home[0] == tmp_path.resolve()


def test_exits_on_nonexistent_directory(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    monkeypatch.setattr(sys, "argv", ["envrc-switcher", "/no/such/directory"])

    with pytest.raises(SystemExit) as exc:
        main()

    assert exc.value.code == 1
    assert "is not a directory" in capsys.readouterr().err


def test_exits_on_file_path(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    f = tmp_path / "somefile"
    f.write_text("x")
    monkeypatch.setattr(sys, "argv", ["envrc-switcher", str(f)])

    with pytest.raises(SystemExit) as exc:
        main()

    assert exc.value.code == 1
    assert "is not a directory" in capsys.readouterr().err
