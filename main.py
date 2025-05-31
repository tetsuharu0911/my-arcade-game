import pygame
import sys
import random # For randomizing ball's initial direction

# --- Pygame Initialization ---
pygame.init()

# --- Screen Setup ---
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Block Breaker Game")

# --- Colors (RGB) ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0) # Ball color
PADDLE_COLOR = (0, 128, 128)

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
        # If ball hits bottom (lose condition, for now just bounce)
        # We will handle losing a life later
        if self.rect.bottom >= screen_height_param:
            self.speed_y *= -1 # Temporary bounce, will be game over or lose life

    def draw(self, surface):
        # Draw the ball onto the given surface
        surface.blit(self.image, self.rect)

# --- Game Object Creation ---
paddle_width = 100
paddle_height = 20
paddle_x = (screen_width - paddle_width) // 2
paddle_y = screen_height - paddle_height - 30
paddle = Paddle(paddle_x, paddle_y, paddle_width, paddle_height, PADDLE_COLOR)

ball_radius = 10
ball_x = screen_width // 2
ball_y = paddle_y - ball_radius - 5 # Start just above the paddle
# Randomize initial ball direction
ball_speed_x = random.choice([-5, 5])
ball_speed_y = -5 # Move upwards initially
ball = Ball(ball_x, ball_y, ball_radius, RED, ball_speed_x, ball_speed_y)

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
    # Collision detection between ball and paddle will be added here later

    # Drawing
    screen.fill(BLACK)  # Fill background
    paddle.draw(screen) # Draw paddle
    ball.draw(screen)   # Draw ball

    # Update Display
    pygame.display.flip()

    # Frame Rate Control
    clock.tick(60) # Aim for 60 FPS

# --- Pygame Exit ---
pygame.quit()
sys.exit()