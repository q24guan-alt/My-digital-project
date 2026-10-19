#import other page code
from UI import setting,guide
import pygame as pg
#Define a global variable to track whether any page is open
page_state=None
page_modules={}
#document page
def register(page_name,module):
    page_modules[page_name]=module
#check each page open
def is_paused():
    return page_state is not None or guide.show_guide
#open or close each page
def toggle(page_name):
    global page_state
    if page_state == page_name:
        page_state=None
    elif page_state is None:
        page_state=page_name
#Detect events, such as use button open setting
def handle_event(event):
    if event.type==pg.KEYDOWN:
        for action, keycode in setting.keys.items():
            if event.key==keycode and action in page_modules:
                toggle(action)
                return True
    if page_state:
        page_modules[page_state].handle_event(event)
        return True
    return False
#draw the page
def draw(screen):
    if page_state:
        page_modules[page_state].draw(screen)