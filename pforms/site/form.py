from flask import Blueprint, render_template, redirect, url_for, request, flash

from pforms.extensions import db, login_required, current_user
from pforms.models import User, Form, Question, Answer

form = Blueprint('form', __name__)

@form.route('/forms/home')
def show_forms():
    if current_user.is_authenticated:
        return render_template('formCreation.html')
    else:
        return render_template('formCreation.html')

@form.route('/forms/creation', methods=['GET', 'POST'])
@login_required
def add_form():
    if request.method == 'GET':
        return render_template('formCreation.html')
    else:
        title = request.form.get('title')
        description = request.form.get('description')
        questions = request.form.get('questions')

        form = Form(name=title, description=description, creator=current_user.id)
        db.session.add(form)
        db.session.commit()

        return redirect(url_for('form.add_questions', form=form.id, questions=questions))

@form.route('/forms/creation/<form>/<questions>', methods=['GET', 'POST'])
@login_required
def add_questions(form, questions):
    question_number = int(questions)
    form_id = int(form)

    # TODO: secuirty

    if request.method == 'GET':
        return render_template('formCreation.html', form=form_id, questions=question_number)
    else:
        question_text = request.form.get('question0')
        question_category = "test"
        question_multiple = "on" == request.form.get('multiple0')
        answer_text = request.form.get('answer0-0')

        question = Question(text=question_text, category=question_category, form_id=form, multiple=question_multiple)
        db.session.add(question)
        db.session.commit()
        print(question.id)
        answer = Answer(text=answer_text, question_id=question.id, next_question=None)
        db.session.add(answer)

        for i in range(1, question_number):
            question_text = request.form.get('question' + str(i))
            question_category = "test"
            question_multiple = "on" == request.form.get('multiple' + str(i))
            answer_text = request.form.get('answer0-' + str(i))

            question = Question(text=question_text, category=question_category, form_id=form, multiple=question_multiple)
            db.session.add(question)
            db.session.commit()
            answer.next_question = question.id
            answer = Answer(text=answer_text, question_id=question.id, next_question=None)
            db.session.add(answer)

        db.session.commit()
        flash("Success! Your form has been added.")
        return render_template('success.html')

@form.route('/forms/<form_id>/delete')
@login_required
def delete_form(form_id):
    form_id = int(form_id)

    # TODO: secuirty
    
    form = Form.query.filter_by(id=form_id).first()
    questions = Question.query.filter_by(form_id=form_id).all()
    for question in questions:
        answers = Answer.query.filter_by(question_id=question.id).all()
        for answer in answers:
            db.session.delete(answer)

        db.session.commit()
        db.session.delete(question)

    db.session.commit()
    db.session.delete(form)
    db.session.commit()

    flash("Success! Your form has been deleted")
    return render_template('success.html')