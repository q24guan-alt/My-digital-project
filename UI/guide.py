#import code from other file
import pygame as pg
from core import page_manager
#variable for check page it is open or close and document text for guide and design button size for open button
show_guide = True
GUIDE_LINS=[
    "WASD is move key",
    "MOUSE is attack button",
    "THE door will open when they finish room",
    "N is key for open the setting webpage, It's help change move button",
]
help_button_rect=pg.Rect(760,220,30,30)
#design size and font for print text
_font=None
def _get_font(size=20):
    global _font
    if _font is None:
        _font = pg.font.SysFont("microsoftyaheu", size)
    return _font
# The button for open page on the screen.
def handle_event(event):
    global show_guide
    if show_guide:
        if event.type in(pg.KEYDOWN, pg.MOUSEBUTTONDOWN):
            show_guide = False
        return
    if event.type == pg.MOUSEBUTTONDOWN and help_button_rect.collidepoint(event.pos):
        show_guide = True
#Draw the guide button
def draw_help_button(screen):
    pg.draw.rect(screen,(80,80,80),help_button_rect)
    text= _get_font().render("?",True,(255,255,255))
    screen.blit(text,text.get_rect(center=help_button_rect.center))
#Draw the page
def draw_guide(screen):
    if not show_guide:
        return
    overlay=pg.Surface(screen.get_size(),pg.SRCALPHA)
    overlay.fill((0,0,0,160))
    screen.blit(overlay,(0,0))
    y=250
    y+=40
    for line in GUIDE_LINS:
        text=_get_font(24).render(line,True,(255,255,255))
        screen.blit(text,text.get_rect(center=(400,y)))
        y+=30
    hint=_get_font(24).render("click any key start",True,(255,255,255))
    screen.blit(hint,hint.get_rect(center=(400,y+40)))