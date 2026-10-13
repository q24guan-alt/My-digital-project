import random
import pygame as pg
from .room import Room, assign_types,Bonus_Pool,Tile_size
from player.player_movement import player_rect
from player import player_statement
Directions = ["N", "E", "S", "W"]
Max_stage = 6
Pos_Map = {"N": (400, 20), "E": (770, 350), "S": (400, 670), "W": (20, 350)}
Gap=150
TITLE=20
_font=None
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

def _get_font():
    global _font
    if _font is None:
        _font=pg.font.SysFont("microsoftyahei", 30)
    return _font




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
        keys=random.sample(list(Bonus_Pool),len(dirs))
        rooms=[]
        for d,key in zip(dirs,keys):
            r=Room(self.stage + 1, d)
            r.populate("Battle")
            r.bonus=key
            rooms.append(r)
        return rooms

    def move_to(self, index):
        if index >= len(self.candidates):
            return False
        chosen = self.candidates[index]
        if chosen.bonus and not chosen.bonus_given:
            player_statement.apply_bonus(chosen.bonus)
        self.current = chosen
        self.stage += 1

    def handle_event(self, event):
        pass

    def update(self):
        self.current.update()
        room=self.current
        player_statement.check_trap_collision(player_rect,room.loot,damage=10)
        if room.cleared and room.bonus and not room.bonus_given:
            player_statement.apply_bonus(room.bonus)
            room.bonus_given = True
        bounds = pg.Rect(TITLE, TITLE, 800 - TITLE * 2, 700 - TITLE * 2)


        door_locked=room.room_type in ("Battle","boss") and not room.cleared
        if not door_locked:
            for i,candidate in enumerate(self.candidates):
                x,y=Pos_Map.get(candidate.direction, (400, 350))
                if abs(player_rect.centerx-x)<Gap//2 and abs(player_rect.centery-y)<Gap//2:
                    if not bounds.contains(player_rect):
                        self.move_to(i)
                        player_rect.center=(400,350)
                    return
        obstacle_rects = [pg.Rect(x,y,Tile_size,Tile_size) for _,_,x,y in room.obstacles]
        for obstacle in obstacle_rects:
            if player_rect.colliderect(obstacle):
                if player_rect.centerx<obstacle.centerx:
                    player_rect.right=obstacle.left
                else:
                    player_rect.left=obstacle.right
                if player_rect.centery<obstacle.centery:
                        player_rect.bottom=obstacle.top
                else:
                    player_rect.top=obstacle.bottom
        for wall in self.walls:
            if player_rect.colliderect(wall):
                player_rect.clamp_ip(bounds)
                break
        if  not bounds.contains(player_rect):
            player_rect.clamp_ip(bounds)

    def draw(self, screen):
        pg.draw.rect(screen, (60, 60, 90), (0, 0, 800, 700))
        pg.draw.rect(screen, (100, 60, 30), (0, 0, 800, 700), 6)
        for wall in self.walls:
            pg.draw.rect(screen, (100, 60, 30), wall)
        for candidate in self.candidates:
            x, y = Pos_Map.get(candidate.direction, (400, 350))
            info=Bonus_Pool.get(candidate.bonus)
            color=info["color"] if info else(200,200,60)
            pg.draw.circle(screen,color, (x, y), 15)
            if info:
                text=_get_font().render(info["label"],True,(255,255,255))
                dx,dy=400-x,350-y
                d=max(1,(dx*dx+dy*dy)**0.5)
                screen.blit(text,text.get_rect(center=(x+dx/d*60,y+dy/d*60)))
        self.current.draw(screen)
    def get_room_type(self):
        if self.current and hasattr(self.current, "room_type"):
            return self.current.room_type
        return "Unknown"

    def get_ai_count(self):
        if self.current and hasattr(self.current, "ai_count"):
            return self.current.ai_count
        return []

_instance = MapManager()

def handle_event(event):
    _instance.handle_event(event)

def draw(screen):
    _instance.draw(screen)

def update():
    _instance.update()
def get_room_type():
    return _instance.get_room_type()
def get_ai_count():
    return _instance.get_ai_count()