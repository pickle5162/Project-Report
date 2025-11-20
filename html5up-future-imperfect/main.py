from flask import Flask, render_template, request, redirect, url_for, flash
import os
import sqlite3
app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "users.db")
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/single')
def single():
    return render_template('single.html')