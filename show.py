import pygame
from player import player_movement
from AI import AI_statement
from AI import AI_movement
pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

player = pygame.Rect(400, 300, 20, 20)
monster = pygame.Rect(200, 200, 20, 20)

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    direction, speed = player_movement.get_movement()

    if direction == "up":
        player.y -= speed
    elif direction == "down":
        player.y += speed
    elif direction == "left":
        player.x -= speed
    elif direction == "right":
        player.x += speed

    AI_statement.update_AI(
        player.x,
        player.y,
        monster.x,
        monster.y
    )

    AI_direction, AI_speed = AI_movement.get_movement()

    if AI_direction == "up":
        monster.y -= AI_speed
    elif AI_direction == "down":
        monster.y += AI_speed
    elif AI_direction == "left":
        monster.x -= AI_speed
    elif AI_direction == "right":
        monster.x += AI_speed
    monster.clamp_ip(screen.get_rect())

    screen.fill((30, 30, 30))

    pygame.draw.rect(screen, (0, 255, 0), player)
    pygame.draw.rect(screen, (255, 0, 0), monster)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

