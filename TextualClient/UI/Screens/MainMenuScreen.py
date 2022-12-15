from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Button, Footer, Header


class MainMenuScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        button_id = event.button.id
        if button_id == "sp":
            self.app.push_screen("SinglePlayerMenu")
        if button_id == "mp":
            self.app.push_screen("MultiplayerMenu")
        if button_id == "settings":
            pass
            # self.app.push_screen("") - do we need settings?
        if button_id == "quit":
            self.app.exit()

    def compose(self) -> ComposeResult:
        yield Container(
            Header(),
            Container(
                Button("Singleplayer", id="sp", variant="success"),
                Button("Multiplayer", id="mp", variant="success"),
                Button("Settings", id="settings", variant="warning"),
                Button("Quit", id="quit", variant="error"),
                id="menu-buttons",
            ),
            Footer(),
            id="center_content_container"
        )
