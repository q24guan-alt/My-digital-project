from core import page_manager
from UI import setting
from player import player_statement
import pygame as pg
from player.character_animation import animator
player_rect=pg.Rect(400,300,20,20)
facing_right = True
def update():
    global facing_right
    if page_manager.page_state is not None:
        return
    keys=pg.key.get_pressed()
    speed = player_statement.Speed * (player_statement.Extra["Speed_Extra"] + 1) # calculate speed
    if keys[pg.K_j]:
        animator.trigger_attack()

    is_moving = False
    if not animator.is_attacking:
        if keys[setting.Keys["Move_up"]]:#check player use keyboard
            player_rect.y -= speed
            is_moving = True
        elif keys[setting.Keys["Move_down"]]:
            player_rect.y += speed
            is_moving = True
        elif keys[setting.Keys["Move_left"]]:
            player_rect.x -= speed
            is_moving = True
            facing_right = False
        elif keys[setting.Keys["Move_right"]]:
            player_rect.x += speed
            is_moving = True
            facing_right = True
    animator.update(is_moving, facing_right)
def draw(screen):
    animator.draw(screen, player_rect)