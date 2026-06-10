from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

DB_FILE = 'netflix_system.db'

def init_db():
    """Initialize the database with the catalog table."""
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create the catalog table for Netflix CRUD
    cursor.execute('''CREATE TABLE IF NOT EXISTS catalog (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        creator TEXT NOT NULL,
        media_type TEXT NOT NULL,
        views INTEGER DEFAULT 0
    )''')
    
    conn.commit()
    conn.close()


@app.route('/')
def index():
    """READ: Displays all media items in the catalog."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM catalog")
    media_items = cursor.fetchall()
    conn.close()
    return render_template('index.html', media_items=media_items)


@app.route('/add', methods=['GET', 'POST'])
def add_media():
    """CREATE: Adds a new anime, movie, or show to the database."""
    if request.method == 'POST':
        title = request.form['title']
        creator = request.form['creator']
        media_type = request.form['media_type']
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO catalog (title, creator, media_type) VALUES (?, ?, ?)",
            (title, creator, media_type)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('add_media.html')


@app.route('/watch', methods=['POST'])
def watch_media():
    """UPDATE: Increments the view/stream count of a specific title."""
    media_id = request.form['media_id']
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE catalog SET views = views + 1 WHERE id = ?", (media_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route('/delete/<int:media_id>')
def delete_media(media_id):
    """DELETE: Removes an item from the catalog."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM catalog WHERE id = ?", (media_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route('/trending')
def trending():
    """LEADERBOARD: Displays titles sorted by most views."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM catalog ORDER BY views DESC")
    stats = cursor.fetchall()
    conn.close()
    return render_template('trending.html', stats=stats)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
