import pygame
import json
pygame.init()
#setting quickly keys for game reaction
Keys={
    "up":pygame.K_w,
    "down":pygame.K_s,
    "left":pygame.K_a,
    "right":pygame.K_d,
    "attack":"mouse",
    "backpack":pygame.K_e,
    "guide board":pygame.K_c,
    "stop": pygame.K_ESCAPE
}#document each normal key
inventory_mode=0
inventory_modes=["wheel", "number"]
#document inventory different type for quickly change

def save_keys():
    with open("settings.json", "w") as file:
        json.dump(Keys, file)

def ramap_keys(action,newkey):
    Keys[action]=newkey
    save_keys()
