from typing import Dict, Callable

from textual.screen import Screen


class ButtonMenuScreen(Screen):
    _screens: Dict[str, Callable[[], Screen]] = None

    def __init__(
            self,
            screens: Dict[str, Callable[[...], Screen]],
            name: str | None = None,
            _id: str | None = None,
            classes: str | None = None
    ):
        super().__init__(name, _id, classes)
        self._screens = screens
