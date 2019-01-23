from flask import Flask, render_template, session, redirect, url_for, request
app = Flask(__name__)
from random import randint

all_games = {}
n = []

def nouns():
    with open("nounlist.txt") as f:
        lines = f.read().splitlines()
    l = lines
    return l

def generate_random():
    l = [chr(randint(97,122)) for i in range(10)]
    return "".join(l)

def generate(word, guesses):
    result = []
    for c in word:
        if c in guesses:
            result.append(c + " ")
        else:
            result.append("_ ")
    return "".join(result)

def format_guess(guess):
    r = "".join(list(map(lambda x: x + " ", guess)))
    return r

@app.route('/images/<image>')
def getimages(image):
    return 
@app.route('/')
def hello():
    a = generate_random()
    w = n[randint(0, len(n)-1)]
    all_games[a] = {"game": a, "num": 6, "word": w, "guess" : []}
    return redirect(a)
    

@app.route('/<game>', methods=['GET'])
def gamee(game):
    if game in all_games:
        game = all_games[game]
        err = ""
        if game["num"] == 0:
            err = f"You lost the game! The word was {game['word']}"
        if len(list(set(game["word"]).difference(set(game["guess"])))) == 0:
            err = "Congratulations! You win!"
        return render_template('index.html', t=game["game"], word = generate(game["word"], game["guess"]), guess=format_guess(game["guess"]), num = game["num"], error=err)
    else:
        return "game not found"
                               
@app.route('/<game>', methods=["POST"])
def game_update(game):
    if game in all_games:
        game = all_games[game]
        err = ""
        if len(request.values.get('g').split()) == 0:
            letter = " "
        else:
            letter = request.values.get('g').split()[0]
            #err = "Please enter a value"
            #return render_template('index.html', t=game["game"], word = generate(game["word"], game["guess"]), guess=format_guess(game["guess"]), num = game["num"], error=err)
        
        if game["num"] > 0:
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
            if game["num"] == 0:
                err = f"You lost the game! The word was {game['word']}"
            if len(list(set(game["word"]).difference(set(game["guess"])))) == 0:
                err = "Congratulations! You win!"
                
            return render_template('index.html', t=game["game"], word = generate(game["word"], game["guess"]), guess=format_guess(game["guess"]), num = game["num"], error=err)
        else:
            if len(list(set(game["word"]).difference(set(game["guess"])))) == 0:
                err = "Congratulations! You win!"
            else:
                err = f"You lost the game! The word was {game['word']}"
            return render_template('index.html', t=game["game"], word = generate(game["word"], game["guess"]), guess=format_guess(game["guess"]), num = game["num"], error=err)
    else:
        return "game not found"


if __name__ == '__main__':
    n = nouns()
    app.run()
    print("running")
