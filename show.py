import pygame as pg
from UI import setting,backpack
from core import page_manager
from player import player_movement,player_statement
from map import map_manager
from map import room

pg.init()
screen = pg.display.set_mode((800,700))
clock = pg.time.Clock()
running = True

setting.load_keys()

page_manager.register("setting",setting)
page_manager.register("backpack",backpack)

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            continue
        page_manager.handle_event(event)

    player_movement.update()
    map_manager.update()
    player_statement.check_trap_collision(map_manager._instance.current.loot)
    screen.fill((30,30,30))
    map_manager.draw(screen)
    player_movement.draw(screen)
    page_manager.draw(screen)



    pg.display.flip()
    clock.tick(60)

pg.quit()