#Assignment 1
#Author: Andrew Boyadjiev
#Dependencies: Flask
#Description: Web service that allows the user to play a game of hangman
#             The server chooses a random noun from a text file for each new game 
#             When user starts a game, a instance of a game is created with a
#             unique 10 letter URL link to access.
#             Games are stored in a dictionary object inside a dictionary

from flask import Flask, render_template, session, redirect, url_for, request
app = Flask(__name__)
from random import randint

all_games = {}
n = []

#Takes all nouns from the nounslist text file and puts it into a list object
def nouns():
    with open("nounlist.txt") as f:
        lines = f.read().splitlines()
    l = lines
    return l

#Generates the URL link ID
def generate_random():
    l = [chr(randint(97,122)) for i in range(10)]
    return "".join(l)

#Compares the word to the letters guessed. Replaces unguessed letters with underscore _
def generate(word, guesses):
    result = [c + " " if c in guesses else "_ " for c in word]
    return "".join(result)

#Converts guesses into a string with a ' ' between them
def format_guess(guess):
    r = "".join(list(map(lambda x: x + " ", guess)))
    return r

#Checks if the game is complete or if the user won the game
def check_game_state(game, err):
    if game["num"] == 0:
            err = f"You lost the game! The word was {game['word']}"
    if len(list(set(game["word"]).difference(set(game["guess"])))) == 0:
            err = "Congratulations! You win!"
    return err

#Checks if the user guesses a valid letter
def check_guess(letter, game, err):
    if len(letter) == 0:
        err = "Error: must guess a letter"
    if len(letter) > 1:
        err = "Error: must guess a letter, not a word"
    if len(letter)==1:
        if letter in game["guess"]:
              err = f"Error: you already guessed {letter}"
        elif ord(letter) in range(97, 123) or ord(letter) in range(65, 91):
            game["guess"].append(letter)
            if letter not in game["word"]:
                game["num"] = game["num"]-1
        else:
            err = "Error: must guess a valid letter"
    err = check_game_state(game, err)
    return err

#Default landing page generates a new game for the user
@app.route('/')
def hello():
    a = generate_random()
    w = n[randint(0, len(n)-1)]
    all_games[a] = {"game": a, "num": 6, "word": w, "guess" : []}
    return redirect(a)
    

#For refreshing the game
@app.route('/<game>', methods=['GET'])
def game_get(game):
    if game in all_games:
        game = all_games[game]
        err = ""
        err = check_game_state(game, err)
        return render_template('index.html', t=game["game"], word = generate(game["word"], game["guess"]), guess=format_guess(game["guess"]), num = game["num"], error=err)
    else:
        return "game not found"

#For when the user sends a guess with a POST request
@app.route('/<game>', methods=["POST"])
def game_update(game):
    if game in all_games:
        game = all_games[game]
        err = ""
        if len(request.values.get('g').split()) == 0:
            letter = " "
        else:
            letter = request.values.get('g').split()[0]
        if game["num"] > 0:
            err = check_guess(letter, game, err)    
        else:
            err = check_game_state(game, err)
        return render_template('index.html', t=game["game"], word = generate(game["word"], game["guess"]), guess=format_guess(game["guess"]), num = game["num"], error=err)
    else:
        return "game not found"


if __name__ == '__main__':
    n = nouns()
    app.run()
    print("running")
