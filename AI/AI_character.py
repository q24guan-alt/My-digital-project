HP:100
attack:30
attack_timer=0
from AI import AI_statement
from player import player_statement
def update_attack():
    global attack_timer
    if  AI_statement.distance<=50:
        if attack_timer<=0:
            player_statement.hp-=attack
            attack_timer=60
        else:
            attack_timer-=1

