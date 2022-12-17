from typing import Dict, Callable

from textual.screen import Screen


class ButtonMenuScreen(Screen):
    def __init__(
            self,
            name: str | None = None,
            _id: str | None = None,
            classes: str | None = None
    ):
        super().__init__(name, _id, classes)
