import mysql.connector
from flask import Flask, jsonify, request, g


DATABASE = 'scores'
USER = 'root'
PASSWORD = 'MyN3wP4ssw0rd'
HOST = '127.0.0.1'
port = 3306,

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = mysql.connector.connect(
            host='127.0.0.1',
            port=3306,
            database='scores',
            user='root',
            password='MyN3wP4ssw0rd',
            autocommit=True
        )
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY AUTO_INCREMENT, player1_score INTEGER, player2_score INTEGER)')
        db.commit()

@app.route('/score', methods=['POST'])
def add_score():
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO scores (player1_score, player2_score) VALUES (%s, %s)', (data['player1'], data['player2']))
    db.commit()
    return jsonify({'message': 'Score added'}), 201

@app.route('/scores', methods=['GET'])
def get_scores():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM scores')
    scores = cursor.fetchall()
    return jsonify([{'player1': row[1], 'player2': row[2]} for row in scores])

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
