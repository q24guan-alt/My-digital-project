import importlib.util
import random

from AI import AI_statement
import random

AI_speed = 2

wander_direction = "idle"
wander_timer = 0

def get_movement():

    global wander_direction
    global wander_timer

    # AI state 0 = wander
    if AI_statement.AI_statement == 0:

        wander_timer -= 1

        if wander_timer <= 0:
            wander_direction = random.choice(
                ["up", "down", "left", "right"]
            )
            wander_timer = random.randint(30, 120)

        if wander_direction == "up":
            return "up", AI_speed

        elif wander_direction == "down":
            return "down", AI_speed

        elif wander_direction == "left":
            return "left", AI_speed

        elif wander_direction == "right":
            return "right", AI_speed

    # AI state 1 = chase player
    elif AI_statement.AI_statement == 1:

        if AI_statement.player_x1 > AI_statement.AI_x1:
            return "right", AI_speed

        elif AI_statement.player_x1 < AI_statement.AI_x1:
            return "left", AI_speed

        elif AI_statement.player_y1 > AI_statement.AI_y1:
            return "down", AI_speed

        elif AI_statement.player_y1 < AI_statement.AI_y1:
            return "up", AI_speed

    return "idle", 0