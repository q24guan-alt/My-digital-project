import math
from core import page_manager
from UI import setting
from player import player_statement
import pygame as pg
from player.character_animation import animator
from player.player_fire import fire_laser
player_rect=pg.Rect(400,300,20,20)
facing_right = True
facing_dir="s"
VEC={"n":(0,-1),"s":(0,1),"e":(1,0),"w":(-1,0)}
MUZZLE_OFFSET={"n":(0,-8),"s":(0,8),"e":(10,0),"w":(-10,0)}
lasers=[]
room_provider =None

def set_room_provider(func):
    global room_provider
    room_provider = func

def fire_player_laser():
    from map import map_manager
    room=map_manager._instance.current
    ox,oy=MUZZLE_OFFSET[facing_dir]
    origin=(player_rect.centerx+ox,player_rect.centery+oy)
    lasers.append(fire_laser(origin,facing_dir,room.AI,room.obstacles,player_statement.get_attack_damage()))
def update():
    global facing_right,facing_dir
    if page_manager.page_state is not None:
        return
    if animator.is_dead:
        animator.update(False,facing_right)
        return
    keys=pg.key.get_pressed()
    speed = player_statement.get_speed()
    player_statement.update_attack_cooldown()
    mouse_pressed=pg.mouse.get_pressed()[0]
    if mouse_pressed and player_statement.can_attack():
        animator.trigger_attack()
        fire_player_laser()
        player_statement.start_attack_cooldown()

    is_moving = False
    if not animator.is_attacking:
        if keys[setting.keys["move_up"]]:
            player_rect.y-= speed
            is_moving=True
            facing_dir="n"
        elif keys [setting.keys["move_down"]]:
            player_rect.y+= speed
            is_moving = True
            facing_dir="s"
        elif keys[setting.keys["move_left"]]:
            player_rect.x-= speed
            is_moving = True
            facing_right = False
            facing_dir="w"
        elif keys[setting.keys["move_right"]]:
            player_rect.x+= speed
            is_moving = True
            facing_right = True
            facing_dir="e"

    animator.update(is_moving, facing_right)
    for laser in lasers:
        laser.update()
    lasers[:] = [laser for laser in lasers if laser.alive]

def draw_aim_indicator(screen):
    cx,cy=player_rect.center
    vx,vy=VEC[facing_dir]
    base_angle=math.atan2(vy,vx)

    color=(255,220,70)
    center_len=65
    side_len=35
    side_angle=math.radians(30)
    end_center=(cx+vx*center_len,cy+vy*side_len)
    pg.draw.line(screen,color,(cx,cy),end_center,3)

    for sign in(-1,1):
        angle=base_angle+sign*side_angle
        end=(cx+math.cos(angle)*side_len,cy+math.sin(angle)*side_len)
        pg.draw.line(screen,(255,255,255),(cx,cy),end,1)

def draw(screen):
    animator.draw(screen, player_rect)
    draw_aim_indicator(screen)
    for laser in lasers:
        laser.draw(screen)