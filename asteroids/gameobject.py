from settings import *

class GameObjectManager:
    def __init__(self) -> None:
        self.game_objects = dict[GameObject]()
        self.next_object_id = 0
        self.cleanup_ids = []

    def register(self, obj) -> int:
        self.next_object_id += 1
        self.game_objects[self.next_object_id] = obj
        return self.next_object_id

    def deregister(self, obj_id:int) -> None:
        # can't delete from self.game_objects directly since this gets called while iterating it.
        # the workaround is to save the obj_id and clean it up later in the game loop.
        # del self.game_objects[obj_id]
        self.cleanup_ids.append(obj_id)

    def cleanup(self) -> None:
        for obj_id in self.cleanup_ids:
            try:
                del self.game_objects[obj_id]
            except:
                continue
        self.cleanup_ids = []

class GameObject:
    def __init__(self, game:GameObjectManager, x:int=HALF_WIDTH, y:int=HALF_HEIGHT) -> None:
        self.x = x
        self.y = y
        self.game = game
        self.obj_id = self.game.register(self)

    @property
    def in_bounds(self) -> bool:
        return 0 <= self.x <= WIDTH and 0 <= self.y <= HEIGHT

class UpdateMixin:
    def update(self) -> None:
        pass

class RenderMixin:
    def render(self) -> None:
        pass
