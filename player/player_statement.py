import pygame
from AI import AI_character
from UI import setting
Oxygen= 100
Oxygen_decrease = 10
Oxygen_increase = 20
Hp= 100
attack= 40
attack_time=0
Extra={
    "movement_Extra":0,
    "attack_Extra":0,
    "HP_Extra":0

}

room=1
if room == 1 and Oxygen < 100:
    Oxygen += 1
elif room == 0:
    Oxygen -= 1

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == setting.Keys["attack"] and attack_time <= 0:
                AI_character.HP -= attack * (
                    1 + Extra["attack_Extra"]
                )
                attack_timer = 30

    if attack_time > 0:
        attack_time -= 1


