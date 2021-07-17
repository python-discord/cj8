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
box = space.add_object(200, 700, 50, 50, type="box")
platform1 = space.add_object(20, 750, 300, 20, type="platform")
platform2 = space.add_object(20, 630, 300, 20, type="platform")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                space.move_player(player, "left")
            if event.key == pygame.K_RIGHT:
                space.move_player(player, "right")
            if event.key == pygame.K_UP:
                space.move_player(player, "up")
            if event.key == pygame.K_DOWN:
                space.move_player(player, "down")

    screen.fill((255, 255, 255))

    player_rect = pygame.Rect(*player.get_position(), 100, 100)
    pygame.draw.rect(screen, (0, 0, 255), player_rect)
    box_rect = pygame.Rect(*box.get_position(), 50, 50)
    pygame.draw.rect(screen, (0, 0, 255), box_rect)
    platform1_rect = pygame.Rect(*platform1.get_position(), 300, 20)
    pygame.draw.rect(screen, (255, 0, 0), platform1_rect)
    platform2_rect = pygame.Rect(*platform2.get_position(), 300, 20)
    pygame.draw.rect(screen, (255, 0, 0), platform2_rect)

    pygame.display.flip()
    space.step(60)
    clock.tick(60)

sys.exit()
