from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import sqlite3
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'Your_Highly_Confidential_And_Complex_Secret_Key_For_Session_Security'
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

# ====================================================================
# 路由 (Routes)
# ====================================================================

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



@app.route('/posts', methods=['POST'])
def create_post():
    if 'username' not in session:
        return jsonify({"success": False, "message": "發佈文章需要先登入"}), 401
    current_author = "Guest Poster"
    
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


# --- 登入/登出 (範例) ---
# ❗ 這是簡化的登入範例，在真實環境中您需要搭配密碼雜湊和更嚴謹的驗證
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 這裡應該檢查資料庫中的使用者名稱和密碼是否匹配
        username = request.form.get('username')
        
        # 假設驗證成功，將使用者名稱存入 Session
        session['username'] = username 
        
        # 導向主頁
        return redirect(url_for('/'))
    
    return render_template('login.html') 

@app.route('/logout')
def logout():
    session.pop('username', None) # 從 Session 中移除使用者名稱
    return redirect(url_for('index'))




if __name__ == '__main__':
    app.run(debug=True)