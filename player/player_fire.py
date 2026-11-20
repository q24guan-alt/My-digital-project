import math
import os
import pygame as pg
from player import player_statement

#define configurations laser asset paths,scaling factores, scene boundaries,asset components, and direction vectors.
BASE=os.path.dirname(os.path.abspath(__file__))
SCALE=3
BOUNDS=pg.Rect(20,20,760,660)
TILE_SIZE=40
PARTS={"muzzle":2,"body":[4,3],"cap":6}

#cache loaded abd processed laser data to avoid redundant reading and processing
_cache={}
DIR_VEC={"n":(0,-1),"s":(0,1),"e":(1,0),"w":(-1,0)}

#Load the laser asset with the specified ID, crop, transparent edges, adjust colors, and cache the scaled image.
def _load(n):
    if n not in _cache:
        img=pg.image.load(os.path.join(BASE,"assets","bullets",f"Laser{n}.png")).convert_alpha()
        img=img.subsurface(img.get_bounding_rect()).copy()
        for x in range(img.get_width()):
            for y in range(img.get_height()):
                r,g,b,a=img.get_at((x,y))
                img.set_at((x,y),(b,g,r,a))
        _cache[n]=pg.transform.scale(img,(img.get_width()*SCALE,img.get_height()*SCALE))
    return _cache[n]

#Adjust the length of the laser element by preserving its start and end sections while stretching the middle portion.
def _stretch_v(img,new_h):
    w,h=img.get_size()
    cut=h//3
    if cut<1 or new_h<=h:
        return pg.transform.scale(img,(w,max(1,new_h)))
    surf=pg.Surface((w,new_h),pg.SRCALPHA)
    surf.blit(img,(0,0),(0,0,w,cut))
    mid=img.subsurface((0,cut,w,h-2*cut))
    surf.blit(pg.transform.scale(mid,(w,new_h-2*cut)),(0,cut))
    surf.blit(img,(0,new_h-cut),(0,h-cut,w,cut))
    return surf
# connect start, middle , last park for the laser, and design the full distance to make sure it's not change because distance.
def _compose(body,length):
    muzzle,cap=_load(PARTS["muzzle"]),_load(PARTS["cap"])
    mh,ch=muzzle.get_height(),cap.get_height()
    body_h=max(1,length-mh-ch)
    body_s=_stretch_v(body,body_h)
    w=max(muzzle.get_width(),body_s.get_width(),cap.get_width())
    total=mh+body_h+ch
    surf=pg.Surface((w,total),pg.SRCALPHA)
    surf.blit(cap,cap.get_rect(midtop=(w//2,0)))
    surf.blit(body_s,body_s.get_rect(midbottom=(w//2,ch)))
    surf.blit(muzzle,muzzle.get_rect(midbottom=(w//2,total)))
    return surf

#control direction, time, space and animation for laser
class Laser:
    def __init__(self,origin,direction,length,life=8):
        self.life,self.tick=life,0

        #design animation material by distance and revolve picture.
        length=max(1,int(length))
        base_frames=[_compose(_load(n),length) for n in PARTS["body"]]
        if direction=="n":
            self.frames=base_frames
        elif direction=="s":
            self.frames=[pg.transform.rotate(f,180) for f in base_frames]
        elif direction=="e":
            self.frames=[pg.transform.rotate(f,-90) for f in base_frames]
        else:
            self.frames=[pg.transform.rotate(f,90) for f in base_frames]

        # let the material and the shooting starting point ensure the lasr direction.
        self.rects=[]
        for img in self.frames:
            if direction=="n":
                rect=img.get_rect(midbottom=origin)
            elif direction=="s":
                rect=img.get_rect(midtop=origin)
            elif direction=="e":
                rect=img.get_rect(midleft=origin)
            else:
                rect=img.get_rect(midright=origin)
            self.rects.append(rect)
    #calculate about did laser still at showing time.
    @property
    def alive(self):
        return self.tick<self.life
    #control animation and missing time.
    def update(self):
        self.tick+=1
    # chang animation and draw picture by calculate time.
    def draw(self,screen):
        i=(self.tick//2)%len(self.frames)
        screen.blit(self.frames[i],self.rects[i])

#Detect whether its hits the target and causes damage along the direction.
def fire_laser(origin,direction,enemies,obstacles,damage,max_range=900):
    d=DIR_VEC[direction]
    far=(round(origin[0]+d[0]*max_range),round(origin[1]+d[1]*max_range))
#limit the range avoid going beyond the screen.
    seg=BOUNDS.clipline(origin,far)
    end=seg[1] if seg else far
    best,hit = math.dist(origin,end),None
#excluding blocker and enemgy to detect, and blocker only stop the laser.
    targets=[(e.rect,e) for e in enemies]
    targets+=[(pg.Rect(x,y,TILE_SIZE,TILE_SIZE), None) for _,_, x,y in obstacles]
    # find the target closest to the shooting distance and determine the laser emd point.
    for rect,owner in targets:
        c=rect.clipline(origin,end)
        if c:
            dist=math.dist(origin,c[0])
            if dist<best:
                best,hit=dist,owner
#The enemgy hp will decrease when laser hit enemy and blocker only stop them.
    if hit is not None:
        hit.hp-=damage
    return Laser(origin,direction,best)