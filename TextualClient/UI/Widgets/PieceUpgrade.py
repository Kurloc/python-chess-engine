from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import Reactive
from textual.widget import Widget
from textual.widgets import Label, Button

from ChessEngine.Pieces.ChessPieces import ChessPieces
from TextualClient.Sockets.PlayerManagement import PlayerManagement


class PieceUpgrade(Widget):
    """Widget to tell the user they have won."""
    __player_management: PlayerManagement
    selected_piece = Reactive('none')

    def __init__(
            self,
            _id: str,
            player_management: PlayerManagement
    ):
        super().__init__(id=_id)
        self.__player_management = player_management

    def on_button_pressed(self, event: Button.Pressed) -> None:
        # """Event handler called when a button is pressed."""
        button_id = event.button.id
        if button_id in ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']:
            self.selected_piece = event.button.id

        if button_id == 'confirm_button':
            match self.selected_piece:
                case 'none':
                    self.__player_management.piece_selection.on_next(ChessPieces.NONE)
                case 'pawn':
                    self.__player_management.piece_selection.on_next(ChessPieces.PAWN)
                case 'rook':
                    self.__player_management.piece_selection.on_next(ChessPieces.ROOK)
                case 'bishop':
                    self.__player_management.piece_selection.on_next(ChessPieces.BISHOP)
                case 'knight':
                    self.__player_management.piece_selection.on_next(ChessPieces.KNIGHT)
                case 'queen':
                    self.__player_management.piece_selection.on_next(ChessPieces.QUEEN)
                case 'king':
                    self.__player_management.piece_selection.on_next(ChessPieces.KING)

    def watch_selected_piece(self, piece: str):
        """Watch the moves reactive and update when it changes.
        Args:
            :param piece:
        """
        self.query_one("#selected_piece", Label).update(piece)

    def action_confirm_selected_piece(self):
        pass

    def compose(self) -> ComposeResult:
        yield Container(
            Container(
                Button('pawn', id='pawn', classes='upgrade-button'),
                Button('rook', id='rook', classes='upgrade-button'),
                Button('knight', id='knight', classes='upgrade-button'),
                Button('bishop', id='bishop', classes='upgrade-button'),
                Button('queen', id='queen', classes='upgrade-button'),
                Button('king', id='king', classes='upgrade-button'),
                id='piece-upgrade-grid'
            ),
            Container(
                Label('You\'ve selected: '),
                Label('pawn', id='selected_piece'),
                id='selection-container'
            ),
            Container(
                Button('confirm', variant='success', id='confirm_button'),
                id='selection-footer-container'
            ),
            id='piece-upgrade-container'
        )
