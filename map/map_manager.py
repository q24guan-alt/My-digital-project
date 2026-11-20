import random
import os
import pygame as pg
from .room import Room, assign_types,BONUS_POOL,TILE_SIZE
from player.player_movement import player_rect
from player import player_statement
#design direction, exit coordinates, exit size and wall layout parameters
DIRECTIONS = ["N", "E", "S", "W"]
MAX_STAGE = 6
POS_MAP = {"N": (400, 20), "E": (770, 350), "S": (400, 670), "W": (20, 350)}
GAP=150
TITLE=20
_font=None

#manage te range and position of the wall in alldirections in a unified manner.
Edges = {
    "N": (0, 800, 0, True),
    "S": (0, 800, 700 - TITLE, True),
    "W": (0, 700, 0, False),
    "E": (0, 700, 800 - TITLE, False),
}
WALL_SHEET_path=os.path.join(os.path.dirname(__file__),"assets","SciFi_DungeonTileset16x16_0x72Like.png")
WALL_TILE_RECT=pg.Rect(128,0,16,16)
_wall_tile=None

#generate walls and corresponding channels according to the exit direction.
def build_walls(exit_dirs):
    gaps = {d: POS_MAP[d] for d in exit_dirs}
    tiles = []
    for side, (start, end, fixed, horizontal) in Edges.items():
        gap_center = POS_MAP[side][0 if horizontal else 1] if side in exit_dirs else None
        pos = start
        while pos < end:
            in_gap = gap_center is not None and abs(pos + TITLE/2 - gap_center) < GAP / 2
            if not in_gap:
                rect = pg.Rect(pos, fixed, TITLE, TITLE) if horizontal else pg.Rect(fixed, pos, TITLE, TITLE)
                tiles.append(rect)
            pos += TITLE
    return tiles

