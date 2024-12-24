import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1330, 700
BG_COLOR = (255, 29, 90)
FPS = 60

# Game Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)  # Initialize font

# Load Menu Background Image
try:
    menu_bg = pygame.image.load('menu_bg.png').convert()
    menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT))
    print(f"Loaded menu background image with size: {menu_bg.get_size()}")
except pygame.error as e:
    print(f"Error loading menu background image: {e}")
    menu_bg = pygame.Surface((WIDTH, HEIGHT))
    menu_bg.fill(BG_COLOR)

# Load background music
try:
    pygame.mixer.music.load('background_music.mp3')
    pygame.mixer.music.play(-1)  # Play music in a loop
except pygame.error as e:
    print(f"Error loading background music: {e}")

# Load sound effects
try:
    jump_sound = pygame.mixer.Sound('jump.wav')
    hit_sound = pygame.mixer.Sound('hit.wav')
    hit_sound.set_volume(0.3)  # Adjust the collision sound volume
except pygame.error as e:
    print(f"Error loading sound effects: {e}")
# Function to save high score
def save_high_score(high_score): 
    with open(HIGH_SCORE_FILE, "w") as file: 
        file.write(str(high_score))

# Function to load high score 
def load_high_score(): 
    if os.path.exists(HIGH_SCORE_FILE): 
	    with open(HIGH_SCORE_FILE, "r") as file: 
	        return int(file.read())
#    return 0
# Character Class
class Character:
    def __init__(self, race, char_class):
        try:
            self.image = pygame.image.load('character.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 50))
            print(f"Loaded and resized character image with size: {self.image.get_size()}")
        except pygame.error as e:
            print(f"Error loading character image: {e}")
            self.image = pygame.Surface((50, 50))
            self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = HEIGHT - self.rect.height - 10
        self.vel_y = 0
        self.gravity = 1
        self.jump_power = 15
        self.char_class = char_class
        self.race = race
        self.lives = 5  # Initial lives

    def jump(self):
        if self.rect.bottom == HEIGHT - 10:
            self.vel_y = self.jump_power
            jump_sound.play()
            
    def check_collision(self, obstacles):
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                self.lives -= 1
                obstacles.remove(obstacle)
                hit_sound.play()
                break

    def break_obstacle(self, obstacles):
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                obstacles.remove(obstacle)
                hit_sound.play()
                return True
        return False

    def update(self):
        self.rect.y += self.vel_y
        if self.rect.bottom < HEIGHT - 10:
            self.vel_y += self.gravity
        else:
            self.rect.bottom = HEIGHT - 10
            self.vel_y = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

# Obstacle Class
class Obstacle:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH, HEIGHT - 50, 15, 100)
        self.color = (3, 5, 90)
        self.speed = 3

    def update(self):
        self.rect.x -= 5

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

# Power-Up Class
class PowerUp:
    def __init__(self, x, y):
        try:
            self.image = pygame.image.load('powerup.png').convert_alpha()
        except pygame.error as e:
            print(f"Error loading power-up image: {e}")
            self.image = pygame.Surface((30, 30))
            self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.type = random.choice(['extra_life', 'speed_boost'])

    def apply(self, character):
        if self.type == 'extra_life':
            character.lives += 1
        elif self.type == 'speed_boost':
            character.jump_power = -20

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

# Function to display the menu
def display_menu():
    menu_text = [
        "Select your character:",
        "1. Human - Warrior",
        "2. Elf - Archer",
        "3. Dwarf - Miner",
        "Press the number key to choose."
    ]
    screen.blit(menu_bg, (0, 0))  # Draw background image
    for i, line in enumerate(menu_text):
        text = font.render(line, True, (255, 255, 255))
        screen.blit(text, (150, 150 + i * 40))
    pygame.display.flip()

# Function to handle character selection
def select_character():
    display_menu()
    selected = False
    race = ""
    char_class = ""
    while not selected:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    race, char_class = "Human", "Warrior"
                    selected = True
                if event.key == pygame.K_2:
                    race, char_class = "Elf", "Archer"
                    selected = True
                if event.key == pygame.K_3:
                    race, char_class = "Dwarf", "Miner"
                    selected = True
    return race, char_class

# Function to display lives on the screen
def display_lives(screen, lives):
    text = font.render(f"Lives: {lives}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

# Function to display score
def display_score(screen, score, high_score):
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    high_score_text = font.render(f"High Score: {high_score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 40))  # Adjusted position
    screen.blit(high_score_text, (10, 70))  # Adjusted position

# Function to increase difficulty
def increase_difficulty(obstacles):
    for obstacle in obstacles:
        obstacle.rect.x += 2  # Increase speed of obstacles

# Main game loop
def main():
    race, char_class = select_character()
    character = Character(race, char_class)
    obstacles = []
    power_ups = []
    running = True
    level_up_counter = 0
    score = 0
    high_score = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Jump action
                    character.jump()
                if event.key == pygame.K_b:  # Break obstacle action
                    character.break_obstacle(obstacles)

        character.update()
        character.check_collision(obstacles)  # Check for collisions

        for obstacle in obstacles:
            obstacle.update()
        for power_up in power_ups:
            if character.rect.colliderect(power_up.rect):
                power_up.apply(character)
                power_ups.remove(power_up)

        if character.lives <= 0:
            if score > high_score:
                high_score = score
            running = False

        if level_up_counter >= 500:  # Increase difficulty every 500 ticks
            increase_difficulty(obstacles)
            level_up_counter = 0

        level_up_counter += 1

        obstacles = [obstacle for obstacle in obstacles if obstacle.rect.x > -20]
        if random.randint(1, 100) == 1:
            obstacles.append(Obstacle())
        if random.randint(1, 300) == 1:  # Randomly place power-ups
            power_ups.append(PowerUp(random.randint(WIDTH, WIDTH + 200), HEIGHT - 60))

        score += 1
        screen.fill(BG_COLOR)
        character.draw(screen)
        for obstacle in obstacles:
            obstacle.draw(screen)
        for power_up in power_ups:
            power_up.draw(screen)
        display_lives(screen, character.lives)  # Display lives
        display_score(screen, score, high_score)  # Display score

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


# Start the game
if __name__ == "__main__":
    main()