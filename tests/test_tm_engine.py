import pytest
from pathlib import Path
from turinglab import SingleTapeTM, RunResult

YAML_PATH = Path(__file__).parent.parent / "machines" / "binary_increment.yaml"


@pytest.fixture
def tm():
    return SingleTapeTM.from_yaml(YAML_PATH)


def test_binary_increment_1011(tm):
    """1011 + 1 = 1100 olmalı, makine kabul etmeli."""
    result = tm.run("1011")
    assert result.accepted is True
    assert result.final_tape.strip("B") == "1100"


def test_binary_increment_zero(tm):
    """0 + 1 = 1 olmalı."""
    result = tm.run("0")
    assert result.accepted is True
    assert result.final_tape.strip("B") == "1"


def test_binary_increment_all_ones(tm):
    """1111 + 1 = 10000 olmalı (taşma durumu)."""
    result = tm.run("1111")
    assert result.accepted is True
    assert result.final_tape.strip("B") == "10000"


def test_timeout(tm):
    """max_steps=5 ile uzun girdi zaman aşımına uğramalı."""
    result = tm.run("10101010", max_steps=5)
    assert result.accepted is False
    assert result.reason == "timeout"


def test_no_transition():
    """Girdi alfabesinde olmayan sembol no_transition döndürmeli."""
    tm = SingleTapeTM.from_yaml(YAML_PATH)
    result = tm.run("102")
    assert result.accepted is False
    assert result.reason == "no_transition"


def test_invalid_yaml_raises_value_error(tmp_path):
    """Zorunlu alan eksik YAML ValueError fırlatmalı."""
    bad_yaml = tmp_path / "bad.yaml"
    bad_yaml.write_text("name: test\nstates: [q0]\n", encoding="utf-8")
    with pytest.raises(ValueError, match="zorunlu alan"):
        SingleTapeTM.from_yaml(bad_yaml)


def test_history_length(tm):
    """history uzunluğu steps + 1 olmalı."""
    result = tm.run("101")
    assert len(result.history) == result.steps + 1


def test_verbose_output(tm, capsys):
    """verbose=True iken çıktı 'Adım 0' içermeli."""
    tm.run("1", verbose=True)
    captured = capsys.readouterr()
    assert "Adım 0" in captured.out
