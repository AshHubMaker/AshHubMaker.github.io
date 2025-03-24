import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 32
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# Initialize screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Adventure Quest")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.velocity = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(50, HEIGHT - 100)
        self.coins = 0
        self.pets = []
        self.health = 100
        self.jumping = False

    def update(self):
        self.velocity.y += 0.5  # Gravity
        self.pos += self.velocity
        self.rect.midbottom = self.pos
        self.health = min(self.health + 0.1, 100)  # Auto-regen

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center=(x, y))

class Pet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((24, 24))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(x, y))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, patrol_range=100):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = 1
        self.speed = 2
        self.patrol_range = patrol_range
        self.start_x = x

    def update(self):
        self.rect.x += self.direction * self.speed
        if abs(self.rect.x - self.start_x) > self.patrol_range:
            self.direction *= -1

class MovingPlatform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x=0, move_y=0):
        super().__init__()
        self.image = pygame.Surface((100, 20))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.move_x = move_x
        self.move_y = move_y
        self.direction = 1

    def update(self):
        self.rect.x += self.move_x * self.direction
        self.rect.y += self.move_y * self.direction
        if self.rect.x > WIDTH - 200 or self.rect.x < 0:
            self.direction *= -1

class Level:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.platforms = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.pets = pygame.sprite.Group()
        self.moving_platforms = pygame.sprite.Group()
        self.create_level()

    def create_level(self):
        pass

class Level1(Level):
    def create_level(self):
        # Platforms
        for x in range(0, WIDTH, 100):
            platform = pygame.sprite.Sprite()
            platform.image = pygame.Surface((100, 20))
            platform.image.fill(WHITE)
            platform.rect = platform.image.get_rect(topleft=(x, HEIGHT - 50))
            self.platforms.add(platform)
        
        # Coins
        for _ in range(5):
            self.coins.add(Coin(random.randint(50, WIDTH-50), HEIGHT-100))
        
        # Pet
        self.pets.add(Pet(WIDTH - 50, HEIGHT - 100))

class Level2(Level):
    def create_level(self):
        # Platforms
        platform_positions = [
            (0, HEIGHT - 50), (200, HEIGHT - 150),
            (400, HEIGHT - 250), (600, HEIGHT - 150)
        ]
        for x, y in platform_positions:
            platform = pygame.sprite.Sprite()
            platform.image = pygame.Surface((200, 20))
            platform.image.fill(WHITE)
            platform.rect = platform.image.get_rect(topleft=(x, y))
            self.platforms.add(platform)
        
        # Coins
        for _ in range(8):
            self.coins.add(Coin(random.randint(50, WIDTH-50), random.randint(100, HEIGHT-100)))
        
        # Enemies
        self.enemies.add(Enemy(300, HEIGHT - 200, 150))
        self.enemies.add(Enemy(500, HEIGHT - 300, 100))
        
        # Pets
        self.pets.add(Pet(WIDTH - 100, HEIGHT - 300))

