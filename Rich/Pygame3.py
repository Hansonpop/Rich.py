import pygame
import math
import random
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

while True:  # <-- master restart loop
    # ----------------------------
    # BASIC VALUES
    # ----------------------------
    CENTER = (screen.get_width() / 2, screen.get_height() / 2)
    RADIUS = 150

    angle = 0
    rotation_speed = 0.03

    player_hp = 3
    boss_hp = 15

    player_bullets = []
    boss_bullets = []
    player_shoot_cooldown = 0
    boss_shoot_timer = 0

    # ----------------------------
    # MAIN GAME LOOP
    # ----------------------------
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            angle -= rotation_speed
        if keys[pygame.K_d]:
            angle += rotation_speed

        # SHOOT
        if keys[pygame.K_SPACE] and player_shoot_cooldown <= 0:
            px = CENTER[0] + RADIUS * math.cos(angle)
            py = CENTER[1] + RADIUS * math.sin(angle)
            dx = CENTER[0] - px
            dy = CENTER[1] - py
            length = math.hypot(dx, dy)
            dx /= length
            dy /= length
            player_bullets.append([px, py, dx * 5, dy * 5])
            player_shoot_cooldown = 15

        if player_shoot_cooldown > 0:
            player_shoot_cooldown -= 1

        px = CENTER[0] + RADIUS * math.cos(angle)
        py = CENTER[1] + RADIUS * math.sin(angle)

        boss_shoot_timer += 1
        if boss_shoot_timer > 40:
            boss_shoot_timer = 0
            dx = px - CENTER[0]
            dy = py - CENTER[1]
            length = math.hypot(dx, dy)
            dx /= length
            dy /= length
            boss_bullets.append([CENTER[0], CENTER[1], dx * 4, dy * 4])

        for b in player_bullets[:]:
            b[0] += b[2]
            b[1] += b[3]
            if math.hypot(b[0] - CENTER[0], b[1] - CENTER[1]) < 20:
                boss_hp -= 1
                player_bullets.remove(b)

        for b in boss_bullets[:]:
            b[0] += b[2]
            b[1] += b[3]
            if math.hypot(b[0] - px, b[1] - py) < 15:
                player_hp -= 1
                boss_bullets.remove(b)

        screen.fill((50, 20, 20))
        pygame.draw.circle(screen, (255, 255, 255), CENTER, RADIUS, 1)
        pygame.draw.circle(screen, (100, 255, 0), CENTER, 20)
        pygame.draw.circle(screen, (50, 100, 255), (int(px), int(py)), 10)

        for bx, by, _, _ in player_bullets:
            pygame.draw.circle(screen, (255, 25, 0), (int(bx), int(by)), 5)

        for bx, by, _, _ in boss_bullets:
            pygame.draw.circle(screen, (255, 200, 200), (int(bx), int(by)), 5)

        font = pygame.font.SysFont(None, 30)
        screen.blit(font.render(f"Player HP: {player_hp}", True, (255, 255, 255)), (10, 10))
        screen.blit(font.render(f"Boss HP: {boss_hp}", True, (255, 255, 255)), (10, 40))

        pygame.display.update()
        clock.tick(60)

        if player_hp <= 0 or boss_hp <= 0:
            running = False

    # ----------------------------
    # GAME OVER SCREEN
    # ----------------------------
    font_big = pygame.font.SysFont(None, 80)
    font_small = pygame.font.SysFont(None, 40)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill((0, 0, 0))

        text1 = font_big.render("GAME OVER", True, (255, 50, 50))
        screen.blit(text1, text1.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2.5)))

        if player_hp <= 0:
            msg = "You Lost!"
        else:
            msg = "You Won!"

        text2 = font_small.render(msg, True, (255, 255, 255))
        screen.blit(text2, text2.get_rect(center=(640, 350)))

        text3 = font_small.render("Press R to Restart or Q to Quit", True, (200, 200, 200))
        screen.blit(text3, text3.get_rect(center=(640, 700)))

        pygame.display.update()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            pygame.quit()
            quit()
        if keys[pygame.K_r]:
            break  # <-- jumps back to the TOP of the outer loop
