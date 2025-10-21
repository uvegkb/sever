from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__, template_folder="templates", static_folder="static")

DB = 'likes.db'

def get_likes():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT id, likes FROM cards")
    data = c.fetchall()
    conn.close()
    return {str(row[0]): row[1] for row in data}

def add_like(card_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("UPDATE cards SET likes = likes + 1 WHERE id=?", (card_id,))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html', likes=get_likes())

@app.route('/like/<int:card_id>', methods=['POST'])
def like(card_id):
    add_like(card_id)
    return jsonify(get_likes())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
