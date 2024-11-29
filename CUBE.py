import pygame
import random
import time

pygame.init()

def spawn_enemy():
    while True:
        enemy_x = random.randint(0, SCREEN_WIDTH - 25)
        enemy_y = random.randint(0, SCREEN_HEIGHT - 25)
        new_enemy = pygame.Rect(enemy_x, enemy_y, 25, 25)
        # ensure new enemy does not overlap the player
        if not player.colliderect(new_enemy):
            return new_enemy

def reposition_all_enemies():
    for i in range(len(enemies)):
        enemies[i] = spawn_enemy()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player = pygame.Rect(300, 250, 50, 50)
coin = pygame.Rect(random.randint(0, 750), random.randint(0, 550), 25, 25)

text_font = pygame.font.SysFont(None, 30)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

score = 0
highscore = 0

screen_rect = screen.get_rect()

clock = pygame.time.Clock()

run = True
menu = True
game_over = False

# list to hold enemy rectangles
enemies = []

# timer variables
coin_spawn_time = pygame.time.get_ticks()
TIME_LIMIT = 5000  


while run:
    while menu:
        screen.fill((0, 0, 0))
        draw_text("Welcome to CUBE", text_font, (255, 255, 255), 300, 150)
        draw_text("PRESS A TO START!", text_font, (255, 255, 255), 300, 200)

        for event in pygame.event.get():
            key = pygame.key.get_pressed()
            if key[pygame.K_a]:
                menu = False
        pygame.display.update()

    player.clamp_ip(screen_rect)

    screen.fill((0, 0, 0))
    draw_text(f"Score: {str(score)}", text_font, (255, 255, 255), 10, 10)

    # calculate remaining time
    current_time = pygame.time.get_ticks()
    time_left = max(0, TIME_LIMIT - (current_time - coin_spawn_time)) // 1000
    draw_text(f"Time Left: {time_left} sec", text_font, (255, 255, 255), 10, 40)

    pygame.draw.rect(screen, (0, 255, 0), player)
    pygame.draw.rect(screen, (255, 255, 0), coin)

    # draw all enemies
    for enemy in enemies:
        pygame.draw.rect(screen, (255, 0, 0), enemy)

    if player.colliderect(coin):
        # respawn coin and reset timer
        while True:
            coin_x = random.randint(0, SCREEN_WIDTH - 25)
            coin_y = random.randint(0, SCREEN_HEIGHT - 25)
            coin = pygame.Rect(coin_x, coin_y, 25, 25)
            if not player.colliderect(coin):
                break

        score += 1
        coin_spawn_time = pygame.time.get_ticks()  # Reset timer

        # add a new enemy after every 2 coins
        if score % 2 == 0:
            reposition_all_enemies()  # reposition all enemies
            enemies.append(spawn_enemy())  # add a new enemy

    # game over if time runs out
    if current_time - coin_spawn_time > TIME_LIMIT:
        game_over = True

    # check collisions with enemies
    for enemy in enemies:
        if player.colliderect(enemy):
            game_over = True

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.move_ip(-1, 0)
    elif key[pygame.K_RIGHT]:
        player.move_ip(1, 0)
    elif key[pygame.K_UP]:
        player.move_ip(0, -1)
    elif key[pygame.K_DOWN]:
        player.move_ip(0, 1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    while game_over:
        screen.fill((0, 0, 0))
        draw_text("GAME OVER", text_font, (255, 0, 0), 300, 100)
        draw_text(f"Your Score = {str(score)}", text_font, (255, 0, 0), 300, 200)
        draw_text("Press D to quit", text_font, (255, 0, 0), 300, 250)
        draw_text("Press P to play again", text_font, (255, 0, 0), 300, 300)

        if highscore < score:
            highscore = score

        draw_text(f"HIGHSCORE = {str(highscore)}", text_font, (255, 0, 255), 300, 350)

        key = pygame.key.get_pressed()
        if key[pygame.K_d]:
            game_over = False
            run = False
        elif key[pygame.K_p]:
            game_over = False
            menu = True
            score = 0
            enemies = []
            player = pygame.Rect(300, 250, 50, 50)
            coin = pygame.Rect(random.randint(0, SCREEN_WIDTH - 25), random.randint(0, SCREEN_HEIGHT - 25), 25, 25)
            coin_spawn_time = pygame.time.get_ticks()  # reset timer

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()

    pygame.display.update()

pygame.quit()
