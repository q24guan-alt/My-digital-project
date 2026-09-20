import random
import pygame as pg
from .room import Room, assign_types
from player.player_movement import player_rect

Directions = ["N", "E", "S", "W"]
Max_stage = 6
Pos_Map = {"N": (400, 20), "E": (770, 350), "S": (400, 670), "W": (20, 350)}
Gap=150
TITLE=20
Edges = {
    "N": (0, 800, 0, True),
    "S": (0, 800, 700 - TITLE, True),
    "W": (0, 700, 0, False),
    "E": (0, 700, 800 - TITLE, False),
}
def build_walls(exit_dirs):
    gaps = {d: Pos_Map[d] for d in exit_dirs}
    tiles = []
    for side, (start, end, fixed, horizontal) in Edges.items():
        gap_center = gaps[side][0 if horizontal else 1] if side in gaps else None
        pos = start
        while pos < end:
            in_gap = gap_center is not None and abs(pos + TITLE/2 - gap_center) < Gap / 2
            if not in_gap:
                rect = pg.Rect(pos, fixed, TITLE, TITLE) if horizontal else pg.Rect(fixed, pos, TITLE, TITLE)
                tiles.append(rect)
            pos += TITLE
    return tiles



class MapManager:
    def __init__(self):
        self.stage = 0
        self.current = Room(0, None)
        self.current.populate("start")
        self.candidates = self._spawn_next()
        self.history = [self.current]
        self.map_graph = [{"from": self.current, "options": self.candidates}]
        self.walls = build_walls([c.direction for c in self.candidates])

    def _spawn_next(self):
        if self.stage + 1 >= Max_stage:
            boss = Room(self.stage + 1, random.choice(Directions))
            boss.populate("boss")
            return [boss]
        dirs = random.sample(Directions, 3)
        rooms = [Room(self.stage + 1, d) for d in dirs]
        return assign_types(rooms)

    def move_to(self, index):
        if index >= len(self.candidates):
            return False
        self.current = self.candidates[index]
        self.stage += 1
        self.history.append(self.current)
        if self.current.room_type != "boss":
            self.candidates = self._spawn_next()
            self.map_graph.append({"from": self.current, "options": self.candidates})
        else:
            self.candidates = []
        self.walls = build_walls([c.direction for c in self.candidates])
        return True

    def handle_event(self, event):
        pass

    def update(self):
        bounds = pg.Rect(TITLE, TITLE, 800 - TITLE * 2, 700 - TITLE * 2)
        for i, candidate in enumerate(self.candidates):
            x, y = Pos_Map.get(candidate.direction, (400, 350))
            if abs(player_rect.centerx - x) < Gap // 2 and abs(player_rect.centery - y) < Gap // 2:
                if not bounds.contains(player_rect):
                    self.move_to(i)
                    player_rect.center = (400, 350)
                return
        for wall in self.walls:
            if player_rect.colliderect(wall):
                player_rect.clamp_ip(bounds)
                break

    def draw(self, screen):
        pg.draw.rect(screen, (60, 60, 90), (0, 0, 800, 700))
        pg.draw.rect(screen, (100, 60, 30), (0, 0, 800, 700), 6)
        for wall in self.walls:
            pg.draw.rect(screen, (100, 60, 30), wall)
        for candidate in self.candidates:
            x, y = Pos_Map.get(candidate.direction, (400, 350))
            pg.draw.circle(screen, (200, 200, 60), (x, y), 15)
        self.current.draw(screen)

_instance = MapManager()

def handle_event(event):
    _instance.handle_event(event)

def draw(screen):
    _instance.draw(screen)

def update():
    _instance.update()
