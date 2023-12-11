from flask import Flask, request, jsonify
import sqlite3
import random

app = Flask(__name__)

# Manually handle CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

# Initialize the database and create the table if it doesn't exist
def init_db():
    with sqlite3.connect('rps_game.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_results (
            id INTEGER PRIMARY KEY,
            player_choice TEXT,
            computer_choice TEXT,
            result TEXT
        )
        ''')
        conn.commit()

init_db()

# Function to determine computer's choice
def computer_turn():
    choices = ["ROCK", "PAPER", "SCISSORS"]
    return random.choice(choices)

# Function to determine the winner
def check_winner(player, computer):
    if player == computer:
        return "Draw!"
    elif (player == "ROCK" and computer == "SCISSORS") or \
         (player == "PAPER" and computer == "ROCK") or \
         (player == "SCISSORS" and computer == "PAPER"):
        return "You Win!"
    else:
        return "You Lose!"

# Endpoint to handle the game logic
@app.route('/play', methods=['POST'])
def play_game():
    data = request.json
    player_choice = data['player']
    computer_choice = computer_turn()
    result = check_winner(player_choice, computer_choice)

    # Save the result to the database
    with sqlite3.connect('rps_game.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO game_results (player_choice, computer_choice, result) VALUES (?, ?, ?)',
                       (player_choice, computer_choice, result))
        conn.commit()

    return jsonify({'player': player_choice, 'computer': computer_choice, 'result': result})

if __name__ == "__main__":
    app.run(debug=True)
