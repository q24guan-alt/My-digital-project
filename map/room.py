import random
import pygame as pg
from AI.AI_statement import EnemyAI
from player import player_statement
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
            if room_type in"Battle":
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
                  return[EnemyAI(400,350,"BOSS")]
            return[]

      def update(self):
            for ai in self.AI:
                  ai.update()
                  Room.check_enemy_trap(ai,self.loot,damage=5)
            self.AI=[ai for ai in self.AI if ai.hp>0]
            if self.room_type in ("Battle","boss") and not self.AI:
                  self.cleared=True

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
      def build_grid(room_width,room_height,margin=20):
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
            for col, row, x, y in self.obstacles:
                  pg.draw.rect(screen, (70, 60, 50), (x, y, Tile_size, Tile_size))
            padding=8
            for cell in self.loot:
                  col,row,x,y=cell
                  pg.draw.rect(screen,(90,90,90),(x+padding,y+padding,Tile_size-padding*2,Tile_size-padding*2))
                  pg.draw.polygon(screen,(255,255,0),[(x+Tile_size//2,y+padding),(x+padding , y+Tile_size-padding),(x+Tile_size-padding,y+Tile_size-padding)])
            for ai in self.AI:
                  ai.draw(screen)

def assign_types(rooms):
      weights={t:1.0 for t in Room_type}
      for room in rooms:
            picked = random.choices(list(weights), weights=list(weights.values()))[0]
            weights[picked] *= Decay
            room.populate(picked)
      return rooms

