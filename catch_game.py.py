import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player = pygame.Rect(WIDTH//2 - 30, HEIGHT - 50, 60, 20)
score = 0
lives = 3
WIN_SCORE = 30          

items = []
SPAWN_RATE = 45
counter = 0
base_speed = 2

font = pygame.font.Font(None, 36)

def spawn_item():
    x = random.randint(20, WIDTH - 20)
    if random.random() < 0.5:
        x_speed = random.uniform(-0.8, 0.8)
        items.append((pygame.Rect(x, 0, 15, 15), 'coin', x_speed))
    else:
        x_speed = random.uniform(-0.5, 0.5)
        items.append((pygame.Rect(x, 0, 15, 15), 'rock', x_speed))

running = True
win = False

while running:
    screen.fill((0,0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= 7
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.x += 7
    
    counter += 1
    if counter > max(20, SPAWN_RATE - score//10):
        spawn_item()
        counter = 0
    
    new_items = []
    for rect, typ, x_speed in items:
        rect.x += x_speed
        rect.y += base_speed + score // 80
        
        if rect.colliderect(player):
            if typ == 'coin':
                score += 1
            else:
                lives -= 1
            continue
        if rect.left < 0:
            rect.left = 0
        if rect.right > WIDTH:
            rect.right = WIDTH
        if rect.y < HEIGHT:
            new_items.append((rect, typ, x_speed))
    items = new_items
    
    if score >= WIN_SCORE:
        win = True
        running = False
    
    if lives <= 0:
        running = False
    
    pygame.draw.rect(screen, (0,255,0), player)
    for rect, typ, _ in items:
        color = (255,255,0) if typ == 'coin' else (100,100,100)
        pygame.draw.circle(screen, color, rect.center, 8)
    
    score_text = font.render(f"Score: {score}/{WIN_SCORE}", True, (255,255,255))
    lives_text = font.render(f"Lives: {lives}", True, (255,255,255))
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 100, 10))
    
    pygame.display.flip()
    clock.tick(60)

screen.fill((0,0,0))
if win:
    end_text = font.render(f"You Win! Final Score: {score}", True, (255,255,255))
else:
    end_text = font.render(f"Game Over! Score: {score}", True, (255,255,255))
screen.blit(end_text, (WIDTH//2 - 150, HEIGHT//2))
pygame.display.flip()
pygame.time.wait(3000)

pygame.quit()
sys.exit()