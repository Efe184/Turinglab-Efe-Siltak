import pytest
from pathlib import Path
from turinglab import SingleTapeTM

MACHINES = Path(__file__).parent.parent / "machines"


@pytest.fixture
def unary():
    return SingleTapeTM.from_yaml(MACHINES / "unary_to_binary.yaml")


@pytest.fixture
def compare():
    return SingleTapeTM.from_yaml(MACHINES / "binary_compare.yaml")


@pytest.fixture
def copy():
    return SingleTapeTM.from_yaml(MACHINES / "string_copy.yaml")


@pytest.fixture
def paren():
    return SingleTapeTM.from_yaml(MACHINES / "student_choice.yaml")


# ── TM-1: Unary → Binary ──────────────────────────────────────────────────

def test_unary_accept_three(unary):
    """'111' unary 3'u temsil eder; binary karsiligi '11' olmali."""
    r = unary.run("111", max_steps=10000)
    assert r.accepted is True
    assert r.final_tape.strip("B") == "11"


def test_unary_accept_seven(unary):
    """'1111111' unary 7; binary karsiligi '111' olmali."""
    r = unary.run("1111111", max_steps=50000)
    assert r.accepted is True
    assert r.final_tape.strip("B") == "111"


def test_unary_reject_timeout(unary):
    """max_steps=3 ile uzun girdi zaman asimina ugramali."""
    r = unary.run("1111111", max_steps=3)
    assert r.accepted is False
    assert r.reason == "timeout"


def test_unary_reject_no_transition(unary):
    """Girdi alfabesinde olmayan '0' no_transition vermeli."""
    r = unary.run("10")
    assert r.accepted is False
    assert r.reason == "no_transition"


def test_unary_edge_empty(unary):
    """Bos girdi binary '0' olarak kabul edilmeli."""
    r = unary.run("", max_steps=10)
    assert r.accepted is True
    assert r.final_tape.strip("B") == "0"


# ── TM-2: Binary Compare ─────────────────────────────────────────────────

def test_compare_accept_greater(compare):
    """1100 > 1011 (12 > 11), makine kabul etmeli."""
    r = compare.run("1100#1011", max_steps=50000)
    assert r.accepted is True


def test_compare_accept_one_zero(compare):
    """1 > 0, kabul."""
    r = compare.run("1#0", max_steps=1000)
    assert r.accepted is True


def test_compare_reject_less(compare):
    """1011 < 1100 (11 < 12), ret."""
    r = compare.run("1011#1100", max_steps=50000)
    assert r.accepted is False


def test_compare_reject_equal(compare):
    """101 == 101, ret (esit => kabul degil)."""
    r = compare.run("101#101", max_steps=50000)
    assert r.accepted is False


def test_compare_edge_zero_one(compare):
    """0 < 1, ret."""
    r = compare.run("0#1", max_steps=1000)
    assert r.accepted is False


# ── TM-3: String Copy ────────────────────────────────────────────────────

def test_copy_accept_ab(copy):
    """'ab' -> serit 'ab#ab' olmali."""
    r = copy.run("ab", max_steps=10000)
    assert r.accepted is True
    assert r.final_tape.strip("B") == "ab#ab"


def test_copy_accept_abba(copy):
    """'abba' -> serit 'abba#abba' olmali."""
    r = copy.run("abba", max_steps=50000)
    assert r.accepted is True
    assert r.final_tape.strip("B") == "abba#abba"


def test_copy_reject_timeout(copy):
    """max_steps=5 ile uzun girdi zaman asimina ugramali."""
    r = copy.run("abba", max_steps=5)
    assert r.accepted is False
    assert r.reason == "timeout"


def test_copy_reject_no_transition(copy):
    """Alfabe disindaki 'c' no_transition vermeli."""
    r = copy.run("ac")
    assert r.accepted is False
    assert r.reason == "no_transition"


def test_copy_edge_single(copy):
    """Tek karakter 'a' -> 'a#a' olmali."""
    r = copy.run("a", max_steps=1000)
    assert r.accepted is True
    assert r.final_tape.strip("B") == "a#a"


# ── TM-4: Parantez Denge ─────────────────────────────────────────────────

def test_paren_accept_simple(paren):
    """'()' dengeli, kabul."""
    r = paren.run("()")
    assert r.accepted is True


def test_paren_accept_nested(paren):
    """'(()())' dengeli, kabul."""
    r = paren.run("(()())")
    assert r.accepted is True


def test_paren_reject_open(paren):
    """'(()' kapanis eksik, ret."""
    r = paren.run("(()")
    assert r.accepted is False


def test_paren_reject_close_first(paren):
    """')(' ters sira, ret."""
    r = paren.run(")(")
    assert r.accepted is False


def test_paren_edge_empty(paren):
    """Bos dizi dengeli sayilir, kabul."""
    r = paren.run("")
    assert r.accepted is True
