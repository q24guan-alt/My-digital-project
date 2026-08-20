import importlib.util
import pygame


file_path = r"C:\Users\28212\PycharmProjects\PythonProject1\Y 12 Digital  project\player\player_movement.py"

spec = importlib.util.spec_from_file_location(
    "player_movement",
    file_path
)

player_movement = importlib.util.module_from_spec(spec)
spec.loader.exec_module(player_movement)


pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

player = pygame.Rect(400, 300, 20, 20)


running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
    direction, speed = player_movement.get_movement()
    print(direction, speed)
    if direction == "up":
        player.y -=speed

    elif direction == "down":
       player.y += speed

    elif direction == "left":
        player.x -= speed

    elif direction == "right":
        player.x += speed

    screen.fill((30, 30, 30))

    pygame.draw.rect(
        screen,
        (0, 255, 0),
        player
    )

    pygame.display.flip()

    clock.tick(60)

pygame.quit()