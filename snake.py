#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Snake Terminal Game
Use arrow keys to control the snake and eat food.
"""

import curses
import random
import time


class SnakeGame:
    def __init__(self, height=15, width=30):
        self.height = height
        self.width = width
        self.snake = [(height // 2, width // 2)]
        self.direction = curses.KEY_RIGHT
        self.food = None
        self.score = 0
        self.game_over = False
        self.base_speed = 120  # base milliseconds between moves
        self.direction_changed = False  # Prevent multiple direction changes per tick
        self.place_food()

    def place_food(self):
        """Place food at a random empty cell"""
        empty_cells = []
        for i in range(1, self.height - 1):
            for j in range(1, self.width - 1):
                if (i, j) not in self.snake:
                    empty_cells.append((i, j))
        if empty_cells:
            self.food = random.choice(empty_cells)

    def get_current_speed(self):
        """Get speed adjusted for direction (vertical moves need more time due to taller characters)"""
        if self.direction in [curses.KEY_UP, curses.KEY_DOWN]:
            return self.base_speed * 1.8  # Vertical is slower to match visual speed
        return self.base_speed

    def move(self):
        """Move the snake in the current direction"""
        # Reset direction change flag for next tick
        self.direction_changed = False
        
        head_y, head_x = self.snake[0]

        if self.direction == curses.KEY_UP:
            new_head = (head_y - 1, head_x)
        elif self.direction == curses.KEY_DOWN:
            new_head = (head_y + 1, head_x)
        elif self.direction == curses.KEY_LEFT:
            new_head = (head_y, head_x - 1)
        elif self.direction == curses.KEY_RIGHT:
            new_head = (head_y, head_x + 1)
        else:
            return

        # Check wall collision
        if (new_head[0] <= 0 or new_head[0] >= self.height - 1 or
            new_head[1] <= 0 or new_head[1] >= self.width - 1):
            self.game_over = True
            return

        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        # Check if food is eaten
        if new_head == self.food:
            self.score += 10
            self.place_food()
            # Speed up slightly
            if self.base_speed > 40:
                self.base_speed -= 3
        else:
            self.snake.pop()

    def change_direction(self, new_direction):
        """Change direction if valid (can't reverse, only once per tick)"""
        # Only allow one direction change per movement tick
        if self.direction_changed:
            return
        
        opposites = {
            curses.KEY_UP: curses.KEY_DOWN,
            curses.KEY_DOWN: curses.KEY_UP,
            curses.KEY_LEFT: curses.KEY_RIGHT,
            curses.KEY_RIGHT: curses.KEY_LEFT
        }
        if new_direction in opposites and new_direction != opposites.get(self.direction):
            self.direction = new_direction
            self.direction_changed = True


def main(stdscr):
    # Setup curses
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(1)   # Non-blocking input
    stdscr.timeout(50)  # Refresh rate
    
    # Initialize colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Snake body
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)     # Food
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Border/Score
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Title
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_GREEN)   # Snake head

    # Get terminal size and create game
    max_y, max_x = stdscr.getmaxyx()
    game_height = min(18, max_y - 6)
    game_width = min(50, max_x - 4)
    
    game = SnakeGame(game_height, game_width)
    
    # Calculate offsets for centering
    offset_y = 3
    offset_x = 2

    last_move_time = time.time()

    while not game.game_over:
        stdscr.erase()
        
        # Title
        title = "[ SNAKE GAME ]"
        stdscr.attron(curses.color_pair(4) | curses.A_BOLD)
        stdscr.addstr(0, offset_x, "=" * game.width)
        stdscr.addstr(1, offset_x + (game.width - len(title)) // 2, title)
        stdscr.addstr(2, offset_x, "=" * game.width)
        stdscr.attroff(curses.color_pair(4) | curses.A_BOLD)
        
        # Score
        score_text = f"Score: {game.score}  |  Length: {len(game.snake)}"
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(offset_y - 1, offset_x, score_text)
        stdscr.attroff(curses.color_pair(3))

        # Draw border
        stdscr.attron(curses.color_pair(3))
        for i in range(game.height):
            for j in range(game.width):
                if i == 0 or i == game.height - 1:
                    try:
                        stdscr.addch(offset_y + i, offset_x + j, curses.ACS_HLINE)
                    except:
                        pass
                elif j == 0 or j == game.width - 1:
                    try:
                        stdscr.addch(offset_y + i, offset_x + j, curses.ACS_VLINE)
                    except:
                        pass
        stdscr.attroff(curses.color_pair(3))

        # Draw food
        if game.food:
            stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
            try:
                stdscr.addstr(offset_y + game.food[0], offset_x + game.food[1], "O")
            except:
                pass
            stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)

        # Draw snake
        snake_len = len(game.snake)
        for idx, (y, x) in enumerate(game.snake):
            try:
                if idx == 0:
                    # Head - bright with direction
                    stdscr.attron(curses.color_pair(5) | curses.A_BOLD)
                    if game.direction == curses.KEY_UP:
                        stdscr.addstr(offset_y + y, offset_x + x, "^")
                    elif game.direction == curses.KEY_DOWN:
                        stdscr.addstr(offset_y + y, offset_x + x, "v")
                    elif game.direction == curses.KEY_LEFT:
                        stdscr.addstr(offset_y + y, offset_x + x, "<")
                    else:
                        stdscr.addstr(offset_y + y, offset_x + x, ">")
                    stdscr.attroff(curses.color_pair(5) | curses.A_BOLD)
                elif idx == snake_len - 1 and snake_len > 1:
                    # Tail
                    stdscr.attron(curses.color_pair(1))
                    stdscr.addstr(offset_y + y, offset_x + x, ".")
                    stdscr.attroff(curses.color_pair(1))
                else:
                    # Body
                    stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
                    stdscr.addstr(offset_y + y, offset_x + x, "#")
                    stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)
            except:
                pass

        # Instructions
        try:
            stdscr.addstr(offset_y + game.height + 1, offset_x, "Arrow keys: move | q: quit")
        except:
            pass

        stdscr.refresh()

        # Handle input
        key = stdscr.getch()
        
        if key == ord('q'):
            break
        elif key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            game.change_direction(key)

        # Move snake at regular intervals (adjusted for direction)
        current_time = time.time()
        if (current_time - last_move_time) * 1000 >= game.get_current_speed():
            game.move()
            last_move_time = current_time

    # Game over screen
    stdscr.erase()
    stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
    try:
        stdscr.addstr(max_y // 2 - 2, max_x // 2 - 6, "GAME OVER!")
    except:
        pass
    stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)
    
    stdscr.attron(curses.color_pair(3))
    try:
        stdscr.addstr(max_y // 2, max_x // 2 - 8, f"Final Score: {game.score}")
        stdscr.addstr(max_y // 2 + 1, max_x // 2 - 8, f"Snake Length: {len(game.snake)}")
    except:
        pass
    stdscr.attroff(curses.color_pair(3))
    
    try:
        stdscr.addstr(max_y // 2 + 3, max_x // 2 - 12, "Press any key to exit...")
    except:
        pass
    stdscr.nodelay(0)
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)
