#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
import os
import random

HANGMANPICS = ['''

  +---+
  |   |
      |
      |
      |
      |
=========''', '''

  +---+
  |   |
  O   |
      |
      |
      |
=========''', '''

  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', '''

  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''

  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''', '''

  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''', '''

  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''']
words = 'ant baboon badger bat bear beaver camel cat clam cobra cougar coyote crow deer dog donkey duck eagle ferret fox frog goat goose hawk lion lizard llama mole monkey moose mouse mule newt otter owl panda parrot pigeon python rabbit ram rat raven rhino salmon seal shark sheep skunk sloth snake spider stork swan tiger toad trout turkey turtle weasel whale wolf wombat zebra'.split()
# 최고 점수를 기록한 파일 경로
record_path = 'record.txt'

def getRandomWord(wordList):
    # This function returns a random string from the passed list of strings.
    wordIndex = random.randint(0, len(wordList) - 1)
    return wordList[wordIndex]

def displayBoard(HANGMANPICS, missedLetters, correctLetters, secretWord):
    print(HANGMANPICS[len(missedLetters)])
    print()

    print('Missed letters:', end=' ')
    for letter in missedLetters:
        print(letter, end=' ')
    print()

    blanks = ''
    # replace blanks with correctly guessed letters
    for i in range(len(secretWord)):
        if secretWord[i] in correctLetters:
            blanks += secretWord[i]
        else:
            blanks += '_'
    # show the secret word with spaces in between each letter
    for letter in blanks:
        print(letter, end=' ')
    print()

def getGuess(alreadyGuessed):
    # Returns the letter the player entered. This function makes sure the player entered a single letter, and not something else.
    while True:
        print('Guess a letter.')
        guess = input().lower()
        if len(guess) != 1:
            print('Please enter a single letter.')
        elif guess in alreadyGuessed:
            print('You have already guessed that letter. Choose again.')
        elif guess not in 'abcdefghijklmnopqrstuvwxyz':
            print('Please enter a LETTER.')
        else:
            return guess

def playAgain():
    # This function returns True if the player wants to play again, otherwise it returns False.
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')

# Check if the player has won
def checkCorrectAnswer(correctLetters, secretWord):
    foundAllLetters = True
    for i in range(len(secretWord)):
        if secretWord[i] not in correctLetters:
            foundAllLetters = False
            break
    return foundAllLetters

# Check if player has guessed too many times and lost
def checkWrongAnswer(missedLetters, secretWord):
    # Check if player has guessed too many times and lost
    if len(missedLetters) == len(HANGMANPICS) - 1:
        return True
    return False

# 최고 기록을 저장
def recordHighestScore(gameScore):
    mode = None
    if os.path.isdir(record_path):
        print("Check record is file. record_path: {}".format(record_path))
    # 파일이 없는 경우
    if not os.path.exists(record_path):
        mode = 'a'
    else:
        with open(record_path, "r") as f:
            highestScore = int(f.read())
        # 최고 점수보다 높으면 파일에 저장
        if gameScore > highestScore:
            mode = 'w'
    if mode:
        print("Congratulations on your new record!!! Your record is {}.".format(gameScore))
        with open(record_path, mode) as f:
            f.write(str(gameScore))

def main():
    """Main application entry point."""
    print('Hello, this is hangman game. Guess the word in 6 times.')
    missedLetters = ''
    correctLetters = ''
    gameSucceeded = False
    gameFailed = False
    gameScore = len(HANGMANPICS) - 1
    secretWord = getRandomWord(words)

    while True:
        displayBoard(HANGMANPICS, missedLetters, correctLetters, secretWord)

        if gameSucceeded or gameFailed:
            if gameSucceeded:
                print('Yes! The secret word is "' + secretWord + '"! You have won!')
                recordHighestScore(gameScore)
            else:
                print('You have run out of guesses!\nAfter ' + str(len(missedLetters)) + ' missed guesses and ' + str(len(correctLetters)) + ' correct guesses, the word was "' + secretWord + '"')
            # Ask the player if they want to play again (but only if the game is done).
            if playAgain():
                missedLetters = ''
                correctLetters = ''
                gameSucceeded = False
                gameFailed = False
                gameScore = len(HANGMANPICS) - 1
                secretWord = getRandomWord(words)
                continue 
            else: 
                break

        # Let the player type in a letter.
        guess = getGuess(missedLetters + correctLetters)
        if guess in secretWord:
            correctLetters = correctLetters + guess
            gameSucceeded = checkCorrectAnswer(correctLetters, secretWord)
        else:
            gameScore -= 1
            missedLetters = missedLetters + guess
            gameFailed = checkWrongAnswer(missedLetters, secretWord)


if __name__ == "__main__":
    main()