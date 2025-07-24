from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from .models import User
from . import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        name = request.form.get('username')  # ajusta al name real de tu form
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')

        # Validaciones mínimas
        errors = []
        if not name or not email or not password or not confirm:
            errors.append('Todos los campos son obligatorios.')
        if password != confirm:
            errors.append('Las contraseñas no coinciden.')
        if len(password) < 6:
            errors.append('La contraseña debe tener al menos 6 caracteres.')

        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('register.html')

        try:
            user = User(name=name, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Cuenta creada con éxito, ahora inicia sesión.', 'success')
            return redirect(url_for('auth.login'))
        except IntegrityError:
            db.session.rollback()
            flash('El correo ya está registrado.', 'danger')

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user, remember=True)
            next_url = request.args.get('next')
            return redirect(next_url or url_for('main.home'))
        else:
            flash('Credenciales inválidas.', 'danger')

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('auth.login'))
