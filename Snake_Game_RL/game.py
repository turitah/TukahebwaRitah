import pygame
import random
from enum import Enum
from collections import namedtuple
import time

pygame.init()

# Constants
BLOCK_SIZE = 20
INITIAL_SPEED = 8  # Starting speed
MAX_SPEED = 20  # Maximum speed cap

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple("Point", "x y")

# Colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
LIGHT_GREEN = (100, 255, 100)

class SnakeGame:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake RL - Manual Control")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.reset()
    
    def reset(self):
        """Reset the game state"""
        self.direction = Direction.RIGHT
        self.current_speed = INITIAL_SPEED
        
        # Start snake in the middle with 3 segments
        self.head = Point(self.width // 2, self.height // 2)
        self.snake = [
            self.head,
            Point(self.head.x - BLOCK_SIZE, self.head.y),
            Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)
        ]
        
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0
        self.game_over = False
        
        # For display purposes
        self.last_move_time = time.time()
        self.move_delay = 0.15  # Seconds between moves
    
    def _place_food(self):
        """Place food at random location, not on snake"""
        attempts = 0
        max_attempts = 1000
        
        while attempts < max_attempts:
            x = random.randint(0, (self.width - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (self.height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            food_point = Point(x, y)
            
            # Make sure food doesn't spawn on snake
            if food_point not in self.snake:
                self.food = food_point
                return
            
            attempts += 1
        
        # If we can't place food, place it in a corner (fallback)
        self.food = Point(0, 0)
    
    def play_step(self, action=None):
        """Execute one step of the game"""
        if self.game_over:
            return 0, True, self.score
        
        # Handle keyboard input if no action provided
        if action is None:
            action = self._handle_keyboard()
        
        current_time = time.time()
        
        # Control speed based on score
        if self.score < 5:
            self.move_delay = 0.15
        elif self.score < 10:
            self.move_delay = 0.12
        elif self.score < 20:
            self.move_delay = 0.10
        elif self.score < 30:
            self.move_delay = 0.08
        else:
            self.move_delay = 0.06
        
        # Wait for the appropriate delay
        if current_time - self.last_move_time < self.move_delay:
            self._update_ui()
            return 0, False, self.score
        
        self.last_move_time = current_time
        self.frame_iteration += 1
        
        # Handle quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # Move the snake
        self._move(action)
        self.snake.insert(0, self.head)
        
        reward = 0
        
        # Check for collisions
        if self._is_collision() or self.frame_iteration > 100 * len(self.snake):
            self.game_over = True
            reward = -10
            return reward, True, self.score
        
        # Check if food was eaten
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()
        
        # Update UI
        self._update_ui()
        self.clock.tick(60)
        
        return reward, False, self.score
    
    def _is_collision(self, pt=None):
        """Check if the snake collides with walls or itself"""
        if pt is None:
            pt = self.head
        
        # Wall collision
        if pt.x > self.width - BLOCK_SIZE or pt.x < 0:
            return True
        if pt.y > self.height - BLOCK_SIZE or pt.y < 0:
            return True
        
        # Self collision
        if pt in self.snake[1:]:
            return True
        
        return False
    
    def _move(self, action):
        """Move the snake in the given direction"""
        directions = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = directions.index(self.direction)
        
        # Determine new direction based on action
        if action == [1, 0, 0]:  # Continue straight
            new_direction = directions[idx]
        elif action == [0, 1, 0]:  # Turn right
            next_idx = (idx + 1) % 4
            new_direction = directions[next_idx]
        else:  # Turn left
            next_idx = (idx - 1) % 4
            new_direction = directions[next_idx]
        
        # Prevent moving backwards
        if (new_direction == Direction.UP and self.direction == Direction.DOWN) or \
           (new_direction == Direction.DOWN and self.direction == Direction.UP) or \
           (new_direction == Direction.LEFT and self.direction == Direction.RIGHT) or \
           (new_direction == Direction.RIGHT and self.direction == Direction.LEFT):
            new_direction = self.direction
        
        self.direction = new_direction
        
        # Calculate new head position
        x, y = self.head.x, self.head.y
        
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
        
        self.head = Point(x, y)
    
    def _handle_keyboard(self):
        """Handle keyboard input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    self.reset()
                    return [1, 0, 0]
                elif event.key == pygame.K_RIGHT:
                    return [0, 1, 0]  # Turn right
                elif event.key == pygame.K_LEFT:
                    return [0, 0, 1]  # Turn left
                elif event.key == pygame.K_UP:
                    return [1, 0, 0]  # Go straight
                elif event.key == pygame.K_r:  # Press R to restart
                    self.reset()
                    return [1, 0, 0]
        
        return [1, 0, 0]  # Default: go straight
    
    def _update_ui(self):
        """Update the game display"""
        self.display.fill(BLACK)
        
        # Draw snake
        for i, pt in enumerate(self.snake):
            # Head is brighter
            if i == 0:
                color = LIGHT_GREEN
            else:
                intensity = max(50, 255 - (i * 5))
                color = (0, intensity, 0)
            
            pygame.draw.rect(
                self.display,
                color,
                pygame.Rect(pt.x, pt.y, BLOCK_SIZE - 1, BLOCK_SIZE - 1)
            )
            # Border
            pygame.draw.rect(
                self.display,
                (0, 50, 0),
                pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE),
                1
            )
        
        # Draw food
        if self.food:
            pygame.draw.rect(
                self.display,
                RED,
                pygame.Rect(
                    self.food.x,
                    self.food.y,
                    BLOCK_SIZE,
                    BLOCK_SIZE
                )
            )
        
        # Display info
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.display.blit(score_text, (10, 10))
        
        length_text = self.small_font.render(f"Length: {len(self.snake)}", True, WHITE)
        self.display.blit(length_text, (10, 50))
        
        # Controls info
        controls_text = self.small_font.render("Controls: Arrow Keys | R: Restart", True, WHITE)
        self.display.blit(controls_text, (10, self.height - 30))
        
        # Game over message
        if self.game_over:
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.display.blit(overlay, (0, 0))
            
            game_over_text = self.font.render("GAME OVER", True, RED)
            text_rect = game_over_text.get_rect(center=(self.width//2, self.height//2 - 30))
            self.display.blit(game_over_text, text_rect)
            
            score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            score_rect = score_text.get_rect(center=(self.width//2, self.height//2 + 30))
            self.display.blit(score_text, score_rect)
            
            restart_text = self.small_font.render("Press any key to restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=(self.width//2, self.height//2 + 80))
            self.display.blit(restart_text, restart_rect)
        
        pygame.display.flip() 