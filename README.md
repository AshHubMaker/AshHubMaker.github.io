# Simple Adventure Game

A beginner-friendly game with 3 levels, pets, and coins!

```python
# Save as game.py and run: python game.py
# First install pygame: pip install pygame

import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Colors
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,0)
BLUE = (0,0,255)

class Player:
    def __init__(self):
        self.rect = pygame.Rect(50, 500, 30, 30)
        self.coins = 0
        self.pet = False
        
    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)

class Game:
    def __init__(self):
        self.player = Player()
        self.level = 1
        self.set_level()
        
    def set_level(self):
        self.platforms = []
        self.coins = []
        self.enemies = []
        self.pet_pos = None
        
        if self.level == 1:
            self.platforms = [pygame.Rect(0, 550, 800, 50)]
            self.coins = [pygame.Rect(100, 500, 20, 20)]
            self.pet_pos = pygame.Rect(700, 500, 25, 25)
            
        elif self.level == 2:
            self.platforms = [pygame.Rect(0, 550, 400, 50), 
                            pygame.Rect(500, 450, 300, 50)]
            self.coins = [pygame.Rect(200, 500, 20, 20),
                         pygame.Rect(600, 400, 20, 20)]
            self.enemies = [pygame.Rect(300, 500, 30, 30)]
            self.pet_pos = pygame.Rect(700, 400, 25, 25)
            
        elif self.level == 3:
            self.platforms = [pygame.Rect(200, 550, 400, 50),
                            pygame.Rect(0, 400, 300, 50)]
            self.coins = [pygame.Rect(300, 500, 20, 20),
                        pygame.Rect(150, 350, 20, 20)]
            self.enemies = [pygame.Rect(500, 500, 30, 30),
                          pygame.Rect(100, 350, 30, 30)]
            self.pet_pos = pygame.Rect(700, 300, 25, 25)

    def run(self):
        while True:
            screen.fill((0,0,0))
            
            # Draw platforms
            for plat in self.platforms:
                pygame.draw.rect(screen, WHITE, plat)
                
            # Draw coins
            for coin in self.coins:
                pygame.draw.rect(screen, YELLOW, coin)
                
            # Draw pet
            if self.pet_pos:
                pygame.draw.rect(screen, GREEN, self.pet_pos)
                
            # Draw enemies
            for enemy in self.enemies:
                pygame.draw.rect(screen, BLUE, enemy)
            
            # Player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player.rect.x -= 5
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player.rect.x += 5
            if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.player.rect.y >= 500:
                self.player.rect.y -= 100
                
            # Gravity
            if self.player.rect.y < 500:
                self.player.rect.y += 3
                
            # Collisions
            for coin in self.coins[:]:
                if self.player.rect.colliderect(coin):
                    self.coins.remove(coin)
                    self.player.coins += 1
                    
            if self.pet_pos and self.player.rect.colliderect(self.pet_pos):
                self.player.pet = True
                self.pet_pos = None
                
            for enemy in self.enemies:
                if self.player.rect.colliderect(enemy):
                    font = pygame.font.SysFont(None, 50)
                    text = font.render('GAME OVER!', True, RED)
                    screen.blit(text, (300, 300))
                    pygame.display.update()
                    pygame.time.wait(2000)
                    pygame.quit()
                    sys.exit()
                    
            # Level complete
            if not self.pet_pos and self.player.rect.x > 750:
                self.level += 1
                if self.level > 3:
                    font = pygame.font.SysFont(None, 50)
                    text = font.render('YOU WIN!', True, GREEN)
                    screen.blit(text, (300, 300))
                    pygame.display.update()
                    pygame.time.wait(2000)
                    pygame.quit()
                    sys.exit()
                self.set_level()
                self.player.rect.x = 50
                self.player.rect.y = 500
            
            self.player.draw()
            
            # Display info
            font = pygame.font.SysFont(None, 30)
            text = font.render(f'Level: {self.level}  Coins: {self.player.coins}  Pet: {"Yes" if self.player.pet else "No"}', 
                              True, WHITE)
            screen.blit(text, (10, 10))
            
            pygame.display.update()
            clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

if __name__ == '__main__':
    Game().run()
```

## How to Play
1. Install Python (python.org)
2. Install Pygame:  
   ```bash
   pip install pygame
   ```
3. Copy this code into a file named `game.py`
4. Run with:
   ```bash
   python game.py
   ```

**Controls**:
- Move: Arrow keys or WASD
- Jump: Up arrow or W
- Collect yellow coins
- Collect green pet to unlock next level
- Avoid blue enemies
- Reach right side after getting pet

**Features**:
- 3 different levels
- Collectible coins and pets
- Simple platform jumping
- Enemy obstacles
- Win/lose conditions
