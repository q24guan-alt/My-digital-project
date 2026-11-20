import pygame as pg
import json
import os
#save the pending key-binding operations, font and the corresponding positions for key clicks.
remapping_action=None
font=None
key_rects={}
#Default key bindings
keys_bindings = {
    "move_up":pg.K_w,
    "move_down":pg.K_s,
    "move_left":pg.K_a,
    "move_right":pg.K_d,
    "setting":pg.K_n,
}
inventory_mod="Number"

#Initialize the page font
def init_font():
    global font
    font=pg.font.SysFont(None,20)

#Save the current key configuration to settings.json
def save_keys():
    with open("settings.json","w") as file:
        json.dump(keys_bindings,file)

#read key configuration which was current
def load_keys():
    global keys_bindings
    if os.path.exists("settings.json"):
        with open("settings.json","r") as file:
            saved=json.load(file)
            keys_bindings.update(saved)

#change the corresponding key configuration and save it. The action corresponds to the
# name of the key being modified;new key represents the pygame key code for the new key.
def remap_keys(action,new_key):
    keys_bindings[action]=new_key
    save_keys()

#Manage mouse clicks and key rebindings within the setting menu; simply click to initiate
# the rebinding process, then select you desired key to complete the assignment.
def handle_event(event):
    global remapping_action
    if remapping_action and event.type == pg.KEYDOWN:
        keys_bindings[remapping_action]=event.key
        save_keys()
        remapping_action=None
        return
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
        for action,rect in key_rects.items():
            if rect.collidepoint(event.pos):
                remapping_action=action
                return

#Draw the settings interface, including action labels and their corresponding button; use a pygame screen
#to render the settings display
def draw(screen):
    global key_rects
    if font is None:
        init_font()

    #draw setting and heating
    panel_rect=pg.Rect(150,100,500,400)
    pg.draw.rect(screen,(245,245,245),panel_rect)
    pg.draw.rect(screen,(60,60,60),panel_rect,width=2)

    title=font.render("settings",True,(40,40,40))
    screen.blit(title,(panel_rect.x+20,panel_rect.y+15))

    #redocument place for different button,help mouse for testing use.
    key_rects={}
    y=panel_rect.y+50

    for action,key_code in keys_bindings.items():
        label=font.render(action,True,(40,40,40))
        screen.blit(label,(panel_rect.x+20,y))

        #Key being rebound are indicated in a different color
        is_remapping=remapping_action==action
        key_rect=pg.Rect(panel_rect.x+200,y,150,30)
        color=(250,220,150) if is_remapping else (230,230,230)
        pg.draw.rect(screen,color,key_rect)
        pg.draw.rect(screen,(60,60,60),key_rect,width=1)

        key_name=pg.key.name(key_code) if isinstance(key_code, int) else "mouse"
        key_text=font.render(key_name,True,(40,40,40))
        screen.blit(key_text,(key_rect.x+5,y+5))

        key_rects[action]=key_rect
        y+=40