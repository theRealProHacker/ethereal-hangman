"""
A simple single-player Hangman game demo in Python.
This script allows a user to play a game of Hangman in the console.
It's supposed to be a demo for the future blockchain-deployment.
"""

from random import choice, randint
import re

#========= This Part Handles Word Selection and would be deployed off-chain =========

with open("wordlist", encoding="utf-8") as f:
    words = f.read().splitlines()

def get_word(length: int, like: str, excludes: str) -> str|None:
    """Get a random word of a given length that matches a pattern and excludes certain letters."""
    pattern = re.compile(like.replace("_", "."))

    filtered_words = [
        word for word in words
        if len(word) == length and pattern.fullmatch(word) and all(c not in word for c in excludes)
    ]
    print("Found words:", len(filtered_words))
    if not filtered_words:
        return None
    return choice(filtered_words)

#========= This Part Handles the Game Logic and would be deployed on-chain =========

MAX_WRONG_GUESSES = 6

# First, the length of the word is determined
l = randint(4, 10) # inclusive

# initialize game state
wrong_guesses = 0
wrong_letters = ""
correct_letters = ""
word = "_"*l

print(f"{word} ({l})")

# Now the word is guessed by the player
while True:
    letter = ""
    while not (len(letter) == 1 and letter.isalpha()):
        letter = input("Guess a letter: ")
        if letter in correct_letters + wrong_letters:
            print("You already guessed that letter.")
            letter = ""
    letter = letter.lower()

    new_word = get_word(l, word, wrong_letters)

    # This can't happen as long as the length is valid
    assert new_word is not None, "No valid words found with the current constraints."

    if letter in new_word:
        # correct guess
        correct_letters += letter
        word = "".join(
            c if c == letter else word[i]
            for i, c in enumerate(new_word)
        )
        print(f"Correct! {word} ({l})")
    else:
        # wrong guess
        wrong_guesses += 1
        wrong_letters += letter
        print(f"Wrong! {word} ({l}) - Wrong guesses: {wrong_guesses} - Wrong letters: {wrong_letters}")
    
    if "_" not in word:
        print(f"Congratulations! You guessed the word: {word}")
        break
    elif wrong_guesses >= MAX_WRONG_GUESSES:
        print(f"Game over! The word was: {new_word}")
        break



