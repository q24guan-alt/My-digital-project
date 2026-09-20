import pygame as pg
from UI import setting
from map import room

#player data
HP=100
hurt_cooldown=800
Attack=20
Speed=10
Oxygen=100
last_hurt_time=0
attack_timer=5
Extra={"Attack_Extra":0,"Speed_Extra":0,"Oxygen_Extra":0}
player_rect=pg.Rect(400,300,20,20)
def check_trap_collision(traps,damage=10):
    global HP,last_hurt_time
    now=pg.time.get_ticks()
    if now-last_hurt_time< hurt_cooldown:
        return False
    padding=8
    size=room.Tile_size-padding*2
    for col,row,x,y in traps:
        hitbox=pg.Rect(x+padding,y+padding,size,size)
        if player_rect.colliderect(hitbox):
            HP=max(0,HP-damage)
            last_hurt_time=now
            return True

    return False


