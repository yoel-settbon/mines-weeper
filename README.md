# Mines Weeper

A classic Minesweeper game implementation using Pygame, featuring multiple difficulty levels and a high score system.

## Description

Mines Weeper is a single-player puzzle game where the goal is to clear a rectangular board containing hidden "mines" without detonating any of them. You use clues about the number of neighboring mines in each field to determine where the mines are.

## Features

- **Multiple Difficulty Levels**:
  - Easy: 9x9 grid with 10 mines
  - Medium: 16x16 grid with 40 mines
  - Hard: 16x30 grid with 99 mines

- **Player Profile**: Enter your name to keep track of your scores

- **High Score System**: Top 5 scores are saved for each difficulty level

- **Classic Minesweeper Gameplay**:
  - Left-click to reveal cells
  - Right-click to cycle through flag and question mark

## Installation

1. Make sure you have Python 3.6+ installed on your system
2. Clone this repository:
```
git clone https://github.com/yourusername/mines-weeper.git
cd mines-weeper
```
3. Install the required packages:
```
pip install -r requirements.txt
```
4. Run the game:
```
python main.py
```

## Game Controls

- **Left Mouse Button**: Reveal a cell
- **Right Mouse Button**: Place or remove a flag/question mark
- **Menu Interaction**: Click on buttons to navigate or select options

## Project Structure

```
mines-weeper/
│
├── main.py                  # Main entry point
├── models/                  # Game components
│   ├── game.py              # Game logic
│   ├── grid.py              # Board implementation
│   ├── input_box.py         # Text input field for player name
│   ├── main_menu.py         # Main menu implementation
│   ├── menu_button.py       # Button UI component
│   ├── popup.py             # Popup dialog (win/lose screens)
│   ├── score_manager.py     # High score tracking system
│   └── utilities.py         # UI utilities and rendering
│
├── scores.json              # Saved high scores
├── requirements.txt         # Python dependencies
└── README.md                # This file
```
