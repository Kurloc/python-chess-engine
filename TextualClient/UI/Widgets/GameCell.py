from textual.widgets import Button


class GameCell(Button):
    """Individual playable cell in the game."""

    @staticmethod
    def at(row: int, col: int) -> str:
        """Get the ID of the cell at the given location.
        Args:
            row (int): The row of the cell.
            col (int): The column of the cell.
        Returns:
            str: A string ID for the cell.
        """
        return f"cell-{row}-{col}"

    def __init__(self, row: int, col: int, label: str) -> None:
        """Initialise the game cell.
        Args:
            row (int): The row of the cell.
            col (int): The column of the cell.
        """
        super().__init__(label=label, id=self.at(row, col))
        self.row = row
        self.col = col
