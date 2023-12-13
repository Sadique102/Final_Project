from flask import Flask, request, jsonify
import mysql.connector
import random

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

# Initialize the database and create the table if it doesn't exist
def init_db():
    conn = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='rps',
         user='root',
         password='MyN3wP4ssw0rd',
         autocommit=True
    )
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS game_results (
        id INT AUTO_INCREMENT PRIMARY KEY,
        player_choice VARCHAR(10),
        computer_choice VARCHAR(10),
        result VARCHAR(20)
    )
    ''')
    conn.commit()
    conn.close()

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
    conn = mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        database='rps',
        user='root',
        password='MyN3wP4ssw0rd',
        autocommit=True
    )

    cursor = conn.cursor()
    cursor.execute('INSERT INTO game_results (player_choice, computer_choice, result) VALUES (%s, %s, %s)',
                   (player_choice, computer_choice, result))
    conn.commit()
    conn.close()

    return jsonify({'player': player_choice, 'computer': computer_choice, 'result': result})

if __name__ == "__main__":
    app.run(debug=True)