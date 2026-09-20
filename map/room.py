import random
import pygame as pg
from AI.AI_statement import EnemyAI
Room_size={"weight":800,"height":700}
Room_type=["Battle"]
Decay=0.4
Tile_size=40
class Room:
      def __init__(self,stage,direction):
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

      def populate(self,room_type):
            self.room_type=room_type
            self.loot=self._gemerate_loot()
            self.AI=self._generate_AI()
            if room_type in("Battle"):
                  cells=Room.build_grid(800,700)
                  cells=[c for c in cells if abs(c[2]-400)+abs(c[3]-350)>120]
                  self.traps=Room.spike(cells,random.randint(3,6))

      def _gemerate_loot(self):
            if self.room_type=="Resource":
                  return["item"]
            return[]
      def _generate_AI(self):
            if self.room_type=="Battle":
                  count=random.randint(4,7)
                  return[EnemyAI(random.randint(60,740), random.randint(60,640),"normal_AI")for _ in range(count)]
            if self.room_type=="boss":
                  return[EnemyAI(400,350,"BOSS")]
            return[]
      def clear_loot(self):
            self.loot=[]
            if self.room_type=="Battle":
                  count=random.randint(5,10)

      def spike(grid_cells, count, min_map=5):
            loot=[]
            copy_list=grid_cells
            random.shuffle(copy_list)
            for cell in copy_list:
                  col,row,x,y=cell
                  too_close=False
                  for c_col,c_row,_,_ in loot:
                        if abs(col-c_col)+abs(row-c_row)<=min_map:
                              too_close=True
                              break
                        if not too_close:
                              loot.append(cell)
                        if len(loot)==count:
                              break
            return loot
      def draw(self,screen):
            padding=8
            for cell in self.loot:
                  x,y=cell[2],cell[3] if len(cell)>=4 else(cell[0],cell[1])
                  trap_rect=pg.Rect(x+padding,y+padding,Tile_size*2,Tile_size-padding*2)
                  pg.draw.rect(screen,(150,150,150),trap_rect)
                  top_point=(x+Tile_size//2,y+padding)
                  left_point=(x+padding,y+Tile_size-padding)
                  right_point=(x+Tile_size-padding,y+Tile_size-padding)
                  pg.draw.polygon(screen,(200,40,40),[top_point,left_point,right_point])
            for ai in self.AI:
                  ai.draw(screen)
def assign_types(rooms):
      weights={t:1.0 for t in Room_type}
      for room in rooms:
            picked = random.choices(list(weights), weights=list(weights.values()))[0]
            weights[picked] *= Decay
            room.populate(picked)
      return rooms

