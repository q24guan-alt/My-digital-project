class MapGeneration:
    #coordinate the room switching display, connect the room and the map.
    def __init__(self, map_manager, renderer):
        self.manager = map_manager
        self.renderer = renderer

#when entering the new room, lock the current room and start rendering.
    def on_enter_room(self, room):
        self.manager.lock_current()
        self.renderer.render(room)

#unlock the room after the room battle complete.
    def on_task_complete(self, room):
        self.manager.unlock_current()

#level the room stop switching,avoid the old room continuing to display.
    def on_leave_room(self, old_room):
        old_room.clear_loot()
        self.renderer.stop_rendering(old_room)
