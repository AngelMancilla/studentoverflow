from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import Question, Tag, QuestionTag, Answer
from . import db
from sqlalchemy.orm import joinedload
from werkzeug.security import generate_password_hash, check_password_hash

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    questions = Question.query.options(
        joinedload(Question.author),  
        joinedload(Question.tags)     
    ).all()
    return render_template('home.html', questions=questions)


@main_bp.route('/question/new', methods=['GET', 'POST'])
@login_required
def new_question():
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        tags_raw = request.form.get('tags')

        if not title or not body:
            flash('Título y cuerpo de la pregunta son obligatorios.', 'error')
            return render_template('new_question.html', title=title, body=body, tags=tags_raw)

        question = Question(user_id=current_user.id, title=title, body=body)
        db.session.add(question)
        db.session.flush()

        if tags_raw:
            tags_names = [t.strip().lower() for t in tags_raw.split(',') if t.strip()]
            for name in tags_names:
                tag = Tag.query.filter_by(name=name).first()
                if not tag:
                    tag = Tag(name=name)
                    db.session.add(tag)
                    db.session.flush()
                question_tag = QuestionTag(question_id=question.id, tag_id=tag.id)
                db.session.add(question_tag)

        # Commit para guardar permanentemente los cambios
        db.session.commit()

        return redirect(url_for('main.home'))

    return render_template('new_question.html')

@main_bp.route('/question/<int:question_id>/delete', methods=['POST'])
@login_required
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)

    # Validar que el usuario actual sea el dueño
    if question.user_id != current_user.id:
        flash('No tienes permiso para eliminar esta pregunta.', 'error')
        return redirect(url_for('main.home'))

    # Eliminar pregunta y hacer commit
    db.session.delete(question)
    db.session.commit()

    return redirect(url_for('main.home'))

@main_bp.route('/question/edit/<int:question_id>', methods=['GET', 'POST'])
@login_required
def edit_question(question_id):
    question = Question.query.get_or_404(question_id)

    # Solo el dueño puede editar
    if question.user_id != current_user.id:
        flash("No tienes permiso para editar esta pregunta.", "error")
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        tags_raw = request.form.get('tags')

        if not title or not body:
            flash('Título y cuerpo de la pregunta son obligatorios.', 'error')
            return render_template('new_question.html', title=title, body=body, tags=tags_raw)

        # Actualizar campos
        question.title = title
        question.body = body

        # Limpiar tags actuales
        QuestionTag.query.filter_by(question_id=question.id).delete()

        if tags_raw:
            tags_names = [t.strip().lower() for t in tags_raw.split(',') if t.strip()]
            for name in tags_names:
                tag = Tag.query.filter_by(name=name).first()
                if not tag:
                    tag = Tag(name=name)
                    db.session.add(tag)
                    db.session.flush()
                question_tag = QuestionTag(question_id=question.id, tag_id=tag.id)
                db.session.add(question_tag)

        db.session.commit()
        flash('Pregunta actualizada correctamente.', 'success')
        return redirect(url_for('main.home'))

    # GET: mostrar formulario con datos actuales
    current_tags = ', '.join([tag.name for tag in question.tags])
    return render_template('new_question.html', title=question.title, body=question.body, tags=current_tags)

# routes.py
@main_bp.route('/question/<int:question_id>/answer', methods=['POST'])
@login_required
def add_answer(question_id):
    body = request.form.get('body')
    if not body:
        flash("La respuesta no puede estar vacía", "error")
        return redirect(url_for('main.view_question', question_id=question_id))

    answer = Answer(body=body, user_id=current_user.id, question_id=question_id)
    db.session.add(answer)
    db.session.commit()
    flash("Respuesta añadida con éxito", "success")
    return redirect(url_for('main.view_question', question_id=question_id))

