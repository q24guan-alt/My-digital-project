import math

AI_statement = 0

player_x1 = 0
player_y1 = 0
AI_x1 = 0
AI_y1 = 0


def update_AI(player_x, player_y, monster_x, monster_y):

    global AI_statement
    global player_x1
    global player_y1
    global AI_x1
    global AI_y1

    player_x1 = player_x
    player_y1 = player_y
    AI_x1 = monster_x
    AI_y1 = monster_y

    distance = math.sqrt(
        (player_x1 - AI_x1) ** 2 +
        (player_y1 - AI_y1) ** 2
    )

    if distance <= 100:
        AI_statement = 1
    else:
        AI_statement = 0

    return AI_statement