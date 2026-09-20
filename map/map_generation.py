class MapGeneration:
    def __init__(self, map_manager, renderer):
        self.manager = map_manager
        self.renderer = renderer

    def on_enter_room(self, room):
        self.manager.lock_current()
        self.renderer.render(room)

    def on_task_complete(self, room):
        self.manager.unlock_current()

    def on_leave_room(self, old_room):
        old_room.clear_loot()
        self.renderer.stop_rendering(old_room)
