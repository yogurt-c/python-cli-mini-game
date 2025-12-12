#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hangman Terminal Game
Guess the word letter by letter before the hangman is complete!
"""

import random
import os

# Word list for the game (organized by category)
WORDS = [
    # Programming
    "python", "javascript", "algorithm", "function", "variable",
    "terminal", "developer", "software", "database", "framework",
    "compiler", "debugging", "interface", "iterator", "recursion",
    "inheritance", "polymorphism", "encapsulation", "abstraction", "constructor",
    
    # Animals
    "elephant", "giraffe", "butterfly", "dolphin", "penguin",
    "kangaroo", "crocodile", "cheetah", "flamingo", "octopus",
    "gorilla", "squirrel", "hedgehog", "jellyfish", "leopard",
    "peacock", "mongoose", "platypus", "chameleon", "armadillo",
    
    # Nature
    "mountain", "ocean", "forest", "desert", "island",
    "volcano", "waterfall", "glacier", "canyon", "meadow",
    "savanna", "tundra", "prairie", "rainforest", "hurricane",
    "earthquake", "avalanche", "lightning", "rainbow", "sunset",
    
    # Music
    "guitar", "piano", "violin", "trumpet", "drums",
    "saxophone", "harmonica", "accordion", "tambourine", "xylophone",
    "orchestra", "symphony", "melody", "rhythm", "harmony",
    
    # Food
    "pizza", "spaghetti", "hamburger", "chocolate", "strawberry",
    "pineapple", "avocado", "broccoli", "mushroom", "cinnamon",
    "croissant", "pancake", "sandwich", "sushi", "lasagna",
    
    # Sports
    "basketball", "football", "baseball", "volleyball", "badminton",
    "swimming", "gymnastics", "marathon", "archery", "skateboard",
    "snowboard", "wrestling", "cricket", "hockey", "cycling",
    
    # Science
    "chemistry", "physics", "biology", "astronomy", "molecule",
    "electron", "gravity", "evolution", "photosynthesis", "chromosome",
    "hypothesis", "experiment", "laboratory", "microscope", "telescope",
    
    # Places
    "hospital", "library", "airport", "restaurant", "university",
    "museum", "stadium", "theater", "cathedral", "lighthouse",
    
    # Objects
    "keyboard", "notebook", "umbrella", "backpack", "headphones",
    "telescope", "microscope", "chandelier", "bookshelf", "fireplace",
    
    # Miscellaneous
    "adventure", "mystery", "challenge", "discovery", "imagination",
    "celebration", "friendship", "knowledge", "happiness", "butterfly",
    "magnificent", "extraordinary", "spectacular", "wonderful", "incredible"
]

# Hangman stages (7 stages = 6 wrong guesses allowed)
HANGMAN_STAGES = [
    """
       +---+
       |   |
           |
           |
           |
           |
       =========
    """,
    """
       +---+
       |   |
       O   |
           |
           |
           |
       =========
    """,
    """
       +---+
       |   |
       O   |
       |   |
           |
           |
       =========
    """,
    """
       +---+
       |   |
       O   |
      /|   |
           |
           |
       =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
           |
           |
       =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
      /    |
           |
       =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
      / \\  |
           |
       =========
    """
]


class HangmanGame:
    def __init__(self):
        self.word = random.choice(WORDS).upper()
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.max_wrong = 6
        self.game_over = False
        self.won = False

    def get_display_word(self):
        """Return the word with unguessed letters as underscores"""
        return ' '.join(
            letter if letter in self.guessed_letters else '_'
            for letter in self.word
        )

    def get_wrong_letters(self):
        """Return list of wrong guessed letters"""
        return sorted([
            letter for letter in self.guessed_letters
            if letter not in self.word
        ])

    def guess(self, letter):
        """Make a guess and return result message"""
        letter = letter.upper()
        
        if not letter.isalpha() or len(letter) != 1:
            return "Please enter a single letter!"
        
        if letter in self.guessed_letters:
            return f"You already guessed '{letter}'!"
        
        self.guessed_letters.add(letter)
        
        if letter in self.word:
            # Check if won
            if all(l in self.guessed_letters for l in self.word):
                self.won = True
                self.game_over = True
            return f"Good! '{letter}' is in the word!"
        else:
            self.wrong_guesses += 1
            if self.wrong_guesses >= self.max_wrong:
                self.game_over = True
            return f"Sorry, '{letter}' is not in the word."

    def display(self, message=""):
        """Display the current game state"""
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # Colors
        red = '\033[91m'
        green = '\033[92m'
        yellow = '\033[93m'
        cyan = '\033[96m'
        reset = '\033[0m'
        bold = '\033[1m'
        
        print(f"\n{cyan}{bold}{'=' * 40}{reset}")
        print(f"{cyan}{bold}          🎮 HANGMAN GAME 🎮{reset}")
        print(f"{cyan}{bold}{'=' * 40}{reset}\n")
        
        # Hangman figure
        print(HANGMAN_STAGES[self.wrong_guesses])
        
        # Word display
        print(f"\n  {bold}Word:{reset} {yellow}{self.get_display_word()}{reset}")
        print(f"  {bold}Length:{reset} {len(self.word)} letters\n")
        
        # Wrong letters
        wrong = self.get_wrong_letters()
        if wrong:
            print(f"  {bold}Wrong guesses:{reset} {red}{', '.join(wrong)}{reset}")
        
        # Remaining attempts
        remaining = self.max_wrong - self.wrong_guesses
        if remaining <= 2:
            print(f"  {bold}Remaining:{reset} {red}{remaining} attempts{reset}")
        else:
            print(f"  {bold}Remaining:{reset} {green}{remaining} attempts{reset}")
        
        # Message
        if message:
            if "Good" in message:
                print(f"\n  {green}{message}{reset}")
            elif "Sorry" in message or "already" in message:
                print(f"\n  {red}{message}{reset}")
            else:
                print(f"\n  {yellow}{message}{reset}")
        
        # Game over messages
        if self.game_over:
            print()
            if self.won:
                print(f"  {green}{bold}🎉 CONGRATULATIONS! You won! 🎉{reset}")
                print(f"  {green}The word was: {self.word}{reset}")
            else:
                print(f"  {red}{bold}💀 GAME OVER! 💀{reset}")
                print(f"  {red}The word was: {yellow}{self.word}{reset}")


def main():
    game = HangmanGame()
    message = ""
    
    while not game.game_over:
        game.display(message)
        
        try:
            guess = input("\n  Enter a letter (or 'quit' to exit): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n  Goodbye!")
            return
        
        if guess.lower() == 'quit':
            print("\n  Goodbye!")
            return
        
        if guess:
            message = game.guess(guess)
    
    # Final display
    game.display()
    
    # Play again?
    try:
        again = input("\n  Play again? (y/n): ").strip().lower()
        if again == 'y':
            main()
    except (EOFError, KeyboardInterrupt):
        pass
    
    print("\n  Thanks for playing! 👋\n")


if __name__ == "__main__":
    main()
