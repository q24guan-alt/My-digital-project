import importlib.util

import pygame

file_path = r"C:\Users\28212\PycharmProjects\PythonProject1\Y 12 Digital  project\UI\setting.py"

spec = importlib.util.spec_from_file_location("setting", file_path)
setting = importlib.util.module_from_spec(spec)
spec.loader.exec_module(setting)

file_path = r"C:\Users\28212\PycharmProjects\PythonProject1\Y 12 Digital  project\player\player_statement.py"

spec = importlib.util.spec_from_file_location("player_statement", file_path)
player_statement = importlib.util.module_from_spec(spec)
spec.loader.exec_module(player_statement)


up_key=setting.Keys["up"]
down_key=setting.Keys["down"]
left_key=setting.Keys["left"]
right_key=setting.Keys["right"]


key=pygame.key.get_pressed()
base_speed=20
def get_movement():

    keys = pygame.key.get_pressed()
    movement_direction = "idle"
    speed=base_speed*(1+player_statement.Extra ["movement_Extra"])
    if keys[up_key]:
        movement_direction="up"

    elif keys[down_key]:
        movement_direction="down"

    elif keys[left_key]:
        movement_direction="left"

    elif keys[right_key]:
        movement_direction="right"


    return movement_direction,speed