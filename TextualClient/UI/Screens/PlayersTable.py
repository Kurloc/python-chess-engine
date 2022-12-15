import abc

from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label
from ChessEngine.Debugging.setup_logger import kce_exception_logger

class PlayersTable(Screen):
    def __init__(
            self,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        yield Container(
            Header(),
            Container(
                # headers
                Label("Player Name", classes='table-cell headers'),
                Label("IP Address", classes='table-cell headers'),
                Label("Actions", classes='table-cell headers'),

                # row 1
                Label("Player 1", classes='table-cell row-1'),
                Label("127.0.0.1", classes='table-cell row-1'),
                Label("", classes='table-cell row-1'),

                # row 2
                Label("Player 2", id='player-two-name', classes='table-cell row-2'),
                Label("127.0.0.1", id='player-two-address', classes='table-cell row-2'),
                Button("Kick", id='player-two-kick-player', variant="warning", classes='table-cell row-2'),
                id='player-table-container'
            ),
            Container(
                Button("Back", id="go-back", variant="warning", classes='player-table-footer-button'),
                Label(),
                Button("Start Game", id="start-game", variant="success", classes='player-table-footer-button'),
                id='player-table-buttons-container'
            ),
            Footer()
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'player-two-kick-player':
            kce_exception_logger.info('Kick player event detected')
            kce_exception_logger.info(event)
            kce_exception_logger.info('\n')
            self.kick_player_two()

    def kick_player_two(self):
        self.on_player_two_leave()
        pass

    def on_player_two_join(self, player_name: str, player_address: str):
        skip_label_updates = False
        if player_name is None or player_address is None or player_name == '' or player_address == '':
            skip_label_updates = True

        player_two_name_label = self.query_one('#player-two-name', Label)
        player_two_name_address = self.query_one('#player-two-address', Label)
        player_two_name_kick_button = self.query_one('#player-two-kick-player', Button)
        if not skip_label_updates:
            player_two_name_label.update(player_name)
            player_two_name_address.update(player_address)

        player_two_name_label.styles.visibility = 'visible'
        player_two_name_address.styles.visibility = 'visible'
        player_two_name_kick_button.styles.visibility = 'visible'

    def on_player_two_leave(self):
        player_two_name_label = self.query_one('#player-two-name', Label)
        player_two_name_address = self.query_one('#player-two-address', Label)
        player_two_name_kick_button = self.query_one('#player-two-kick-player', Button)

        player_two_name_label.styles.visibility = 'hidden'
        player_two_name_address.styles.visibility = 'hidden'
        player_two_name_kick_button.styles.visibility = 'hidden'


class TextualGameHostingEventBus:
    players_table: PlayersTable

    def on_player_join(self, player_name: str, player_address):
        self.players_table.on_player_two_join(player_name, player_address)

    def on_player_leave(self):
        self.players_table.on_player_two_leave()
