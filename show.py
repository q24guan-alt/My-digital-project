# This park import code from different file
import pygame as pg
from UI import setting,hud,guide
from core import page_manager
from player import player_movement,player_statement
from map import map_manager,minimap

pg.init()
screen = pg.display.set_mode((800,700))
clock = pg.time.Clock()
running = True
#Loading key bindings and recording other page of the game
setting.load_keys()
page_manager.register("setting",setting)
page_manager.register("game_over",hud)
#Handle various in game events, such as closing page
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            continue
        page_manager.handle_event(event)
        hud.handle_event(event)
        guide.handle_event(event)
#Update the game state, such as by detecting player movement, ad stop game when each page is open
    if not page_manager.is_paused():
        hud.update()
        player_movement.update()
        map_manager.update()
    player_statement.check_trap_collision(player_movement.player_rect,map_manager._instance.current.loot)
    screen.fill((30,30,30))
# Load the content rendered from other pages onto the screen
    map_manager.draw(screen)
    player_movement.draw(screen)
    page_manager.draw(screen)
    hud.draw_hp_bar(screen)
    minimap.draw(screen)
    guide.draw_help_button(screen)
    guide.draw_guide(screen)


    pg.display.flip()
    clock.tick(60)
pg.quit()