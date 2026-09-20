from UI import setting
import pygame as pg

page_state=None
page_modules={}

def register(page_name,module):
    page_modules[page_name]=module

def toggle(page_name):
    global page_state
    if page_state == page_name:
        page_state=None
    elif page_state is None:
        page_state=page_name

def handle_event(event):
    if event.type==pg.KEYDOWN:
        for action, keycode in setting.Keys.items():
            if event.key==keycode and action in page_modules:
                toggle(action)
                return True

    if page_state:
        page_modules[page_state].handle_event(event)
        return True

    return False

def draw(screen):
    if page_state:
        page_modules[page_state].draw(screen)