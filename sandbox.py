import pygame
import sys
import physics2

window_x = 1200
window_y = 800

pygame.init()
screen = pygame.display.set_mode((window_x, window_y))
clock = pygame.time.Clock()

space = physics2.Space(1200, 800, 100, upscale=10)
player = space.add_object(50, 600, 100, 100, type="player")
platform = space.add_object(20, 750, 300, 20, type="platform")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    screen.fill((255, 255, 255))

    player_rect = pygame.Rect(*player.get_position(), 100, 100)
    pygame.draw.rect(screen, (0, 0, 255), player_rect)
    platform_rect = pygame.Rect(*platform.get_position(), 300, 20)
    pygame.draw.rect(screen, (255, 0, 0), platform_rect)

    pygame.display.flip()
    space.step(60)
    clock.tick(60)

sys.exit()
