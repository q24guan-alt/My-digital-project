import pygame as pg
from player import player_statement
from map import map_manager
from core import page_manager
result_text=""
def _fill_color(ratio):
    blue=(70,140,220)
    red=(220,60,60)
    if ratio>=0.6:
        return blue
    t=ratio/0.6
    return tuple(int(red[i]+(blue[i]-red[i])*t)for i in range(3))

class playerhealthbar:
    PHP=(30,30)
    width=180
    height=20
    border=3
    def draw(self,screen):
        hp,max_hp=player_statement.hp,player_statement.max_hp
        ratio=max(0,min(1,hp/max_hp))
        x,y=self.PHP
        pg.draw.rect(screen,(20,20,20),(x,y,self.width,self.height))
        inner_w=self.width-self.border*2
        inner_h=self.height-self.border*2
        fill_w=int(inner_w*ratio)
        if fill_w>0:
            pg.draw.rect(screen,_fill_color(ratio),(x+self.border,y+self.border,fill_w,inner_h))

player_health_bar=playerhealthbar()

def draw_AI_bar(screen,rect,hp,max_hp):
    if hp>=max_hp:
        return
    ratio=max(0,min(1,hp/max_hp))
    bar_w,bar_h=24,4
    x=rect.centerx-bar_w//2
    y=rect.top-8
    pg.draw.rect(screen,(40,40,40),(x,y,bar_w,bar_h))
    pg.draw.rect(screen,_fill_color(ratio),(x,y,int(bar_w*ratio),bar_h))


def update():
    global result_text
    if page_manager.page_state is not None:
        return
    if player_statement.hp<=0:
        result_text="You lose the game"
        page_manager.page_state="game_over"
    elif map_manager.get_room_type()=="boss" and map_manager._instance.stage>0 and map_manager.get_ai_count()==0:
        result_text="You win the game"
        page_manager.page_state="game_over"
def handle_event(event):
    pass

def draw_result(screen):

    overlay=pg.Surface(screen.get_size(),pg.SRCALPHA)
    overlay.fill((0,0,0,180))
    screen.blit(overlay,(0,0))

    popup=pg.Surface((400,200),pg.SRCALPHA)
    popup.fill((30,30,30,240))
    pg.draw.rect(popup,(255,215,0),popup.get_rect(),4)
    font=pg.font.SysFont("Arial",32,bold=True)
    text_surf=font.render(result_text,True,(250,250,250))
    text_rect=text_surf.get_rect(center=(200,100))
    popup.blit(text_surf,text_rect)
    screen_width,screen_height=screen.get_size()
    screen.blit(popup,((screen_width-400)//2,(screen_height-200)//2))

def draw_hp_bar(screen):
    player_health_bar.draw(screen)
def draw(screen):
    draw_result(screen)