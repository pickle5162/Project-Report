from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import sqlite3
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'This_Is_My_Final_Project_Its_Called_Rabbit'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data.db")

def get_all_articles():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = 'SELECT title, content, author, time, category FROM data ORDER BY time DESC'
    cursor.execute(query)
    articles = cursor.fetchall()
    conn.close()
    return articles

def get_articles_by_category(category_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = 'SELECT title, content, author, time, category FROM data WHERE category = ? ORDER BY time DESC'
    cursor.execute(query, (category_name,))
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

def insert_article(title, content, author, category):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    query = 'INSERT INTO data (title, content, author, time, category) VALUES (?, ?, ?, ?, ?)'
    
    try:
        cursor.execute(query, (title, content, author, current_time, category))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"資料庫插入錯誤: {e}") 
        return False
    finally:
        conn.close()

def get_user_by_credentials(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = 'SELECT username FROM user WHERE username = ? AND password = ?'
    try:
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        conn.close()
        return user
    except sqlite3.Error as e:
        print(f"登入查詢錯誤: {e}")
        conn.close()
        return None

def is_email_exist(email):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = 'SELECT 1 FROM user WHERE gmail = ?'
    cursor.execute(query, (email,))
    exists = cursor.fetchone()
    conn.close()
    return exists is not None

def register_new_user(username, password, email):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        query = 'INSERT INTO user (username, password, gmail) VALUES (?, ?, ?)'
        cursor.execute(query, (username, password, email))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"使用者註冊錯誤: {e}")
        return False
    finally:
        conn.close()


# ====================================================================
# 路由 (Routes)
# ====================================================================


@app.route('/')
def index():
    articles = get_all_articles()
    current_username = session.get('username')
    return render_template('index.html',articles=articles, username=current_username)

@app.route('/category/<string:category_name>')
def category_posts(category_name):
    articles = get_articles_by_category(category_name)
    current_username = session.get('username')
    return render_template('index.html', category=category_name, articles=articles, username=current_username)

@app.route('/author/<string:author_name>')
def author_posts(author_name):
    articles = get_articles_by_author(author_name)
    current_username = session.get('username')
    return render_template('index.html', author=author_name, articles=articles, username=current_username)

@app.route('/posts', methods=['POST'])
def create_post():
    if 'username' not in session:
        return jsonify({"success": False, "message": "發佈文章需要先登入"}), 401
    current_author = session['username']
    if request.is_json:
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')
        category = data.get('category')
        if not all([title, content, category]):
            return jsonify({"success": False, "message": "文章標題、內容和種類不能為空"}), 400
        if insert_article(title, content, current_author, category):
            return jsonify({"success": True, "message": "文章發佈成功", "title": title}), 201
        else:
            return jsonify({"success": False, "message": "資料庫儲存失敗，請檢查後端日誌"}), 500
    return jsonify({"success": False, "message": "請求必須是 JSON 格式"}), 415


@app.route('/login', methods=['POST'])
def login_user():
    if not request.is_json:
        return jsonify({"success": False, "message": "請求格式錯誤"}), 400
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not all([username, password]):
        return jsonify({"success": False, "message": "請填寫使用者名稱和密碼"}), 400
    user = get_user_by_credentials(username, password)
    if user:
        session['username'] = username 
        print(f"Session 設置成功: {session.get('username')}")
        return jsonify({"success": True, "message": "登入成功", "username": username}), 200
    else:
        return jsonify({"success": False, "message": "使用者名稱或密碼錯誤"}), 401


@app.route('/register', methods=['POST'])
def register_user():
    if not request.is_json:
        return jsonify({"success": False, "message": "請求格式錯誤"}), 400
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    if not all([username, password, email]):
        return jsonify({"success": False, "message": "所有欄位皆為必填"}), 400
    if not email.endswith("@gmail.com"):
        return jsonify({"success": False, "message": "Email 格式不符，必須是 @gmail.com"}), 400
    if is_email_exist(email):
        return jsonify({"success": False, "message": "Email 已存在"}), 409 
    if register_new_user(username, password, email):
        session['username'] = username 
        return jsonify({"success": True, "message": "註冊成功並已自動登入"}), 201
    else:
        return jsonify({"success": False, "message": "資料庫儲存失敗，請檢查密碼格式"}), 500

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)