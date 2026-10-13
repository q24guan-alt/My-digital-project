import pygame as pg
from map import map_manager
from player import player_statement

BONUS_LABELS={
    "attack":("Attack+5",(220,80,60)),
    "speed":("Speed+5",(80,200,220)),
    "heal":("HP recover",(80,200,100)),
    "maxhp":("Max HP",(80,200,100)),
}

_font=None

def _get_font(size=16):
    global _font
    if _font is None:
        _font = pg.font.SysFont("microsoftyahei", size)
    return _font

def draw_progress(screen):
    stage=map_manager._instance.stage
    max_stage=map_manager.Max_stage
    box_size=24
    gap=6
    total_w=max_stage*box_size+(max_stage-1)*gap
    x=(800-total_w)//2
    y=15

    for i in range(max_stage):
        rect=pg.Rect(x+i*(box_size+gap),y,box_size,box_size)
        if i<stage:
            color=(90,200,120)
        elif i==stage:
            color=(230,200,60)
        else:
            color=(70,70,70)
        pg.draw.rect(screen,color,rect)

def draw_bonus_list(screen):
    bonuses=player_statement.chosen_bonuses
    if not bonuses:
        return

    panel_w=190
    x=900-panel_w-20
    y=15
    pg.draw.rect(screen,(40,40,60),(x,y,panel_w,20+len(bonuses)*22))
    pg.draw.rect(screen,(80,80,110),(x,y,panel_w,20+len(bonuses)*22),width=2)

    font=_get_font(16)
    title=font.render("BUFFS",True,(200,200,210))
    screen.blit(title,(x+10,y+5))

    row_y=y+16
    for key in bonuses:
        label,color=BONUS_LABELS.get(key,(key,(200,200,200)))
        pg.draw.circle(screen,color,(x+15,row_y+6),5)
        text=font.render(label,True,(230,230,240))
        screen.blit(text,(x+28,row_y))
        row_y+=22

def draw(screen):
    draw_progress(screen)
    draw_bonus_list(screen)