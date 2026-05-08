from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
import yaml


@dataclass
class Configuration:
    """Tek bir adımın anlık görüntüsü.

    Attributes:
        state: O anki durum adı.
        tape: O anki şerit içeriği (string olarak).
        head_position: Okuma/yazma kafasının pozisyonu.
    """
    state: str
    tape: str
    head_position: int


@dataclass
class RunResult:
    """Bir çalıştırmanın sonucu.

    Attributes:
        accepted: Makine kabul durumuna ulaştıysa True.
        reason: Sonlanma nedeni: 'accept', 'no_transition', 'timeout', 'head_out_of_bounds'.
        final_tape: Son şerit içeriği.
        steps: Toplam adım sayısı.
        history: Her adımdaki Configuration listesi.
    """
    accepted: bool
    reason: str
    final_tape: str
    steps: int
    history: list[Configuration] = field(default_factory=list)


class Tape:
    """Turing makinesi şeridi. Sparse dict[int, str] olarak temsil edilir."""

    def __init__(self, input_string: str, blank: str = "B"):
        """Şeridi başlat.

        Args:
            input_string: Başlangıç içeriği, 0. pozisyondan itibaren yazılır.
            blank: Boş hücre sembolü.
        """
        self.blank = blank
        self._cells: dict[int, str] = {}
        for i, ch in enumerate(input_string):
            self._cells[i] = ch

    def read(self, pos: int) -> str:
        """Verilen pozisyondaki sembolü oku.

        Args:
            pos: Şerit pozisyonu (negatif olabilir).

        Returns:
            O pozisyondaki sembol; yazılmamışsa blank döner.
        """
        return self._cells.get(pos, self.blank)

    def write(self, pos: int, symbol: str) -> None:
        """Verilen pozisyona sembol yaz.

        Args:
            pos: Şerit pozisyonu.
            symbol: Yazılacak sembol.
        """
        self._cells[pos] = symbol

    def get_tape_str(self, blank: str | None = None) -> str:
        """Şeridin yazılı kısmını string olarak döndür.

        Args:
            blank: Kullanılacak boş sembol; None ise self.blank kullanılır.

        Returns:
            Minimum ve maksimum yazılı pozisyon arasındaki semboller.
        """
        b = blank if blank is not None else self.blank
        if not self._cells:
            return b
        lo = min(self._cells)
        hi = max(self._cells)
        return "".join(self._cells.get(i, b) for i in range(lo, hi + 1))


class SingleTapeTM:
    """Tek şeritli deterministik Turing makinesi."""

    def __init__(
        self,
        states: list[str],
        input_alphabet: list[str],
        tape_alphabet: list[str],
        blank: str,
        start_state: str,
        accept_states: list[str],
        reject_states: list[str],
        transitions: dict[tuple[str, str], tuple[str, str, str]],
    ):
        """Makinenin iç durumunu sakla.

        Args:
            states: Tüm durum adları.
            input_alphabet: Girdi alfabesi.
            tape_alphabet: Şerit alfabesi (blank dahil).
            blank: Boş sembol.
            start_state: Başlangıç durumu.
            accept_states: Kabul durumları listesi.
            reject_states: Ret durumları listesi.
            transitions: (durum, sembol) -> (yaz, yön, yeni_durum) eşlemesi.
        """
        self.states = states
        self.input_alphabet = input_alphabet
        self.tape_alphabet = tape_alphabet
        self.blank = blank
        self.start_state = start_state
        self.accept_states = accept_states
        self.reject_states = reject_states
        self.transitions = transitions

    @classmethod
    def from_yaml(cls, path: str | Path) -> "SingleTapeTM":
        """YAML dosyasından makine yükle.

        Args:
            path: YAML dosyasının yolu.

        Returns:
            Yüklenen SingleTapeTM örneği.

        Raises:
            ValueError: Zorunlu alan eksik veya hatalıysa.
        """
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)

        required = ["states", "input_alphabet", "tape_alphabet", "blank",
                    "start_state", "accept_states", "transitions"]
        for field_name in required:
            if field_name not in data:
                raise ValueError(f"YAML'da zorunlu alan eksik: '{field_name}'")

        raw_tr = data["transitions"]
        if not isinstance(raw_tr, dict):
            raise ValueError("'transitions' bir dict olmalıdır.")

        transitions: dict[tuple[str, str], tuple[str, str, str]] = {}
        for state, sym_map in raw_tr.items():
            if not isinstance(sym_map, dict):
                raise ValueError(f"Durum '{state}' için transitions dict olmalıdır.")
            for symbol, action in sym_map.items():
                if not isinstance(action, list) or len(action) != 3:
                    raise ValueError(
                        f"Geçiş ({state}, {symbol}) için [yaz, yön, yeni_durum] listesi bekleniyor."
                    )
                transitions[(str(state), str(symbol))] = (
                    str(action[0]), str(action[1]), str(action[2])
                )

        reject_states = data.get("reject_states", []) or []

        return cls(
            states=data["states"],
            input_alphabet=data["input_alphabet"],
            tape_alphabet=data["tape_alphabet"],
            blank=str(data["blank"]),
            start_state=str(data["start_state"]),
            accept_states=data["accept_states"],
            reject_states=reject_states,
            transitions=transitions,
        )
