import math
import os
import pygame as pg
from player import player_statement
BASE=os.path.dirname(os.path.abspath(__file__))
SCALE=3
bounds=pg.Rect(20,20,760,660)
tile=40
PARTS={"muzzle":2,"body":[4,3],"cap":6}
_cache={}
DIR_VEC={"n":(0,-1),"s":(0,1),"e":(1,0),"w":(-1,0)}
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

class Laser:
    def __init__(self,origin,direction,length,life=8):
        self.life,self.tick=life,0


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

    @property
    def alive(self):
        return self.tick<self.life
    def update(self):
        self.tick+=1
    def draw(self,screen):
        i=(self.tick//2)%len(self.frames)
        screen.blit(self.frames[i],self.rects[i])

def fire_laser(origin,direction,enemies,obstacles,damage,max_range=900):
    d=DIR_VEC[direction]
    far=(round(origin[0]+d[0]*max_range),round(origin[1]+d[1]*max_range))
    seg=bounds.clipline(origin,far)
    end=seg[1] if seg else far
    best,hit = math.dist(origin,end),None
    targets=[(e.rect,e) for e in enemies]
    targets+=[(pg.Rect(x,y,tile,tile), None) for _,_, x,y in obstacles]
    for rect,owner in targets:
        c=rect.clipline(origin,end)
        if c:
            dist=math.dist(origin,c[0])
            if dist<best:
                best,hit=dist,owner
    if hit is not None:
        hit.hp-=damage
    return Laser(origin,direction,best)