import pygame
import sys
import random
import os
from pygame.locals import *
import time
import math

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 750  # Increased from 600 to 750
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('Yacht Dice Game')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)
LIGHT_GREEN = (200, 255, 200)

# Fonts
font_small = pygame.font.SysFont('Arial', 20)
font_medium = pygame.font.SysFont('Arial', 30)
font_large = pygame.font.SysFont('Arial', 40)

# Game constants
MAX_PLAYERS = 4
MIN_PLAYERS = 2
DICE_COUNT = 5
MAX_ROLLS = 3

# Create images directory if it doesn't exist
if not os.path.exists('images'):
    os.makedirs('images')

# Dice images - we'll draw them programmatically
dice_images = []

def generate_dice_images(size=60):
    """Generate dice face images"""
    images = []
    for value in range(1, 7):
        # Create a surface for the dice
        dice_img = pygame.Surface((size, size))
        dice_img.fill(WHITE)
        
        # Draw border
        pygame.draw.rect(dice_img, BLACK, (0, 0, size, size), 2)
        
        # Draw dots based on value
        dot_radius = size // 10
        if value == 1:
            # Center dot
            pygame.draw.circle(dice_img, BLACK, (size // 2, size // 2), dot_radius)
        elif value == 2:
            # Top-left and bottom-right dots
            pygame.draw.circle(dice_img, BLACK, (size // 4, size // 4), dot_radius)
            pygame.draw.circle(dice_img, BLACK, (3 * size // 4, 3 * size // 4), dot_radius)
        elif value == 3:
            # Top-left, center, and bottom-right dots
            pygame.draw.circle(dice_img, BLACK, (size // 4, size // 4), dot_radius)
            pygame.draw.circle(dice_img, BLACK, (size // 2, size // 2), dot_radius)
            pygame.draw.circle(dice_img, BLACK, (3 * size // 4, 3 * size // 4), dot_radius)
        elif value == 4:
            # Four corners
            pygame.draw.circle(dice_img, BLACK, (size // 4, size // 4), dot_radius)
            pygame.draw.circle(dice_img, BLACK, (3 * size // 4, size // 4), dot_radius)
            pygame.draw.circle(dice_img, BLACK, (size // 4, 3 * size // 4), dot_radius)
            pygame.draw.circle(dice_img, BLACK, (3 * size // 4, 3 * size // 4), dot_radius)
        elif value == 5:
            # Four corners and center
            pygame.draw.circle(dice_img, BLACK, (size // 4, size // 4), dot_radius)
            pygame.draw.circle(dice_img, BLACK, (3 * size // 4, size // 4), dot_radius)
            pygame.draw.circle(dice_img, BLACK, (size // 2, size // 2), dot_radius)
            pygame.draw.circle(dice_img, BLACK, (size // 4, 3 * size // 4), dot_radius)
            pygame.draw.circle(dice_img, BLACK, (3 * size // 4, 3 * size // 4), dot_radius)
        elif value == 6:
            # Six dots - 3 on each side
            pygame.draw.circle(dice_img, BLACK, (size // 4, size // 4), dot_radius)
            pygame.draw.circle(dice_img, BLACK, (size // 4, size // 2), dot_radius)
            pygame.draw.circle(dice_img, BLACK, (size // 4, 3 * size // 4), dot_radius)
            pygame.draw.circle(dice_img, BLACK, (3 * size // 4, size // 4), dot_radius)
            pygame.draw.circle(dice_img, BLACK, (3 * size // 4, size // 2), dot_radius)
            pygame.draw.circle(dice_img, BLACK, (3 * size // 4, 3 * size // 4), dot_radius)
        
        images.append(dice_img)
    return images

# Class to represent a die
class Die:
    def __init__(self, x, y, size=60):
        self.x = x
        self.y = y
        self.size = size
        self.value = random.randint(1, 6)
        self.locked = False
        self.rect = pygame.Rect(x, y, size, size)
        self.rolling = False
        self.roll_frames = 0
        self.roll_duration = 10  # Number of frames for rolling animation
        self.hover = False
    
    def roll(self):
        if not self.locked:
            self.rolling = True
            self.roll_frames = self.roll_duration
    
    def update(self):
        if self.rolling and self.roll_frames > 0:
            self.value = random.randint(1, 6)
            self.roll_frames -= 1
            if self.roll_frames <= 0:
                self.rolling = False
    
    def toggle_lock(self):
        if not self.rolling:
            self.locked = not self.locked
    
    def check_hover(self, pos):
        self.hover = self.rect.collidepoint(pos)
    
    def draw(self, surface):
        # Draw the die with some visual effects
        offset = 0
        if self.rolling:
            # Add a slight shake effect when rolling
            offset = random.randint(-2, 2)
        
        # Draw the die with a shadow effect
        shadow_offset = 3
        pygame.draw.rect(surface, DARK_GRAY, 
                         (self.x + shadow_offset, self.y + shadow_offset, self.size, self.size))
        
        # Draw the base of the die
        surface.blit(dice_images[self.value-1], (self.x + offset, self.y + offset))
        
        # Draw lock indicator
        if self.locked:
            lock_size = 15
            lock_rect = pygame.Rect(self.x + self.size - lock_size, self.y, lock_size, lock_size)
            pygame.draw.rect(surface, RED, lock_rect)
            pygame.draw.rect(surface, BLACK, lock_rect, 1)  # Add border
        
        # Draw hover effect
        if self.hover and not self.rolling:
            pygame.draw.rect(surface, YELLOW, self.rect, 2)

# Add Confetti class after the Die class
class Confetti:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(5, 10)
        self.color = random.choice([RED, GREEN, BLUE, YELLOW])
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(1, 3)
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-5, 5)
    
    def update(self):
        self.y += self.speed_y
        self.x += self.speed_x
        self.rotation += self.rotation_speed
    
    def draw(self, surface):
        # Create a surface for the confetti piece
        confetti = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.rect(confetti, self.color, (0, 0, self.size, self.size))
        
        # Rotate the confetti
        rotated = pygame.transform.rotate(confetti, self.rotation)
        # Get the rect for the rotated image
        rect = rotated.get_rect(center=(self.x, self.y))
        
        # Draw to the screen
        surface.blit(rotated, rect)

# Scoring categories
CATEGORIES = {
    'Aces': 'Sum of all 1s',
    'Twos': 'Sum of all 2s',
    'Threes': 'Sum of all 3s',
    'Fours': 'Sum of all 4s',
    'Fives': 'Sum of all 5s',
    'Sixes': 'Sum of all 6s',
    'Choice': 'Sum of all dice',
    'Four of a Kind': 'Four dice showing the same face',
    'Full House': 'Three of a kind and a pair',
    'Small Straight': 'Four sequential dice',
    'Large Straight': 'Five sequential dice',
    'Yacht': 'Five dice showing the same face'
}

# Class to handle scoring
class ScoreCard:
    def __init__(self):
        self.scores = {category: None for category in CATEGORIES}
    
    def calculate_possible_score(self, category, dice_values):
        """Calculate possible score for a given category with current dice"""
        
        if category == 'Aces':
            return sum(d for d in dice_values if d == 1)
        elif category == 'Twos':
            return sum(d for d in dice_values if d == 2)
        elif category == 'Threes':
            return sum(d for d in dice_values if d == 3)
        elif category == 'Fours':
            return sum(d for d in dice_values if d == 4)
        elif category == 'Fives':
            return sum(d for d in dice_values if d == 5)
        elif category == 'Sixes':
            return sum(d for d in dice_values if d == 6)
        elif category == 'Choice':
            return sum(dice_values)
        elif category == 'Four of a Kind':
            for value in range(1, 7):
                if dice_values.count(value) >= 4:
                    return value * 4
            return 0
        elif category == 'Full House':
            has_three = False
            has_two = False
            for value in range(1, 7):
                if dice_values.count(value) == 3:
                    has_three = True
                elif dice_values.count(value) == 2:
                    has_two = True
            if has_three and has_two:
                return sum(dice_values)
            return 0
        elif category == 'Small Straight':
            # Check for 1-2-3-4 or 2-3-4-5 or 3-4-5-6
            sorted_dice = sorted(dice_values)
            unique_sorted = sorted(set(sorted_dice))
            
            if len(unique_sorted) >= 4:
                for i in range(len(unique_sorted) - 3):
                    if unique_sorted[i] + 1 == unique_sorted[i+1] and \
                       unique_sorted[i+1] + 1 == unique_sorted[i+2] and \
                       unique_sorted[i+2] + 1 == unique_sorted[i+3]:
                        return 15
            return 0
        elif category == 'Large Straight':
            # Check for 1-2-3-4-5 or 2-3-4-5-6
            sorted_dice = sorted(dice_values)
            if sorted_dice == [1, 2, 3, 4, 5] or sorted_dice == [2, 3, 4, 5, 6]:
                return 30
            return 0
        elif category == 'Yacht':
            if all(d == dice_values[0] for d in dice_values):
                return 50
            return 0
        return 0
    
    def record_score(self, category, score):
        self.scores[category] = score
    
    def is_category_used(self, category):
        return self.scores[category] is not None
    
    def get_total_score(self):
        return sum(score for score in self.scores.values() if score is not None)

# Player class
class Player:
    def __init__(self, name):
        self.name = name
        self.scorecard = ScoreCard()
        self.total_score = 0
    
    def update_total_score(self):
        self.total_score = self.scorecard.get_total_score()

# Game state manager
class YachtGame:
    def __init__(self):
        self.state = 'menu'  # menu, setup, playing, game_over, help, scoreboard
        self.players = []
        self.current_player_index = 0
        self.dice = []
        self.rolls_left = MAX_ROLLS
        self.selected_category = None
        self.previous_state = None  # To remember where to return from help or scoreboard
        self.confetti = []
        self.time_at_game_over = 0
        
    def initialize_game(self, player_count):
        self.players = []
        for i in range(player_count):
            self.players.append(Player(f"Player {i+1}"))
        
        self.current_player_index = 0
        self.dice = []
        
        # Create dice with positions based on screen size
        positions = get_dice_positions()
        for i in range(DICE_COUNT):
            self.dice.append(Die(positions[i][0], positions[i][1]))
        
        self.rolls_left = MAX_ROLLS
        self.state = 'playing'
    
    def roll_dice(self):
        if self.rolls_left > 0:
            for die in self.dice:
                die.roll()
            self.rolls_left -= 1
    
    def update(self):
        # Update dice states
        for die in self.dice:
            die.update()
        
        # Update confetti
        if self.state == 'game_over':
            # Get current screen dimensions
            width, height = get_screen_dimensions()
            
            # Update existing confetti
            for conf in self.confetti[:]:
                conf.update()
                if conf.y > height:
                    self.confetti.remove(conf)
            
            # Add new confetti periodically
            if len(self.confetti) < 50 and time.time() - self.time_at_game_over < 10:  # Limit confetti duration
                self.confetti.append(Confetti(random.randint(0, width), -10))
    
    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.rolls_left = MAX_ROLLS
        for die in self.dice:
            die.locked = False
        
        # Check if game is over
        game_completed = True
        for player in self.players:
            for category, score in player.scorecard.scores.items():
                if score is None:
                    game_completed = False
                    break
        
        if game_completed:
            self.state = 'game_over'
            self.time_at_game_over = time.time()
            # Create initial confetti
            self.create_confetti(100)
    
    def score_current_roll(self, category):
        current_player = self.players[self.current_player_index]
        
        if not current_player.scorecard.is_category_used(category):
            dice_values = [die.value for die in self.dice]
            score = current_player.scorecard.calculate_possible_score(category, dice_values)
            current_player.scorecard.record_score(category, score)
            current_player.update_total_score()
            self.next_player()
    
    def handle_click(self, pos):
        width, height = get_screen_dimensions()
        
        if self.state == 'menu':
            # Calculate button positions for responsive menu
            button_width = 200
            button_height = 40
            button_x = width // 2 - button_width // 2
            
            # Check for player number buttons
            for i in range(MIN_PLAYERS, MAX_PLAYERS + 1):
                button_rect = pygame.Rect(button_x, height // 6 + 100 + 50 * (i - MIN_PLAYERS), button_width, button_height)
                if button_rect.collidepoint(pos):
                    self.initialize_game(i)
                    return
            
            # Handle help button
            help_rect = pygame.Rect(button_x, height // 6 + 100 + 50 * (MAX_PLAYERS - MIN_PLAYERS + 1), button_width, button_height)
            if help_rect.collidepoint(pos):
                self.previous_state = self.state
                self.state = 'help'
        
        elif self.state == 'playing':
            # Handle dice clicks
            for die in self.dice:
                if die.rect.collidepoint(pos):
                    die.toggle_lock()
            
            # Handle roll button
            button_width = 100
            button_height = 40
            roll_button = pygame.Rect(width // 2 - button_width // 2, get_dice_positions()[0][1] + 100, button_width, button_height)
            if roll_button.collidepoint(pos) and self.rolls_left > 0:
                self.roll_dice()
            
            # Handle "View Scoreboard" button
            scoreboard_button = pygame.Rect(width - 150, 20, 130, 30)
            if scoreboard_button.collidepoint(pos):
                self.previous_state = self.state
                self.state = 'scoreboard'
                return
            
            # Calculate row height for categories based on screen height
            max_categories = len(CATEGORIES)
            available_height = height - 350
            row_height = min(30, max(20, available_height // max_categories))
            
            # Handle category selection
            if self.rolls_left < MAX_ROLLS:  # Only allow scoring after at least one roll
                y_pos = 320
                for category in CATEGORIES:
                    category_rect = pygame.Rect(30, y_pos, 200, 30)
                    if category_rect.collidepoint(pos):
                        self.score_current_roll(category)
                    y_pos += row_height
        
        elif self.state == 'game_over':
            # Handle play again button
            button_width = 200
            button_height = 50
            play_again_rect = pygame.Rect(width // 2 - button_width // 2, height - button_height - 50, button_width, button_height)
            if play_again_rect.collidepoint(pos):
                self.state = 'menu'
        
        elif self.state == 'help':
            # Handle back button
            button_width = 100
            button_height = 40
            back_rect = pygame.Rect(width // 2 - button_width // 2, height - button_height - 30, button_width, button_height)
            if back_rect.collidepoint(pos):
                self.state = self.previous_state or 'menu'
        
        elif self.state == 'scoreboard':
            # Handle back button
            button_width = 100
            button_height = 40
            back_rect = pygame.Rect(width // 2 - button_width // 2, height - button_height - 30, button_width, button_height)
            if back_rect.collidepoint(pos):
                self.state = self.previous_state or 'playing'
    
    def handle_mouse_motion(self, pos):
        # Update hover states
        if self.state == 'playing':
            for die in self.dice:
                die.check_hover(pos)
    
    def create_confetti(self, count):
        self.confetti = []
        width, height = get_screen_dimensions()
        for _ in range(count):
            self.confetti.append(Confetti(random.randint(0, width), -10))

# Drawing functions
def draw_menu(screen):
    width, height = get_screen_dimensions()
    screen.fill(LIGHT_BLUE)
    
    # Title
    title_text = font_large.render("Yacht Dice Game", True, BLACK)
    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 6))
    
    # Player number selection
    subtitle_text = font_medium.render("Select number of players:", True, BLACK)
    screen.blit(subtitle_text, (width // 2 - subtitle_text.get_width() // 2, height // 6 + 60))
    
    button_width = 200
    button_height = 40
    button_x = width // 2 - button_width // 2
    
    for i in range(MIN_PLAYERS, MAX_PLAYERS + 1):
        player_rect = pygame.Rect(button_x, height // 6 + 100 + 50 * (i - MIN_PLAYERS), button_width, button_height)
        pygame.draw.rect(screen, GREEN, player_rect)
        
        player_text = font_medium.render(f"{i} Players", True, BLACK)
        screen.blit(player_text, (player_rect.centerx - player_text.get_width() // 2, 
                                 player_rect.centery - player_text.get_height() // 2))
    
    # Help button
    help_rect = pygame.Rect(button_x, height // 6 + 100 + 50 * (MAX_PLAYERS - MIN_PLAYERS + 1), button_width, button_height)
    pygame.draw.rect(screen, YELLOW, help_rect)
    help_text = font_medium.render("Help", True, BLACK)
    screen.blit(help_text, (help_rect.centerx - help_text.get_width() // 2, 
                          help_rect.centery - help_text.get_height() // 2))

def draw_game(screen, game):
    width, height = get_screen_dimensions()
    screen.fill(LIGHT_BLUE)
    
    # Draw player info
    current_player = game.players[game.current_player_index]
    player_text = font_medium.render(f"{current_player.name}'s turn", True, BLACK)
    screen.blit(player_text, (20, 20))
    
    # Draw rolls left
    rolls_text = font_small.render(f"Rolls left: {game.rolls_left}", True, BLACK)
    screen.blit(rolls_text, (20, 60))
    
    # Draw "View Scoreboard" button
    scoreboard_button = pygame.Rect(width - 150, 20, 130, 30)
    pygame.draw.rect(screen, YELLOW, scoreboard_button)
    pygame.draw.rect(screen, BLACK, scoreboard_button, 1)  # Add border
    scoreboard_text = font_small.render("View Scoreboard", True, BLACK)
    screen.blit(scoreboard_text, (scoreboard_button.centerx - scoreboard_text.get_width() // 2, 
                            scoreboard_button.centery - scoreboard_text.get_height() // 2))
    
    # Draw dice
    for die in game.dice:
        die.draw(screen)
    
    # Draw roll button
    button_width = 100
    button_height = 40
    roll_button = pygame.Rect(width // 2 - button_width // 2, get_dice_positions()[0][1] + 100, button_width, button_height)
    button_color = GREEN if game.rolls_left > 0 else GRAY
    pygame.draw.rect(screen, button_color, roll_button)
    roll_text = font_small.render("Roll", True, BLACK)
    screen.blit(roll_text, (roll_button.centerx - roll_text.get_width() // 2, 
                           roll_button.centery - roll_text.get_height() // 2))
    
    # Draw scorecard
    draw_scorecard(screen, game)
    
    # Draw scores for all players
    draw_all_player_scores(screen, game)

def draw_scorecard(screen, game):
    width, height = get_screen_dimensions()
    current_player = game.players[game.current_player_index]
    dice_values = [die.value for die in game.dice]
    
    # Adjust vertical spacing based on screen height
    max_categories = len(CATEGORIES)
    available_height = height - 350  # Space after other UI elements
    row_height = min(30, max(20, available_height // max_categories))
    
    # Draw category options
    y_pos = 320
    title_text = font_small.render("Categories", True, BLACK)
    screen.blit(title_text, (30, y_pos - 30))
    
    score_title_text = font_small.render("Possible Score", True, BLACK)
    screen.blit(score_title_text, (250, y_pos - 30))
    
    for category, description in CATEGORIES.items():
        # Category name
        category_color = BLACK
        if current_player.scorecard.is_category_used(category):
            category_color = DARK_GRAY
        
        category_text = font_small.render(category, True, category_color)
        screen.blit(category_text, (30, y_pos))
        
        # Possible score
        if not current_player.scorecard.is_category_used(category) and game.rolls_left < MAX_ROLLS:
            score = current_player.scorecard.calculate_possible_score(category, dice_values)
            score_text = font_small.render(str(score), True, category_color)
            screen.blit(score_text, (250, y_pos))
        
        # Draw category box
        pygame.draw.rect(screen, BLACK, (30, y_pos, 200, 30), 1)
        
        y_pos += row_height

def draw_all_player_scores(screen, game):
    width, height = get_screen_dimensions()
    # Section for showing all player scores
    x_pos = min(550, width - 200)  # Keep visible on smaller screens
    y_pos = 320
    
    # Title
    score_title = font_small.render("Scores", True, BLACK)
    screen.blit(score_title, (x_pos, y_pos - 30))
    
    # Player scores
    for player in game.players:
        player_text = font_small.render(f"{player.name}: {player.total_score}", True, BLACK)
        screen.blit(player_text, (x_pos, y_pos))
        y_pos += 30

def draw_game_over(screen, game):
    width, height = get_screen_dimensions()
    screen.fill(LIGHT_BLUE)
    
    # Find winner
    winner = max(game.players, key=lambda p: p.total_score)
    
    # Draw confetti
    for conf in game.confetti:
        conf.draw(screen)
    
    # Title with glow effect
    title_text = font_large.render("Game Over!", True, BLACK)
    title_y = height // 6
    for offset in range(1, 4):
        screen.blit(title_text, (width // 2 - title_text.get_width() // 2 + offset, title_y + offset))
    title_glow = font_large.render("Game Over!", True, YELLOW)
    screen.blit(title_glow, (width // 2 - title_glow.get_width() // 2, title_y))
    
    # Winner announcement with animation
    winner_text = font_medium.render(f"Winner: {winner.name} with {winner.total_score} points!", True, BLACK)
    
    # Add a pulsing effect
    scale = 1.0 + 0.1 * abs(math.sin(time.time() * 3))  # Pulsing between 90% and 110%
    winner_rect = winner_text.get_rect(center=(width // 2, title_y + 80))
    
    # Draw with glow
    for offset in range(1, 3):
        screen.blit(winner_text, (winner_rect.x + offset, winner_rect.y + offset))
    winner_glow = font_medium.render(f"Winner: {winner.name} with {winner.total_score} points!", True, GREEN)
    screen.blit(winner_glow, winner_rect)
    
    # Display all scores
    scores_y = title_y + 150
    title_text = font_medium.render("Final Scores:", True, BLACK)
    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, scores_y))
    
    scores_y += 50
    for player in sorted(game.players, key=lambda p: p.total_score, reverse=True):
        # Highlight the winner
        color = GREEN if player is winner else BLACK
        score_text = font_medium.render(f"{player.name}: {player.total_score}", True, color)
        screen.blit(score_text, (width // 2 - score_text.get_width() // 2, scores_y))
        scores_y += 40
    
    # Play again button with animation
    button_width = 200
    button_height = 50
    play_again_rect = pygame.Rect(width // 2 - button_width // 2, height - button_height - 50, button_width, button_height)
    
    # Button glow animation
    glow_intensity = abs(math.sin(time.time() * 2)) * 50
    pygame.draw.rect(screen, (200 + glow_intensity, 255, 200 + glow_intensity), play_again_rect)
    pygame.draw.rect(screen, BLACK, play_again_rect, 2)  # Add border
    
    play_again_text = font_medium.render("Play Again", True, BLACK)
    screen.blit(play_again_text, (play_again_rect.centerx - play_again_text.get_width() // 2, 
                                  play_again_rect.centery - play_again_text.get_height() // 2))

def draw_help(screen):
    width, height = get_screen_dimensions()
    screen.fill(LIGHT_GREEN)
    
    # Title
    title_text = font_large.render("How to Play Yacht", True, BLACK)
    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 10))
    
    # Rules text
    rules = [
        "Yacht is a dice game similar to Yahtzee.",
        "On your turn:",
        "1. Roll five dice (up to three times per turn)",
        "2. Click on dice to lock/unlock them between rolls",
        "3. After rolling, select a scoring category",
        "",
        "Scoring Categories:",
        "• Aces to Sixes: Sum of all dice with that number",
        "• Choice: Sum of all dice",
        "• Four of a Kind: Four dice with same value",
        "• Full House: Three of a kind and a pair",
        "• Small Straight: Four sequential dice (score: 15)",
        "• Large Straight: Five sequential dice (score: 30)",
        "• Yacht: All five dice same value (score: 50)",
        "",
        "Each category can only be used once per game.",
        "The player with the highest total score wins!"
    ]
    
    # Adjust line spacing based on screen height
    available_height = height - 200  # Space after title and before button
    line_height = min(25, max(18, available_height // len(rules)))
    
    y_pos = height // 10 + 70
    for line in rules:
        if line == "":
            y_pos += 10  # Add a little extra space for blank lines
        else:
            text = font_small.render(line, True, BLACK)
            screen.blit(text, (width // 2 - text.get_width() // 2, y_pos))
        y_pos += line_height
    
    # Back button
    button_width = 100
    button_height = 40
    back_rect = pygame.Rect(width // 2 - button_width // 2, height - button_height - 30, button_width, button_height)
    pygame.draw.rect(screen, GREEN, back_rect)
    back_text = font_small.render("Back", True, BLACK)
    screen.blit(back_text, (back_rect.centerx - back_text.get_width() // 2, 
                          back_rect.centery - back_text.get_height() // 2))

# Add a new function to draw the detailed scoreboard
def draw_scoreboard(screen, game):
    width, height = get_screen_dimensions()
    screen.fill(LIGHT_BLUE)
    
    # Title
    title_text = font_large.render("Detailed Scoreboard", True, BLACK)
    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, 30))
    
    # Calculate column widths and positions
    num_players = len(game.players)
    category_width = 150
    player_column_width = min(100, (width - category_width) // num_players)
    start_x = (width - (category_width + player_column_width * num_players)) // 2
    
    # Draw player headers
    for i, player in enumerate(game.players):
        # Highlight the current player
        player_color = GREEN if i == game.current_player_index else BLACK
        player_header = font_medium.render(player.name, True, player_color)
        player_x = start_x + category_width + i * player_column_width + player_column_width // 2
        screen.blit(player_header, (player_x - player_header.get_width() // 2, 80))
    
    # Draw category rows and scores
    y_pos = 120
    row_height = min(30, max(24, (height - 170) // len(CATEGORIES)))
    
    for category in CATEGORIES:
        # Draw category name
        category_text = font_small.render(category, True, BLACK)
        screen.blit(category_text, (start_x + 10, y_pos + (row_height - category_text.get_height()) // 2))
        
        # Draw horizontal line
        pygame.draw.line(screen, BLACK, (start_x, y_pos), (start_x + category_width + player_column_width * num_players, y_pos), 1)
        
        # Draw each player's score for this category
        for i, player in enumerate(game.players):
            score = player.scorecard.scores[category]
            
            if score is not None:
                score_text = font_small.render(str(score), True, BLACK)
                score_x = start_x + category_width + i * player_column_width + player_column_width // 2
                screen.blit(score_text, (score_x - score_text.get_width() // 2, y_pos + (row_height - score_text.get_height()) // 2))
            else:
                # Draw empty cell indicator
                pygame.draw.line(screen, DARK_GRAY, 
                               (start_x + category_width + i * player_column_width + 10, y_pos + 5),
                               (start_x + category_width + (i+1) * player_column_width - 10, y_pos + row_height - 5), 1)
                pygame.draw.line(screen, DARK_GRAY,
                               (start_x + category_width + i * player_column_width + 10, y_pos + row_height - 5),
                               (start_x + category_width + (i+1) * player_column_width - 10, y_pos + 5), 1)
        
        # Draw vertical grid lines
        for i in range(num_players + 1):
            x = start_x + category_width + i * player_column_width
            pygame.draw.line(screen, BLACK, (x, 80), (x, y_pos + row_height), 1)
        
        y_pos += row_height
    
    # Draw horizontal line at bottom
    pygame.draw.line(screen, BLACK, (start_x, y_pos), (start_x + category_width + player_column_width * num_players, y_pos), 1)
    
    # Draw totals
    y_pos += 10
    total_text = font_medium.render("Total:", True, BLACK)
    screen.blit(total_text, (start_x + 10, y_pos))
    
    for i, player in enumerate(game.players):
        total_score = player.total_score
        total_score_text = font_medium.render(str(total_score), True, GREEN if i == game.current_player_index else BLACK)
        total_score_x = start_x + category_width + i * player_column_width + player_column_width // 2
        screen.blit(total_score_text, (total_score_x - total_score_text.get_width() // 2, y_pos))
    
    # Back button
    button_width = 100
    button_height = 40
    back_rect = pygame.Rect(width // 2 - button_width // 2, height - button_height - 30, button_width, button_height)
    pygame.draw.rect(screen, GREEN, back_rect)
    back_text = font_small.render("Back", True, BLACK)
    screen.blit(back_text, (back_rect.centerx - back_text.get_width() // 2, 
                          back_rect.centery - back_text.get_height() // 2))

# Add these functions after the draw_ functions to handle responsive layout
def get_screen_dimensions():
    """Get current screen dimensions for responsive layout"""
    return screen.get_width(), screen.get_height()

def get_dice_positions():
    """Calculate dice positions based on current screen size"""
    width, height = get_screen_dimensions()
    dice_spacing = 80
    start_x = (width - dice_spacing * DICE_COUNT) // 2
    y_pos = min(150, height // 4)  # Adjust y position based on screen height
    
    positions = []
    for i in range(DICE_COUNT):
        positions.append((start_x + i * dice_spacing, y_pos))
    return positions

# Main game loop
def main():
    # Add global screen declaration
    global screen
    
    # Generate dice images
    global dice_images
    dice_images = generate_dice_images()
    
    # Create game object
    game = YachtGame()
    
    # Main game loop
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    game.handle_click(event.pos)
            
            if event.type == MOUSEMOTION:
                game.handle_mouse_motion(event.pos)
                
            if event.type == VIDEORESIZE:
                # Update the global screen variable to handle resizing
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                # Reposition dice if we're in playing state
                if game.state == 'playing':
                    positions = get_dice_positions()
                    for i, die in enumerate(game.dice):
                        die.x, die.y = positions[i]
                        die.rect = pygame.Rect(die.x, die.y, die.size, die.size)
        
        # Update game state
        game.update()
        
        # Draw the appropriate screen based on game state
        if game.state == 'menu':
            draw_menu(screen)
        elif game.state == 'playing':
            draw_game(screen, game)
        elif game.state == 'game_over':
            draw_game_over(screen, game)
        elif game.state == 'help':
            draw_help(screen)
        elif game.state == 'scoreboard':
            draw_scoreboard(screen, game)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main() 