from flask import render_template
from app import app

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')
