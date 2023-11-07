
class GameObjectManager:
    def __init__(self) -> None:
        self.game_objects = list[GameObject]()

class GameObject:
    def __init__(self, game:GameObjectManager) -> None:
        self.game = game
        self.game.game_objects.append(self)

class UpdateMixin:
    def update(self) -> None:
        pass

class RenderMixin:
    def render(self) -> None:
        pass