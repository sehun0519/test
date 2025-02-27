# Yacht Dice Game

A Pygame implementation of the classic Yacht dice game (similar to Yahtzee) for 2-4 players.

## Game Rules

Yacht is a dice game where players take turns rolling five dice to achieve certain combinations. Each player gets three rolls per turn, and after each roll, they can choose which dice to keep and which to reroll. After their rolls, they must choose a category to score in.

### Scoring Categories

- **Aces to Sixes**: Sum of all dice showing the corresponding number
- **Choice**: Sum of all five dice
- **Four of a Kind**: Four dice showing the same face
- **Full House**: Three of a kind and a pair
- **Small Straight**: Four sequential dice (score: 15)
- **Large Straight**: Five sequential dice (score: 30)
- **Yacht**: All five dice showing the same face (score: 50)

Each category can only be used once per game. The player with the highest total score at the end wins.

## How to Play

1. Run the game: `python yacht_game.py`
2. Select the number of players (2-4)
3. On your turn:
   - Click "Roll" to roll the dice (up to 3 times per turn)
   - Click on dice to lock/unlock them between rolls
   - Select a scoring category after at least one roll
4. The game ends when all players have filled all categories
5. The player with the highest score wins!

## Controls

- **Mouse**: Click on dice to lock/unlock, click on scoring categories to select, click buttons to navigate

## Requirements

- Python 3.x
- Pygame

## Installation

1. Ensure Python 3.x is installed
2. Install requirements: `pip install -r requirements.txt` 
3. Run the game: `python yacht_game.py` 