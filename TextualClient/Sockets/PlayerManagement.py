from reactivex import Subject
from reactivex.subject import BehaviorSubject

from TextualClient.Sockets.PlayerLobby import PlayerLobby


class PlayerManagement:
    end_lobby: Subject = Subject()
    player_lobby: BehaviorSubject[PlayerLobby] = BehaviorSubject[PlayerLobby](None)
    kick_player: BehaviorSubject[str] = BehaviorSubject[str](None)
    host_address_to_join: BehaviorSubject[str] = BehaviorSubject[str]('')
