from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import sqlite3
from datetime import datetime, timedelta
app = Flask(__name__)
app.permanent_session_lifetime = timedelta(hours=2)
app.secret_key = 'This_Is_My_Final_Project_Its_Called_Rabbit'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data.db")

def get_all_articles():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = 'SELECT id, title, content, author, time, category FROM data ORDER BY time DESC'
    cursor.execute(query)
    articles = cursor.fetchall()
    conn.close()
    return articles

def get_articles_by_category(category_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = 'SELECT id, title, content, author, time, category FROM data WHERE category = ? ORDER BY time DESC'
    cursor.execute(query, (category_name,))
    articles = cursor.fetchall()
    conn.close()
    return articles

def get_articles_by_author(author_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = 'SELECT id, title, content, author, time, category FROM data WHERE author = ? ORDER BY time DESC'
    cursor.execute(query, (author_name,))
    articles = cursor.fetchall()
    conn.close()
    return articles

def get_article_by_id(article_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = 'SELECT id, title, content, author, time, category FROM data WHERE id = ?'
    cursor.execute(query, (article_id,))
    article = cursor.fetchone() 
    conn.close()    
    return article
        
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
        conn.close()
        return None
    
def get_comments_by_article_id(article_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = """SELECT content_id, author, content, time FROM comment WHERE data_id = ? ORDER BY time DESC"""
    cursor.execute(query, (article_id,))
    comments = cursor.fetchall()
    conn.close()
    return comments

def get_comment_count_by_article_id(article_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = "SELECT COUNT(content_id) FROM comment WHERE data_id = ?" 
    cursor.execute(query, (article_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count

def add_comment(article_id, author, content):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = """INSERT INTO comment (data_id, author, content, time)  VALUES (?, ?, ?, ?)"""
    cursor.execute(query, (article_id, author, content, current_time))
    conn.commit()
    return True

def is_gmail_exist(gmail):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = 'SELECT 1 FROM user WHERE gmail = ?'
    cursor.execute(query, (gmail,))
    exists = cursor.fetchone()
    conn.close()
    return exists is not None

def register_new_user(username, password, gmail):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        query = 'INSERT INTO user (username, password, gmail) VALUES (?, ?, ?)'
        cursor.execute(query, (username, password, gmail))
        conn.commit()
        return True
    except sqlite3.Error as e:
        return False
    finally:
        conn.close()
    
def update_article(article_id, title, content, category):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = 'UPDATE data SET title = ?, content = ?, category = ? WHERE id = ?'
    try:
        cursor.execute(query, (title, content, category, article_id))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"資料庫錯誤 (update_article): {e}")
        return False
    finally:
        conn.close()

def delete_article(article_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = 'DELETE FROM data WHERE id = ?'
    try:
        cursor.execute(query, (article_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"資料庫錯誤 (delete_article): {e}")
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
    articles_with_count = []
    for article in articles:
        article_id = article[0]
        comment_count = get_comment_count_by_article_id(article_id)
        article_list = list(article)
        article_list.append(comment_count)
        articles_with_count.append(tuple(article_list))
    return render_template('index.html',articles=articles_with_count, username=current_username)

@app.route('/category')
def category_posts():
    category_name = request.args.get('category_name')
    articles = get_articles_by_category(category_name)
    current_username = session.get('username')
    articles_with_count = []
    for article in articles:
        article_id = article[0]
        comment_count = get_comment_count_by_article_id(article_id)
        article_list = list(article)
        article_list.append(comment_count)
        articles_with_count.append(tuple(article_list))
    return render_template('category.html',articles=articles_with_count, username=current_username)

@app.route('/author')
def author_posts():
    author_name = request.args.get('author_name')
    articles = get_articles_by_author(author_name)
    current_username = session.get('username')
    articles_with_count = []
    for article in articles:
        article_id = article[0]
        comment_count = get_comment_count_by_article_id(article_id)
        article_list = list(article)
        article_list.append(comment_count)
        articles_with_count.append(tuple(article_list))
    return render_template('author.html',articles=articles_with_count, username=current_username)

@app.route('/single')
def single_posts():
    article_id = request.args.get('article_id')
    article = get_article_by_id(article_id)
    comments = get_comments_by_article_id(article_id)
    current_username = session.get('username')
    return render_template('single.html', article=article,username=current_username,comments=comments)


# ====================================================================
# api
# ====================================================================

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
        session.permanent = True
        session['username'] = username 
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
    gmail = data.get('gmail')
    if not all([username, password, gmail]):
        return jsonify({"success": False, "message": "所有欄位皆為必填"}), 400
    if not gmail.endswith("@gmail.com"):
        return jsonify({"success": False, "message": "Gmail 格式不符，必須是 @gmail.com"}), 400
    if is_gmail_exist(gmail):
        return jsonify({"success": False, "message": "Gmail 已存在"}), 409 
    if register_new_user(username, password, gmail):
        session['username'] = username 
        return jsonify({"success": True, "message": "註冊成功並已自動登入"}), 201
    else:
        return jsonify({"success": False, "message": "資料庫儲存失敗，請檢查密碼格式"}), 500

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/edit/<int:article_id>', methods=['POST'])
def edit_post(article_id):
    article = get_article_by_id(article_id)
    current_username = session.get('username')

    if not article or not current_username or current_username != article[3]:
        return redirect(url_for('index'))

    new_title = request.form.get('title')
    new_content = request.form.get('content')
    new_category = request.form.get('category')
    
    if update_article(article_id, new_title, new_content, new_category):
        return redirect(url_for('index'))
    else:
        return "更新失敗，請檢查資料庫連線。", 500

@app.route('/delete/<int:article_id>', methods=['GET', 'POST'])
def delete_post(article_id):
    article = get_article_by_id(article_id)
    current_username = session.get('username')
    if not article:
        return redirect(url_for('index'))
    if not current_username or current_username != article[3]:
        return redirect(url_for('index'))
    if delete_article(article_id):
        return redirect(url_for('index'))
    else:
        return "刪除失敗，請檢查資料庫連線。", 500
    
@app.route('/comment/<int:article_id>', methods=['POST'])
def post_comment(article_id):
    current_username = session.get('username')
    comment_content = request.form.get('comment_content')
    if current_username:
        author_to_save = current_username
    else:
        author_to_save = '訪客'

    if comment_content and comment_content.strip():
        if add_comment(article_id, author_to_save, comment_content):
            return redirect(url_for('single_posts', article_id=article_id))
        else:
            return "留言失敗，資料庫錯誤。", 500
    return redirect(url_for('single_posts', article_id=article_id))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)