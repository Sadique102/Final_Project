import sqlite3
from flask import Flask, jsonify, request, g

DATABASE = 'scores.db'

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        db.cursor().execute('CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY, player1_score INTEGER, player2_score INTEGER)')
        db.commit()

@app.route('/score', methods=['POST'])
def add_score():
    data = request.get_json()
    db = get_db()
    db.execute('INSERT INTO scores (player1_score, player2_score) VALUES (?, ?)', (data['player1'], data['player2']))
    db.commit()
    return jsonify({'message': 'Score added'}), 201

@app.route('/scores', methods=['GET'])
def get_scores():
    db = get_db()
    scores = db.execute('SELECT * FROM scores').fetchall()
    return jsonify([{'player1': row[1], 'player2': row[2]} for row in scores])

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
