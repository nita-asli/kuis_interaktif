# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Gantilah dengan secret key yang aman

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Definisikan kelas User jika belum ada
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class QuizScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    score = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Logika login
    return render_template('login.html')

# Rute untuk logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout successful. Goodbye!', 'success')
    return redirect(url_for('home'))

# Rute untuk registrasi
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Password and Confirm Password must match.', 'error')
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

# Rute untuk papan peringkat
@app.route('/leaderboard')
def leaderboard():
    # Tambahkan logika untuk mengambil dan menampilkan skor dari database
    scores = QuizScore.query.all()
    return render_template('leaderboard.html', scores=scores)

# Rute untuk kuis
@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    if request.method == 'POST':
        # Tambahkan logika untuk mengevaluasi jawaban dan menghitung skor
        # Simpan skor ke database
        score_entry = QuizScore(user_id=current_user.id, score=10)  # Gantilah dengan nilai yang sesuai
        db.session.add(score_entry)
        db.session.commit()
        flash('Quiz submitted successfully. Your score is X.', 'success')
        return redirect(url_for('home'))

    return render_template('quiz.html')

# Rute untuk halaman utama
@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
