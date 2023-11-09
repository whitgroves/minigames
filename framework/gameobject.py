
class GameObjectBase:
    def __init__(self, x:int, y:int) -> None:
        self.x = x
        self.y = y

class GameObjectManager:
    def __init__(self) -> None:
        self.game_objects = dict[GameObjectBase]()
        self.next_object_id = 0
        self.cleanup_ids = list[int]()

    def register(self, obj:GameObjectBase) -> None: # no type hints for this one
        if not isinstance(obj, GameObjectBase):
            raise TypeError('Must register object of type GameObject.')
        self.next_object_id += 1
        self.game_objects[self.next_object_id] = obj
        return self.next_object_id
    
    def deregister(self, obj_id:int) -> None:
        self.cleanup_ids.append(obj_id)

    def cleanup(self) -> None:
        for obj_id in self.cleanup_ids:
            del self.game_objects[obj_id]
        self.cleanup_ids.clear()

class GameObject(GameObjectBase):
    def __init__(self, manager:GameObjectManager, **kwargs) -> None:
        super().__init__(**kwargs)
        self.manager = manager
        self.obj_id = self.manager.register(self)

class UpdateMixin:
    def update(self) -> None:
        pass

class RenderMixin:
    def render(self) -> None:
        pass
