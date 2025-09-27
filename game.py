import pygame, sys, random

pygame.init()
WIDTH, HEIGHT = 600, 400
CELL = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Snake Game")

WHITE = (255,255,255)
GREEN = (0,200,0)
RED = (200,0,0)
BLACK = (0,0,0)
YELLOW = (255,255,0)

font = pygame.font.SysFont(None, 36)

eat_sound = pygame.mixer.Sound("assets/food_G1U6tlb.mp3")
gameover_sound = pygame.mixer.Sound("assets/game_over.mp3")

def draw_snake(snake):
    for block in snake:
        pygame.draw.rect(screen, GREEN, (*block, CELL, CELL))

def draw_apple(apple):
    pygame.draw.rect(screen, RED, (*apple, CELL, CELL))

def draw_text(text, pos, color=WHITE):
    txt = font.render(text, True, color)
    screen.blit(txt, pos)

def game_loop():
    snake = [(100,100), (80,100), (60,100)]
    dx, dy = CELL, 0
    apple = (random.randrange(0, WIDTH, CELL), random.randrange(0, HEIGHT, CELL))
    score = 0
    speed = 10  # vitesse initiale

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and dy == 0: dx, dy = 0, -CELL
                elif event.key == pygame.K_DOWN and dy == 0: dx, dy = 0, CELL
                elif event.key == pygame.K_LEFT and dx == 0: dx, dy = -CELL, 0
                elif event.key == pygame.K_RIGHT and dx == 0: dx, dy = CELL, 0

        head = (snake[0][0]+dx, snake[0][1]+dy)
        snake = [head] + snake[:-1]

        # Collision pomme
        if head == apple:
            snake.append(snake[-1])
            apple = (random.randrange(0, WIDTH, CELL), random.randrange(0, HEIGHT, CELL))
            score += 1
            speed += 0.5  # augmente la vitesse à chaque pomme
            eat_sound.play()

        # Collision murs ou corps
        if head[0]<0 or head[0]>=WIDTH or head[1]<0 or head[1]>=HEIGHT or head in snake[1:]:
            gameover_sound.play()
            return score

        screen.fill(BLACK)
        draw_snake(snake)
        draw_apple(apple)
        draw_text(f"Score: {score}", (10,10))
        pygame.display.flip()
        clock.tick(speed)

def menu(options, title="SNAKE GAME"):
    selected = 0
    while True:
        screen.fill(BLACK)
        draw_text(title, (WIDTH//2 - 80, HEIGHT//4))
        for i, option in enumerate(options):
            color = YELLOW if i == selected else WHITE
            draw_text(option, (WIDTH//2 - 100, HEIGHT//2 + i*40), color)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return selected

def main():
    while True:
        choice = menu(["Jouer", "Quitter"])
        if choice == 0:
            score = game_loop()
            choice_over = menu([f"Score: {score} - Rejouer", "Quitter"], "GAME OVER")
            if choice_over == 1:
                pygame.quit()
                sys.exit()
        else:
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()