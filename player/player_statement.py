import pygame as pg
from UI import setting
from map import room

#player data
# document player hp,attack,move and attack cooldown and award data
hp=100
max_hp=100
hurt_cooldown=800
attack=30
speed=3
last_hurt_time=0
attack_timer=20
_attack_cooldown=0
chosen_bonuses=[]
extra={"attack_extra":0,"speed_extra":0,"max_hp":100}

#check player touch cash, and avoid sustained damage by cooling down while injured
def check_trap_collision(rect,traps,damage=10):
    global hp,last_hurt_time
    now=pg.time.get_ticks()
    if now-last_hurt_time< hurt_cooldown:
        return False
    padding=8
    size=room.TILE_SIZE-padding*2
    for col,row,x,y in traps:
        hitbox=pg.Rect(x+padding,y+padding,size,size)

        if rect.colliderect(hitbox):
            hp=max(0,hp-damage)
            last_hurt_time=now
            return True
    return False

#Record the rewards obtained by players and update the corresponding formula data.
def apply_bonus(key):
    global hp,max_hp
    chosen_bonuses.append(key)
    if key=="attack":
        extra["attack_extra"]+=5
    elif key=="speed":
        extra["speed_extra"]+=5
    elif key=="heal":
        hp=min(max_hp,hp+30)
    elif key=="maxhp":
        max_hp+=20
        hp+=20

#Determine whether the attack cooldown has ended
def can_attack():
    return _attack_cooldown <=0
#start attack cooldown time
def start_attack_cooldown():
    global _attack_cooldown
    _attack_cooldown=attack_timer
#Reduce attack cooldown frame by frame
def update_attack_cooldown():
    global _attack_cooldown
    if _attack_cooldown>0:
        _attack_cooldown-=1
#Obtain attack damage that includes an additional attack bonus
def get_attack_damage():
    return attack+extra["attack_extra"]
#Gain speed based that includes an additional speed bonus
def get_speed():
    return speed+extra["speed_extra"]


