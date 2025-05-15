from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Deck
from config import Config
from FINAL_FLASK.API import get_all_cards
import random
import json

app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader #login manager запамятовує користувача
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/') #основна сторінка
def home():
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST']) #Реєстрація і додання користувача до БД
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter((User.username == username) | (User.email == email)).first(): #перевірка на наявність користувача в БД
            flash('Користувач з таким ім\'ям або поштою вже існує!')
            return redirect(url_for('register'))

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Реєстрація успішна. Тепер увійдіть!')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST']) #логін користувача
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password): #перевірка логіну і паролю
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Невірне ім\'я користувача або пароль.')

    return render_template('login.html')


@app.route('/logout') #вилогування
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required #dashboard це свого роду main з якого можна перейти на самі важливіші html сторінки
def dashboard():
    return render_template('dashboard.html', user=current_user)


@app.route('/generate_deck') #генерація колоди
@login_required
def generate_deck():
    try: #перевірка на помилки
        all_cards = get_all_cards()
        selected_cards = random.sample(all_cards, 8)

        deck = Deck(user_id=current_user.id, cards=json.dumps(selected_cards))
        db.session.add(deck)
        db.session.commit()

        return render_template('deck.html', cards=selected_cards)
    except Exception as e:
        flash(str(e))
        return redirect(url_for('dashboard'))


if __name__ == "__main__":
    with app.app_context(): #Створює контекст програми шоб можна було працювати з базою даних
        db.create_all()
    app.run(debug=True)
