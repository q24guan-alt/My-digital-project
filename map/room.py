import random
import os
import pygame as pg
from AI.AI_statement import EnemyAI
from player import player_statement
from core import page_manager
Room_size={"weight":800,"height":700}
Room_type=["Battle"]
Decay=0.4
Tile_size=40
Bonus_Pool={
      "attack":{"label":"attack+5","color":(220,80,60)},
      "speed":{"label":"speed+2","color":(80,200,220)},
      "heal":{"label":"HP recovery+30","color":(80,200,100)},
      "maxhp":{"label":"HP limit+20","color":(230,180,60)},
}
SHEET_PATH=os.path.join(os.path.dirname(__file__),"assets","SciFi_DungeonTileset16x16_0x72Like.png")
BOX_RECT=pg.Rect(224,32,16,16)
SPIKE_RECT=pg.Rect(64,64,32,32)
_FLOOR_RECT=pg.Rect(16,64,16,16)
_box_img=None
_spike_img=None
_floor_img=None
def _get_floor():
      global _floor_img
      if _floor_img is None:
            sheet = pg.image.load(SHEET_PATH).convert_alpha()
            floor=sheet.subsurface(_FLOOR_RECT)
            _floor_img=pg.transform.scale(floor,(Tile_size,Tile_size))
      return _floor_img
def _get_spike():
      global _spike_img
      if _spike_img is None:
            sheet = pg.image.load(SHEET_PATH).convert_alpha()
            _spike_img=pg.transform.scale(sheet.subsurface(SPIKE_RECT), (Tile_size, Tile_size))
      return _spike_img
def _get_box():
      global _box_img
      if _box_img is None:
            sheet = pg.image.load(SHEET_PATH).convert_alpha()
            _box_img = pg.transform.scale(sheet.subsurface(BOX_RECT), (Tile_size, Tile_size))
      return _box_img
class Room:
      def __init__(self,stage,direction):
            self.obstacles=[]
            self.stage=stage
            self.direction=direction
            self.room_type=None
            self.loot=[]
            self.locked=False
            self.aisle=[]
            self.AI_Name_list=[]
            self.AI=[]
            self.cleared=False
            self.traps=[]
            self.bonus=None
            self.bonus_given=False
      def populate(self,room_type):
            self.room_type=room_type
            self.AI=self._generate_AI()
            print({self.stage},{self.room_type},{ai.ai_type_name for ai in self.AI})
            if room_type =="Battle":
                  cells=Room.build_grid(800,700)
                  cells=[c for c in cells if abs(c[2]-400)+abs(c[3]-350)>120]
                  self.loot=Room.spike(cells,random.randint(3,6))
                  remaining = [c for c in cells if c not in self.loot]
                  self.obstacles = Room.spike(remaining, random.randint(3, 6), min_map=6)

      def _generate_AI(self):
            if self.room_type=="Battle":
                  count=random.randint(4,7)
                  result=[EnemyAI(random.randint(60,740),random.randint(60,640),"normal_AI")for _ in range(count) ]
                  return result
            if self.room_type=="boss":
                  return[EnemyAI(400,150,"BOSS")]
            return[]

      def update(self,paused=False):
            for ai in self.AI:
                  if ai.hp<=0 and not ai.animator.is_dead:
                        ai.animator.trigger_death()
                  ai.update(paused=page_manager.page_state is not None)
                  Room.check_enemy_trap(ai,self.loot,damage=5)
            self.AI=[ai for ai in self.AI if ai.hp>0]
            if self.room_type in ("Battle","boss") and not self.AI:
                  self.cleared=True
            if paused:
                  return

      @staticmethod
      def check_enemy_trap(enemy,traps,damage=5,cooldown=60):
            if getattr(enemy,"trap_cooldown",0)>0:
                  enemy.trap_cooldown-=1
                  return False
            padding=8
            size=Tile_size-padding*2
            for col,row,x,y in traps:
                  hitbox=pg.Rect(x+padding,y+padding,size,size)
                  if enemy.rect.colliderect(hitbox):
                        enemy.hp-=damage
                        enemy.trap_cooldown=cooldown
                        return True
            return False

      @staticmethod
      def build_grid(room_width,room_height,margin=Tile_size):
            cols=(room_width-margin*2)//Tile_size
            rows=(room_height-margin*2)//Tile_size
            grid_cells=[]
            for row in range(rows):
                  for col in range(cols):
                        x=margin+col*Tile_size
                        y=margin+row*Tile_size
                        grid_cells.append((col,row,x,y))
            return grid_cells

      @staticmethod
      def spike(grid_cells, count, min_map=5):
            cells=list(grid_cells)
            random.shuffle(cells)
            traps=[]
            for cell in cells:
                  col,row=cell[0],cell[1]
                  too_close=any(abs(col- t[0])+abs(row-t[1])<=min_map for t in traps)
                  if not too_close:
                        traps.append(cell)
                  if len(traps)>=count:
                        break
            return traps

      def draw(self,screen):
            for y in range (0,Room_size["height"],Tile_size):
                  for x in range (0,Room_size["weight"],Tile_size):
                        screen.blit(_get_floor(),(x,y))
            _box_img=_get_box()
            for col, row, x, y in self.obstacles:
                  screen.blit(_get_box(),(x,y))
            padding=8
            _spike_img=_get_spike()
            for col,row,x,y in self.loot:
                  screen.blit(_get_spike(),(x,y))
            for ai in self.AI:
                  ai.draw(screen)

def assign_types(rooms):
      weights={t:1.0 for t in Room_type}
      for room in rooms:
            picked = random.choices(list(weights), weights=list(weights.values()))[0]
            weights[picked] *= Decay
            room.populate(picked)
      return rooms

