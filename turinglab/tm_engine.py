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
