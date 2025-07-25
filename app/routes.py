from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
# @login_required
def home():
    return render_template('home.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash('Credenciales inválidas')
    return render_template('login.html')

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not email or not username or not password or not confirm_password:
            flash('Todos los campos son obligatorios.', 'error')
            return render_template('register.html')

        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'error')
            return render_template('register.html')

        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres.', 'error')
            return render_template('register.html')

        existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
        if existing_user:
            flash('El email o nombre de usuario ya están registrados.', 'error')
            return render_template('register.html')

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
        new_user = User(email=email, username=username, password_hash=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        flash('Usuario creado exitosamente. Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('main.login')) 
        
    return render_template('register.html')


@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

