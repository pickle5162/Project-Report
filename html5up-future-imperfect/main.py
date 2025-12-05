from flask import Flask, render_template, request, redirect, url_for, flash
import os
import sqlite3
app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data.db")

def get_articles_by_category(category_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = 'SELECT title, content, author, time, category FROM data WHERE category = ? ORDER BY time DESC'
    cursor.execute(query, (category_name,))
    articles = cursor.fetchall()
    conn.close()
    return articles

def get_all_articles():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = 'SELECT title, content, author, time, category FROM data ORDER BY time DESC'
    cursor.execute(query)
    articles = cursor.fetchall()
    conn.close()
    return articles

def get_articles_by_author(author_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = 'SELECT title, content, author, time, category FROM data WHERE author = ? ORDER BY time DESC'
    cursor.execute(query, (author_name,))
    articles = cursor.fetchall()
    conn.close()
    return articles

@app.route('/')
def index():
    articles = get_all_articles()
    return render_template('index.html',articles=articles)

@app.route('/category/<string:category_name>')
def category_posts(category_name):
    articles = get_articles_by_category(category_name)
    return render_template('single.html', category=category_name, articles=articles)

@app.route('/author/<string:author_name>')
def author_posts(author_name):
    articles = get_articles_by_author(author_name)
    return render_template('single.html', author=author_name, articles=articles)




if __name__ == '__main__':
    app.run(debug=True)