import pygame
import random

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

# Initialize screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Adventure Quest")
clock = pygame.time.Clock()

# Player class
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

    def update(self):
        self.velocity.y += 0.5  # Gravity
        self.pos += self.velocity
        self.rect.midbottom = self.pos

# Coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center=(x, y))

# Pet class
class Pet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((24, 24))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(x, y))

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = 1
        self.speed = 2

    def update(self):
        self.rect.x += self.direction * self.speed
        if self.rect.x > WIDTH - 50 or self.rect.x < 50:
            self.direction *= -1

# Base Level class
class Level:
    def __init__(self):
        self.platforms = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.pets = pygame.sprite.Group()
        self.exit = None

    def create_level(self):
        pass

# Level 1
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
            self.coins.add(Coin(random.randint(50, WIDTH-50), random.randint(100, HEIGHT-100)))
        
        # Pet
        self.pets.add(Pet(WIDTH - 50, HEIGHT - 100))

# Level 2
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
        self.enemies.add(Enemy(300, HEIGHT - 200))
        self.enemies.add(Enemy(500, HEIGHT - 300))
        
        # Pet
        self.pets.add(Pet(WIDTH - 100, HEIGHT - 300))

# Game manager
class Game:
    def __init__(self):
        self.player = Player()
        self.current_level = 1
        self.levels = [Level1(), Level2()]
        self.load_level()
        self.running = True
        self.font = pygame.font.Font(None, 36)

    def load_level(self):
        self.level = self.levels[self.current_level - 1]
        self.level.create_level()
        self.player.pos = pygame.math.Vector2(50, HEIGHT - 100)
        self.player.velocity = pygame.math.Vector2(0, 0)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.pos.x -= 5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.pos.x += 5
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.player.velocity.y == 0:
            self.player.velocity.y = -15

    def check_collisions(self):
        # Platform collisions
        for platform in self.level.platforms:
            if self.player.rect.colliderect(platform.rect):
                if self.player.velocity.y > 0:
                    self.player.pos.y = platform.rect.top
                    self.player.velocity.y = 0
        
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
                self.player.health -= 10
                if self.player.health <= 0:
                    self.game_over()
        
        # Check exit condition
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
                        self.__init__()
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
        health_text = self.font.render(f"Health: {self.player.health}", True, WHITE)
        level_text = self.font.render(f"Level: {self.current_level}", True, WHITE)
        
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
            
            self.level.platforms.draw(screen)
            self.level.coins.draw(screen)
            self.level.enemies.draw(screen)
            self.level.pets.draw(screen)
            screen.blit(self.player.image, self.player.rect)
            
            self.draw_hud()
            
            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
