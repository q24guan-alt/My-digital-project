import pygame as pg
import json
import os
#
remapping_action=None
font=None
key_rects={}
keys = {
    "move_up":pg.K_w,
    "move_down":pg.K_s,
    "move_left":pg.K_a,
    "move_right":pg.K_d,
    "setting":pg.K_n,
}
inventory_mod="Number"

def init_font():
    global font
    font=pg.font.SysFont(None,20)

def save_keys():
    with open("settings.json","w") as file:
        json.dump(keys,file)

def load_keys():
    global keys
    if os.path.exists("settings.json"):
        with open("settings.json","r") as file:
            saved=json.load(file)
            keys.update(saved)

def remap_keys(action,newkey):
    keys[action]=newkey
    save_keys()

def handle_event(event):
    global remapping_action
    if remapping_action and event.type == pg.KEYDOWN:
        keys[remapping_action]=event.key
        save_keys()
        remapping_action=None
        return
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
        for action,rect in key_rects.items():
            if rect.collidepoint(event.pos):
                remapping_action=action
                return

def draw(screen):
    global key_rects
    if font is None:
        init_font()

    panel_rect=pg.Rect(150,100,500,400)
    pg.draw.rect(screen,(245,245,245),panel_rect)
    pg.draw.rect(screen,(60,60,60),panel_rect,width=2)

    title=font.render("settings",True,(40,40,40))
    screen.blit(title,(panel_rect.x+20,panel_rect.y+15))

    key_rects={}
    y=panel_rect.y+50

    for action,keycode in keys.items():
        label=font.render(action,True,(40,40,40))
        screen.blit(label,(panel_rect.x+20,y))

        is_remapping=remapping_action==action
        key_rect=pg.Rect(panel_rect.x+200,y,150,30)
        color=(250,220,150) if is_remapping else (230,230,230)
        pg.draw.rect(screen,color,key_rect)
        pg.draw.rect(screen,(60,60,60),key_rect,width=1)

        key_name=pg.key.name(keycode) if isinstance(keycode, int) else "mouse"
        key_text=font.render(key_name,True,(40,40,40))
        screen.blit(key_text,(key_rect.x+5,y+5))

        key_rects[action]=key_rect
        y+=40