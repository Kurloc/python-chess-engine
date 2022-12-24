import traceback

from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label
from ChessEngine.Debugging.setup_logger import kce_exception_logger
from TextualClient.Sockets.PlayerLobby import PlayerLobby
from TextualClient.Sockets.PlayerManagement import PlayerManagement
from TextualClient.UI.Enums.ScreenKeys import ScreenKeys


class PlayersTable(Screen):
    __player_management: PlayerManagement

    def __init__(
            self,
            player_management: PlayerManagement
    ):
        super().__init__()
        self.__player_management = player_management

    def compose(self) -> ComposeResult:
        yield Container(
            Header(),
            Container(
                # headers
                Label("Player Name", classes='table-cell headers'),
                Label("IP Address", classes='table-cell headers'),
                Label("Actions", classes='table-cell headers'),

                # row 1
                Label("Player 1", id='player-one-name', classes='table-cell row-1'),
                Label("127.0.0.1", id='player-one-address', classes='table-cell row-1'),
                Label("", id='player-one-kick-player', classes='table-cell row-1'),

                # row 2
                Label(
                    "Player 2",
                    id='player-two-name',
                    classes='table-cell row-2 hidden-player'
                ),
                Label(
                    "127.0.0.1",
                    id='player-two-address',
                    classes='table-cell row-2 hidden-player'
                ),
                Button(
                    id='player-two-kick-player',
                    label="Kick",
                    variant="warning",
                    classes='table-cell row-2 hidden-player'
                ),
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

    def on_mount(self) -> None:
        self.__on_player_two_leave()
        self.__player_management \
            .player_lobby \
            .subscribe(lambda pl: self.update_from_player_lobby(pl))

        player_lobby = self.__player_management.player_lobby.value
        player_lobby.players.pop('1', None)
        self.__player_management.player_lobby.on_next(player_lobby)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case 'go-back':
                self.__player_management.end_lobby.on_next(True)
                self.app.push_screen(ScreenKeys.MAIN_MENU)
            case 'player-two-kick-player':
                kce_exception_logger.info('Kick player event detected')
                kce_exception_logger.info(event)
                kce_exception_logger.info('\n')
                self.__kick_player_two()

    def update_from_player_lobby(self, player_lobby: PlayerLobby):
        if player_lobby is None:
            return

        try:
            host_player = player_lobby.players.get('0')
            client_player = player_lobby.players.get('1')

            player_one_name_label = self.query_one('#player-one-name', Label)
            player_one_name_address = self.query_one('#player-one-address', Label)
            player_one_kick_button = self.query_one('#player-one-kick-player', Label)
            player_one_name_label.update(str(host_player.name))
            player_one_name_address.update(str(host_player.address))

            if host_player.is_local_player:
                player_one_name_label.add_class('local-player')
                player_one_name_address.add_class('local-player')
                player_one_kick_button.add_class('local-player')
                kce_exception_logger.info('host is local player!')
            else:
                player_one_name_label.remove_class('local-player')
                player_one_name_address.remove_class('local-player')
                player_one_kick_button.remove_class('local-player')

                kce_exception_logger.info('host is not local player!')

            if client_player is None:
                self.__on_player_two_leave()
            else:
                self.__on_player_two_join(
                    client_player.name,
                    client_player.address,
                    client_player.is_local_player
                )
        except Exception as e:
            tb = traceback.format_exc()
            kce_exception_logger.exception(e)
            kce_exception_logger.warning(tb)

    def __kick_player_two(self):
        self.__player_management.kick_player.on_next('1')

    def __on_player_two_join(
            self,
            player_name: str,
            player_address: str,
            is_local_player: bool
    ):
        skip_label_updates = False
        if player_name is None or player_address is None or player_name == '' or player_address == '':
            skip_label_updates = True

        player_two_name_label = self.query_one('#player-two-name', Label)
        player_two_name_address = self.query_one('#player-two-address', Label)
        player_two_name_kick_button = self.query_one('#player-two-kick-player', Button)
        start_game_button = self.query_one('#start-game', Button)
        if not skip_label_updates:
            player_two_name_label.update(player_name)
            player_two_name_address.update(player_address)

        if is_local_player:
            player_two_name_label.add_class('local-player')
            player_two_name_address.add_class('local-player')
            player_two_name_kick_button.label = 'Ready'
            player_two_name_kick_button.variant = 'success'
            start_game_button.styles.visibility = 'hidden'
        else:
            player_two_name_label.remove_class('local-player')
            player_two_name_address.remove_class('local-player')
            player_two_name_kick_button.label = 'Kick'
            player_two_name_kick_button.variant = 'warning'
            start_game_button.styles.visibility = 'visible'

        player_two_name_label.styles.visibility = 'visible'
        player_two_name_address.styles.visibility = 'visible'
        player_two_name_kick_button.styles.visibility = 'visible'

    def __on_player_two_leave(self):
        player_two_name_label = self.query_one('#player-two-name', Label)
        player_two_name_address = self.query_one('#player-two-address', Label)
        player_two_name_kick_button = self.query_one('#player-two-kick-player', Button)

        player_two_name_label.styles.visibility = 'hidden'
        player_two_name_address.styles.visibility = 'hidden'
        player_two_name_kick_button.styles.visibility = 'hidden'