class Level3(Level):
    def create_level(self):
        # Moving platforms
        self.moving_platforms.add(MovingPlatform(100, HEIGHT-200, move_x=2))
        self.moving_platforms.add(MovingPlatform(400, HEIGHT-300, move_y=1))
        
        # Coins
        for _ in range(10):
            self.coins.add(Coin(random.randint(50, WIDTH-50), random.randint(100, HEIGHT-100)))
        
        # Enemies
        self.enemies.add(Enemy(200, HEIGHT-250, 200))
        self.enemies.add(Enemy(600, HEIGHT-350, 150))
        
        # Pets
        self.pets.add(Pet(WIDTH//2, 100))

class Level4(Level):
    def create_level(self):
        # Ice platforms
        for x in range(0, WIDTH, 150):
            platform = pygame.sprite.Sprite()
            platform.image = pygame.Surface((150, 20))
            platform.image.fill((200, 200, 255))
            platform.rect = platform.image.get_rect(topleft=(x, HEIGHT - 50))
            self.platforms.add(platform)
        
        # Dangerous lava
        self.enemies.add(Enemy(0, HEIGHT-30, patrol_range=WIDTH))
        self.enemies.add(Enemy(0, HEIGHT-25, patrol_range=WIDTH))
        
        # Coins
        for _ in range(15):
            self.coins.add(Coin(random.randint(50, WIDTH-50), random.randint(100, HEIGHT-100)))
        
        # Pets
        self.pets.add(Pet(WIDTH - 50, 50))

class Game:
    def __init__(self):
        self.reset_game()
        
    def reset_game(self):
        self.player = Player()
        self.current_level = 1
        self.levels = [Level1(), Level2(), Level3(), Level4()]
        self.load_level()
        self.running = True
        self.font = pygame.font.Font(None, 36)

    def load_level(self):
        self.level = self.levels[self.current_level - 1]
        self.level.reset()
        self.player.pos = pygame.math.Vector2(50, HEIGHT - 100)
        self.player.velocity = pygame.math.Vector2(0, 0)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.pos.x -= 5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.pos.x += 5
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and not self.player.jumping:
            self.player.velocity.y = -15
            self.player.jumping = True

    def check_collisions(self):
        # Platform collisions
        for platform in [*self.level.platforms, *self.level.moving_platforms]:
            if self.player.rect.colliderect(platform.rect):
                if self.player.velocity.y > 0:
                    self.player.pos.y = platform.rect.top
                    self.player.velocity.y = 0
                    self.player.jumping = False
        
        # Coin collection
        for coin in self.level.coins:
            if self.player.rect.colliderect(coin.rect):
                self.player.coins += 1
                coin.kill()
        
        # Pet collection
        for pet in self.level.pets:
            if self.player.rect.colliderect(pet.rect):
                self.player.pets.append("Pet")
                pet.kill()
        
        # Enemy collision
        for enemy in self.level.enemies:
            if self.player.rect.colliderect(enemy.rect):
                self.player.health -= 0.5
                if self.player.health <= 0:
                    self.game_over()
        
        # Level completion
        if len(self.level.pets) == 0 and self.player.rect.x > WIDTH - 100:
            self.current_level += 1
            if self.current_level > len(self.levels):
                self.victory()
            else:
                self.load_level()

    def game_over(self):
        text = self.font.render("Game Over! Press R to restart", True, WHITE)
        screen.blit(text, (WIDTH//2 - 200, HEIGHT//2))
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
                        waiting = False

    def victory(self):
        text = self.font.render("Congratulations! You won!", True, WHITE)
        screen.blit(text, (WIDTH//2 - 150, HEIGHT//2))
        pygame.display.flip()
        pygame.time.wait(3000)
        self.running = False

    def draw_hud(self):
        coin_text = self.font.render(f"Coins: {self.player.coins}", True, WHITE)
        pet_text = self.font.render(f"Pets: {len(self.player.pets)}", True, WHITE)
        health_text = self.font.render(f"Health: {int(self.player.health)}", True, WHITE)
        level_text = self.font.render(f"Level: {self.current_level}/4", True, WHITE)
        
        screen.blit(coin_text, (10, 10))
        screen.blit(pet_text, (10, 50))
        screen.blit(health_text, (10, 90))
        screen.blit(level_text, (WIDTH - 150, 10))

    def run(self):
        while self.running:
            screen.fill(BLACK)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.handle_input()
            self.check_collisions()
            
            self.player.update()
            self.level.enemies.update()
            self.level.moving_platforms.update()
            
            self.level.platforms.draw(screen)
            self.level.moving_platforms.draw(screen)
            self.level.coins.draw(screen)
            self.level.enemies.draw(screen)
            self.level.pets.draw(screen)
            screen.blit(self.player.image, self.player.rect)
            
            self.draw_hud()
            
            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
