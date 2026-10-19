#import other page code
import pygame as pg
from player import player_statement
from player import player_movement
from map import map_manager
from core import page_manager
#use variable document what text need show when game is finish such as dead or win the game
result_text=""
#calculate hp color at different number, the ratio is proportion for hp
def _fill_color(ratio):
    blue=(70,140,220)
    red=(220,60,60)
    if ratio>=0.6:
        return blue
    t=ratio/0.6
    return tuple(int(red[i]+(blue[i]-red[i])*t)for i in range(3))
#It is document size for player hp bar and what place should be put on, and get player hp from differenet file than calculate ratio for real hp and max hp, than draw hp bar
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
# design AI hp bar, the principle same with player hp, different is hp=max hp doesn't show hp bar
def draw_AI_bar(screen,rect,hp,max_hp):
    if hp>=max_hp:
        return
    ratio=max(0,min(1,hp/max_hp))
    bar_w,bar_h=24,4
    x=rect.centerx-bar_w//2
    y=rect.top-8
    pg.draw.rect(screen,(40,40,40),(x,y,bar_w,bar_h))
    pg.draw.rect(screen,_fill_color(ratio),(x,y,int(bar_w*ratio),bar_h))

# check Game victory and defeat conditions and give resuit text different sentences whwen different outcome
def update():
    global result_text
    if page_manager.page_state is not None:
        return
    if player_statement.hp<=0:
        if not player_movement.animator.is_dead:
            player_movement.animator.trigger_death()
        elif player_movement.animator.death_done:
            result_text="You lose the game"
            page_manager.page_state="game_over"
        return
    elif (map_manager.get_room_type()=="boss" and map_manager._instance.current.cleared):
        result_text="You win the game"
        page_manager.page_state="game_over"
def handle_event(event):
    pass
# it is draw page for when condition met, it is get screen size actual page performance/appearance
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
# draw player and AI hp bar
def draw_hp_bar(screen):
    player_health_bar.draw(screen)
def draw(screen):
    draw_result(screen)