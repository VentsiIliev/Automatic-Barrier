import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
THRESHOLD_LINE_COLOR = (0, 0, 255)  # Blue color for the threshold lines
BARRIER_WIDTH = 10
BARRIER_HEIGHT = HEIGHT  # Full height of the window
CAR_WIDTH, CAR_HEIGHT = 50, 30
CAR_SPEED = 5
DISTANCE_FROM_BARRIER = 150  # Distance from the barrier to both thresholds
OPEN_THRESHOLD = WIDTH // 2 - DISTANCE_FROM_BARRIER  # Move the open threshold further away
CLOSE_THRESHOLD = WIDTH // 2 + DISTANCE_FROM_BARRIER  # Keep the same distance for the close threshold
DEBOUNCE_DELAY = 500  # Delay in milliseconds to prevent flickering

# Mock license plates
LICENSE_PLATES = ["ABC1234", "XYZ5678", "LMN9101", "JKL2345"]

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Car Park Barrier Simulation')

# Barrier class
class Barrier:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - BARRIER_WIDTH // 2, 0, BARRIER_WIDTH, BARRIER_HEIGHT)
        self.open = False
        self.color = RED  # Start with barrier closed (red)
        self.last_change_time = pygame.time.get_ticks()

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def open_barrier(self):
        if not self.open and pygame.time.get_ticks() - self.last_change_time > DEBOUNCE_DELAY:
            self.open = True
            self.color = GREEN
            self.last_change_time = pygame.time.get_ticks()

    def close_barrier(self):
        if self.open and pygame.time.get_ticks() - self.last_change_time > DEBOUNCE_DELAY:
            self.open = False
            self.color = RED
            self.last_change_time = pygame.time.get_ticks()

# Car class
class Car:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, CAR_WIDTH, CAR_HEIGHT)
        self.speed = CAR_SPEED
        self.license_plate = random.choice(LICENSE_PLATES)  # Randomly assign a license plate

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)
        # Draw license plate
        font = pygame.font.SysFont(None, 24)
        text = font.render(self.license_plate, True, (0, 0, 0))
        screen.blit(text, (self.rect.x + 5, self.rect.y + 5))

# Main loop
def main():
    barrier = Barrier()
    car = Car(50, HEIGHT // 2 - CAR_HEIGHT // 2)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        car.move(keys)

        # Check if the car is between the open and close thresholds
        car_between_lines = OPEN_THRESHOLD < car.rect.x < CLOSE_THRESHOLD

        # Open the barrier if the car is between the lines
        if car_between_lines:
            barrier.open_barrier()
        else:
            barrier.close_barrier()

        # Update display
        screen.fill((0, 0, 0))  # Clear the screen
        barrier.draw()
        car.draw()

        # Draw threshold lines
        pygame.draw.line(screen, THRESHOLD_LINE_COLOR, (OPEN_THRESHOLD, 0), (OPEN_THRESHOLD, HEIGHT), 2)
        pygame.draw.line(screen, THRESHOLD_LINE_COLOR, (CLOSE_THRESHOLD, 0), (CLOSE_THRESHOLD, HEIGHT), 2)

        pygame.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    main()
