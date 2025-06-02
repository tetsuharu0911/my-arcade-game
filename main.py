import pygame
import sys
import random # For randomizing ball's initial direction

# --- Pygame Initialization ---
pygame.init()

# --- Screen Setup ---
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Block Breaker Game - Paddle Collision")

# --- Colors (RGB) ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0) # Ball color
PADDLE_COLOR = (0, 128, 128)
BLOCK_COLORS = [
    (0, 150, 0),  # Dark Green
    (150, 150, 0), # Yellow-ish
    (150, 0, 150), # Purple
    (0, 150, 150)  # Cyan-ish
]

# --- Class Definitions ---
class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        # Create the image of the paddle
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        # Get the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()
        # Set the initial position of the paddle
        self.rect.x = x
        self.rect.y = y
        self.speed = 10 # Speed of the paddle

    def move(self, direction):
        # Move the paddle left or right
        if direction == "left":
            self.rect.x -= self.speed
        if direction == "right":
            self.rect.x += self.speed

        # Keep the paddle within the screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width

    def draw(self, surface):
        # Draw the paddle onto the given surface
        surface.blit(self.image, self.rect)

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, color, speed_x, speed_y):
        super().__init__()
        # Create the image of the ball
        self.radius = radius
        # Create a surface that can be transparent
        self.image = pygame.Surface([radius*2, radius*2], pygame.SRCALPHA)
        # Draw the ball (circle) on this surface
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        # Get the rectangle object for positioning
        self.rect = self.image.get_rect(center=(x, y)) # Position by center
        
        self.speed_x = speed_x
        self.speed_y = speed_y

    def move(self):
        # Move the ball based on its speed
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def bounce_walls(self, screen_width_param, screen_height_param):
        # Bounce off the left or right wall
        if self.rect.left <= 0 or self.rect.right >= screen_width_param:
            self.speed_x *= -1
        # Bounce off the top wall
        if self.rect.top <= 0:
            self.speed_y *= -1
        # We will handle losing a life when ball hits bottom later
        if self.rect.bottom >= screen_height_param:
            # For now, let's reset the ball or make it bounce for testing
            # self.speed_y *= -1 # Temporary bounce
            # Reset ball to a position for testing (or implement game over)
            self.rect.x = screen_width_param // 2
            self.rect.y = screen_height_param // 2
            self.speed_y = abs(self.speed_y) * random.choice([-1, 1]) # Randomize direction slightly
            self.speed_x = abs(self.speed_x) * random.choice([-1, 1])

    def draw(self, surface):
        # Draw the ball onto the given surface
        surface.blit(self.image, self.rect)

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        # Create the image of the block
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        # Get the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()
        # Set the position of the block
        self.rect.x = x
        self.rect.y = y

    def draw(self, surface):
        # Draw the block onto the given surface
        surface.blit(self.image, self.rect)

# --- Game Object Creation ---
# Paddle
paddle_width = 100
paddle_height = 20
paddle_x = (screen_width - paddle_width) // 2
paddle_y = screen_height - paddle_height - 30
paddle = Paddle(paddle_x, paddle_y, paddle_width, paddle_height, PADDLE_COLOR)

# Ball
ball_radius = 10
ball_x = screen_width // 2
ball_y = paddle_y - ball_radius - 5 # Start just above the paddle
ball_speed_x = random.choice([-5, 5])
ball_speed_y = -5 # Move upwards initially
ball = Ball(ball_x, ball_y, ball_radius, RED, ball_speed_x, ball_speed_y)

# Block
all_blocks = []
block_width = 70
block_height = 20
block_padding = 10
num_rows = 4
num_cols = (screen_width - block_padding) // (block_width + block_padding)

# Top-left corner for the block grid
start_x = block_padding
start_y = 50

for row in range(num_rows):
    for col in range(num_cols):
        # Calculate x and y position for each block
        block_x = start_x + col * (block_width + block_padding)
        block_y = start_y + row * (block_height + block_padding)
        # Choose a color based on the row
        block_color = BLOCK_COLORS[row % len(BLOCK_COLORS)]
        # Create a new block
        block = Block(block_x, block_y, block_width, block_height, block_color)
        all_blocks.append(block)

# --- Game Loop Control ---
clock = pygame.time.Clock()
running = True

# --- Game Loop ---
while running:
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key Input Processing
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.move("left")
    if keys[pygame.K_RIGHT]:
        paddle.move("right")

    # Game Logic
    ball.move()
    ball.bounce_walls(screen_width, screen_height)
    
    # --- Ball and Paddle Collision Detection
    # The 'colliderect' method checks if two Rect objects overlap
    if paddle.rect.colliderect(ball.rect):
        # Check if ball is moving downward (or towards the paddle top)
        if ball.speed_y > 0:
            ball.speed_y *= -1
            
            offset = (ball.rect.centerx - paddle.rect.centerx) / (paddle_width / 2)
            ball.speed_x = offset * 5

            ball.rect.bottom = paddle.rect.top

    # Drawing
    screen.fill(BLACK)  # Fill background
    paddle.draw(screen) # Draw paddle
    ball.draw(screen)   # Draw ball

    # Draw all the blocks
    for block_item in all_blocks:
        block_item.draw(screen)
    # Update Display
    pygame.display.flip()

    # Frame Rate Control
    clock.tick(60) # Aim for 60 FPS

# --- Pygame Exit ---
pygame.quit()
sys.exit()