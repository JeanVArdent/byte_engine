from game.client.user_client import UserClient
from game.common.avatar import Avatar
from game.common.enums import *
from game.common.game_object import GameObject


class Player(GameObject):
    """
    `Player Class Notes:`

    -----

        The Player class is what represents the team that's competing. The player can contain a list of Actions to
        execute each turn. The avatar is what's used to execute actions (e.g., interacting with stations, picking up
        items, etc.). For more details on the difference between the Player and Avatar classes, refer to the README
        document.
    """

    def __init__(self, code: object | None = None, team_name: str | None = None, actions: list[ActionType] = [],
                 avatars: dict[ObjectType, Avatar] | None = None):
        super().__init__()
        self.object_type: ObjectType = ObjectType.PLAYER
        self.functional: bool = True
        self.error: str | None = None
        self.file_name: str | None = None
        self.team_name: str | None = team_name
        self.code: UserClient | None = code
        self.actions: list[ActionType] = actions
        self.avatars: dict[ObjectType, Avatar] | None = avatars
        self.__selected_avatar_type: ObjectType = ObjectType.AVATAR
        self.score: int = 0

    @property
    def error(self) -> str | None:
        return self.__error

    @error.setter
    def error(self, error: str | None) -> None:
        if error is not None and not isinstance(error, str):
            raise ValueError(f'{self.__class__.__name__}.error must be either a string or None.')
        self.__error = error

    @property
    def actions(self) -> list[ActionType] | list:  # change to Action if you want to use the action object
        return self.__actions

    @actions.setter
    def actions(self, actions: list[ActionType] | list) -> None:  # showing it returns nothing(like void in java)
        # if it's (not none = and) if its (none = or)
        # going across all action types and making it a boolean, if any are true this will be true\/
        if actions is None or not isinstance(actions, list) \
                or (len(actions) > 0
                    and any(map(lambda action_type: not isinstance(action_type, ActionType), actions))):
            raise ValueError(
                f'{self.__class__.__name__}.action must be an empty list or a list of action types. It is a(n) {actions.__class__.__name__} and has the value of {actions}.')
            # ^if it's not either throw an error
        self.__actions = actions

    @property
    def functional(self) -> bool:
        return self.__functional

    @functional.setter  # do this for all the setters
    def functional(self, functional: bool) -> None:  # this enforces the type hinting
        if functional is None or not isinstance(functional, bool):  # if this statement is true throw an error
            raise ValueError(
                f'{self.__class__.__name__}.functional must be a boolean. It is a(n) {functional.__class__.__name__} and has the value of {functional}.')
        self.__functional = functional

    @property
    def team_name(self) -> str | None:
        return self.__team_name

    @team_name.setter
    def team_name(self, team_name: str | None) -> None:
        if team_name is not None and not isinstance(team_name, str):
            raise ValueError(
                f'{self.__class__.__name__}.team_name must be a String or None. It is a(n) {team_name.__class__.__name__} and has the value of {team_name}.')
        self.__team_name = team_name

    @property
    def file_name(self) -> str | None:
        return self.__file_name

    @file_name.setter
    def file_name(self, file_name: str | None) -> None:
        if file_name is not None and not isinstance(file_name, str):
            raise ValueError(f'{self.__class__.__name__}.file_name must be a String or None')
        self.__file_name = file_name

    @property
    def avatars(self) -> dict[ObjectType, Avatar]:
        return self.__avatars

    @avatars.setter
    def avatars(self, avatars: dict[ObjectType, Avatar]) -> None:
        if (avatars is not None and not (isinstance(avatars, dict)
                and len(avatars) > 0
                and all(map(lambda name_and_avatar: isinstance(name_and_avatar[0], ObjectType) and isinstance(name_and_avatar[1], Avatar), avatars.items())))):
            raise ValueError(
                f'{self.__class__.__name__}.avatars must be a dict with a key of ObjectType and a value of Avatar or None. It is a(n) {avatars.__class__.__name__} and has the value of {avatars}.')
        self.__avatars = avatars

    def select_avatar(self, avatar_type: ObjectType) -> None:
        if avatar_type is None or not isinstance(avatar_type, ObjectType):
            raise ValueError(
                f'avatar_name must be a ObjectType. It is a(n) {avatar_type.__class__.__name__} and has the value of '
                f'{avatar_type}'
            )
        self.__selected_avatar_type = avatar_type

    @property
    def avatar(self) -> Avatar | None:
        return self.avatars.get(self.__selected_avatar_type, None) if self.avatars is not None else None

    @property
    def score(self) -> int:
        return self.__score

    @score.setter
    def score(self, score: int) -> None:
        if score is None or not isinstance(score, int):
            raise ValueError(
                f'{self.__class__.__name__}.score must be an int. It is a(n) {score.__class__.__name__} and has the value of '
                f'{score}')
        self.__score: int = score

    @property
    def object_type(self) -> ObjectType:
        return self.__object_type

    @object_type.setter
    def object_type(self, object_type: ObjectType) -> None:
        if object_type is None or not isinstance(object_type, ObjectType):
            raise ValueError(
                f'{self.__class__.__name__}.object_type must be ObjectType. It is a(n) {object_type.__class__.__name__} and has the value of {object_type}.')
        self.__object_type = object_type

    def to_json(self):
        data = super().to_json()

        data['functional'] = self.functional
        data['error'] = self.error
        data['team_name'] = self.team_name
        data['file_name'] = self.file_name
        data['actions'] = [act.value for act in self.actions]
        data['selected_avatar_type'] = self.__selected_avatar_type
        data['avatars'] = { k: v.to_json() if v is not None else None for k, v in self.avatars} if self.avatars is not None else None
        data['score'] = self.score

        return data

    def from_json(self, data):
        super().from_json(data)

        self.functional = data['functional']
        self.error = data['error']
        self.team_name = data['team_name']
        self.file_name = data['file_name']
        self.score = data['score']
        self.actions: list[ActionType] = [ActionType(action) for action in data['actions']]
        self.__selected_avatar_type = data['selected_avatar_type']
        avatars: dict[str, Avatar] = data['avatars']
        if avatars is None:
            self.avatars = None
            return self
        self.avatars = { k:Avatar().from_json(v) if v is not None else None for k, v in data['avatars']}
        return self

    # to String
    def __str__(self):
        p = f"""ID: {self.id}
            Team name: {self.team_name}
            Actions: 
            """
        # This concatenates every action from the list of actions to the string 
        [p := p + action for action in self.actions]
        return p
