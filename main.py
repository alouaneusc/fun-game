import pygame, sys, random


# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 800
PLAYER_SIZE = 50
PLAYER_SPEED = 5
DEFENSE_SPEED = 10
game_over = False
score = 0
font = pygame.font.Font(None, 36)


# Colors
WHITE = (255, 255, 255)



# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Run Edd, Run!")

#player image
players = pygame.image.load('pics/edd.png').convert_alpha()
players = pygame.transform.scale(players, (PLAYER_SIZE, PLAYER_SIZE))

#defense image(s)
opps = pygame.image.load('pics/thecc.png').convert_alpha()
opps = pygame.transform.scale(opps, (PLAYER_SIZE // 1.5, PLAYER_SIZE // 1.5))
#field
field = pygame.image.load('pics/butchers.png').convert()
field = pygame.transform.scale(field, (WIDTH, HEIGHT))

class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - PLAYER_SIZE - 20

    def move(self, direction):
        if direction == "left":
            self.x -= PLAYER_SPEED
        elif direction == "right":
            self.x += PLAYER_SPEED
        elif direction == "up":
            self.y -= PLAYER_SPEED
        elif direction == "down":
            self.y += PLAYER_SPEED

    def draw(self):
        screen.blit(players, (self.x, self.y))
class Defense:
    def __init__(self):
        self.x = random.randint(0, WIDTH  - PLAYER_SIZE)  # X position is fixed at zero
        self.y = 0
        self.points = 0
        self.score_incremented = False
        self.defense_images = [
            pygame.image.load('pics/fsf.png').convert_alpha(),
            pygame.image.load('pics/painted.png').convert_alpha(),
            pygame.image.load('pics/rake.png').convert_alpha(),
            pygame.image.load('pics/thecc.png').convert_alpha(),
            pygame.image.load('pics/tswift.png').convert_alpha(),
            pygame.image.load('pics/yeti.png').convert_alpha(),
        ]
        self.defense_image = random.choice(self.defense_images)
        self.defense_image = pygame.transform.scale(self.defense_image, (PLAYER_SIZE, PLAYER_SIZE))

    def move_down(self):
        self.y += DEFENSE_SPEED
    def draw(self):
        defense_rect = pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, PLAYER_SIZE/1.5, PLAYER_SIZE/1.5))
        screen.blit(self.defense_image,defense_rect)
    def draw_score(self):
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 75))

    def check_collision(self):
        global score
        if not self.score_incremented and self.y >= HEIGHT - (PLAYER_SIZE / 2):
            score += 1
            self.score_incremented = True

player = Player()
defense = Defense()
defenses = []  # List to hold defense blocks

# Game loop
running = True
while running and not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move("left")
    if keys[pygame.K_RIGHT]:
        player.move("right")
    if keys[pygame.K_UP]:
        player.move("up")
    if keys[pygame.K_DOWN]:
        player.move("down")


    player.x = max(0, min(player.x, WIDTH - PLAYER_SIZE))
    player.y = max(0, min(player.y, HEIGHT - PLAYER_SIZE))

    screen.fill((0, 0, 0))  # Clear the screen
    screen.blit(field, (0, 0))
    player.draw()  # Draw the player
    # Add a new defense block to the list at a certain interval
    if random.randint(0, 100) < 2:
        defenses.append(Defense())

    # Draw and update all defense blocks
    for defense in defenses:
        defense.move_down()
        defense.draw()

        # Create a Rect for defense position
        defense_rect = pygame.Rect(defense.x, defense.y, PLAYER_SIZE // 2, PLAYER_SIZE // 2)
        # Blit the image onto the screen at the defense position
        screen.blit(defense.defense_image, defense_rect.topleft)

        # Check for collision between player and defense
        if defense_rect.colliderect(pygame.Rect(player.x, player.y, PLAYER_SIZE, PLAYER_SIZE)):
            game_over = True  # Set the game over flag

        defense.check_collision()

    defense.draw_score()  # Draw the score

    pygame.display.flip()  # Update the display
    pygame.time.Clock().tick(60)  # Limit the frame rate

pygame.quit()
sys.exit()