#generate the corresponding door area for each exit, which is used to control the closure and opening of the channel.
def build_doors(exit_dirs):
    doors={}
    for direction in exit_dirs:
        if direction=="N":
            rect=pg.Rect(400-GAP//2,0,GAP,TITLE)
        elif direction=="S":
            rect=pg.Rect(400-GAP//2,700-TITLE,GAP,TITLE)
        elif direction=="E":
            rect=pg.Rect(800-TITLE//2,350-GAP//2,TITLE,GAP)
        else:
            rect=pg.Rect(0,350-GAP//2,TITLE,GAP)
        doors[direction]=rect
    return doors

#cache fonts to avoid repeating the creation of font objects
def _get_font():
    global _font
    if _font is None:
        _font=pg.font.SysFont("microsoftyahei", 30)
    return _font
#Extract the wall material from the material map and scale the size
def get_wall_tile():
    global _wall_tile
    if _wall_tile is None:
        sheet=pg.image.load(WALL_SHEET_path).convert_alpha()
        tile=sheet.subsurface(WALL_TILE_RECT)
        _wall_tile=pg.transform.scale(tile,(TITLE,TITLE))
    return _wall_tile
#repeatedly lay the wall material and draw the range by cropping the drawing area.
def draw_wall_tile(screen,rect):
    tile=get_wall_tile()
    old_clip=screen.get_clip()
    screen.set_clip(rect)

    for y in range(rect.top,rect.bottom,TITLE):
        for x in range(rect.left,rect.right,TITLE):
            screen.blit(tile,(x,y))
    screen.set_clip(old_clip)






class MapManager:
    #Initilise the map progress, the starting room and the layout of the next batch of rooms and the layout of the next batch of rooms and the current room.
    def __init__(self):
        self.stage = 0
        self.current = Room(0, None)
        self.current.populate("start")
        self.candidates = self._spawn_next()
        self.history = [self.current]
        self.map_graph = [{"from": self.current, "options": self.candidates}]
        self.walls = build_walls([c.direction for c in self.candidates])
        self.doors=build_doors([c.direction for c in self.candidates])
    #Generate the next room according to the progress and fix the BOSS room at the end.
    def _spawn_next(self):

        if self.stage  >= MAX_STAGE-2:
            boss = Room(self.stage - 1, random.choice(DIRECTIONS))
            boss.populate("boss")
            return [boss]

#Randomly select the exit direction and rewards to ensure that each candidate room has corresponding rewards.
        dirs = random.sample(DIRECTIONS, 3)
        keys=random.sample(list(BONUS_POOL),len(dirs))
        rooms=[]
        for d,key in zip(dirs,keys):
            r=Room(self.stage + 1, d)
            r.populate("Battle")
            r.bonus=key
            rooms.append(r)
        return rooms

#switch to the selected room to issue rewards and update the follow-up route and layout.
    def move_to(self, index):
        if index >= len(self.candidates):
            return False
        chosen = self.candidates[index]
        if chosen.bonus and not chosen.bonus_given:
            player_statement.apply_bonus(chosen.bonus)
            chosen.bonus_given = True
        self.current = chosen
        self.stage += 1
        self.history.append(chosen)
        if self.current.room_type!="boss":
            self.candidates=self._spawn_next()
            self.map_graph.append({"from": self.current, "options": self.candidates})
        else:
            self.candidates=[]
        self.walls=build_walls([c.direction for c in self.candidates])
        self.doors=build_doors([c.direction for c in self.candidates])
        return True

#Update the room status, trap exit switchong and player abstacles and wall collision
    def update(self):
        self.current.update()
        room=self.current
        player_statement.check_trap_collision(player_rect,room.loot,damage=10)
        bounds = pg.Rect(TITLE, TITLE, 800 - TITLE * 2, 700 - TITLE * 2)

#If the battle is not completed or the exit will be locked, it will be allowed to enter the candidate room.
        door_locked=room.room_type in ("Battle","boss") and not room.cleared
        if not door_locked:
            for i,candidate in enumerate(self.candidates):
                x,y=POS_MAP.get(candidate.direction, (400, 350))
                if abs(player_rect.centerx-x)<GAP//2 and abs(player_rect.centery-y)<GAP//2:
                    if not bounds.contains(player_rect):
                        self.move_to(i)
                        player_rect.center=(400,350)
                    return

#Prevent players from passing through obstancles or walls in the room and limit the cross-border position to the room.
        obstacle_rects = [pg.Rect(x,y,TILE_SIZE,TILE_SIZE) for _,_,x,y in room.obstacles]
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

#Draw the current room, wall, locked status exit and candidate room reward logo.
    def draw(self, screen):
        self.current.draw(screen)
        pg.draw.rect(screen, (100, 60, 30), (0, 0, 800, 700), 6)
        for wall in self.walls:
            draw_wall_tile(screen, wall)
        door_locked=(self.current.room_type in ("boss","Battle") and not self.current.cleared)
        if door_locked:
            for direction,rect in self.doors.items():
                draw_wall_tile(screen,rect)

#Draw the curret room, wall, locked status exit and candidate room reward logo.
        for candidate in self.candidates:
            x, y = POS_MAP.get(candidate.direction, (400, 350))
            info=BONUS_POOL.get(candidate.bonus)
            color=info["color"] if info else(200,200,60)
            pg.draw.circle(screen,color, (x, y), 15)
            if info:
                text=_get_font().render(info["label"],True,(255,255,255))
                dx,dy=400-x,350-y
                d=max(1,(dx*dx+dy*dy)**0.5)
                screen.blit(text,text.get_rect(center=(x+dx/d*60,y+dy/d*60)))
#Get the current room type.
    def get_room_type(self):
        if self.current and hasattr(self.current, "room_type"):
            return self.current.room_type
        return "Unknown"

#Get the current number of enemies.
    def get_ai_count(self):
        if self.current and hasattr(self.current, "ai_count"):
            return self.current.ai_count
        return 0
#Create an instance of the global map manager for other modules to use.
_instance = MapManager()

def draw(screen):
    _instance.draw(screen)

def update():
    _instance.update()
    #provide interface to quary the roon type and the number of enemies.
def get_room_type():
    return _instance.get_room_type()
def get_ai_count():
    return _instance.get_ai_count()