from game.common.enums import ActionType, ObjectType
from game.common.map.game_board import GameBoard
from game.common.player import Player
from game.controllers.controller import Controller


class AvatarSelectionController(Controller):
    def __init__(self):
        super().__init__()

    def handle_actions(self, action: ActionType, client: Player, world: GameBoard) -> None:
        """
           Given the ActionType for interacting in a direction, the Player's avatar will engage with the object.
           :param action:
           :param client:
           :param world:
           :return: None
        """

        match action:
            case ActionType.SELECT_DEFAULT_AVATAR:
                client.select_avatar(ObjectType.AVATAR)
            case _:
                return

        return