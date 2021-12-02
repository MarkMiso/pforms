from flask import Blueprint, render_template, redirect, url_for, request, flash, send_from_directory
import csv

from pforms.settings import CSV_FOLDER_PATH
from pforms.extensions import db, login_required, current_user
from pforms.models import User, Form, Question, Answer, Submission, Category

form = Blueprint('form', __name__)

@form.route('/forms/home', methods=['GET', 'POST'])
def show_forms():
    categories = Category.query.all()
    forms = Form.query.all()

    if request.method == 'GET':
        return render_template('form_home.html', forms=forms, categories=categories)
    else:
        category = int(request.form.get('category'))
        
        if category < 0 or Category.query.filter_by(id=category).first() is None:
            return render_template('form_home.html', forms=forms, categories=categories)
        else:
            print("dio maledetto mailale")
            forms = Form.query.filter_by(category_id=category).all()
            return render_template('form_home.html', forms=forms, categories=categories)



@form.route('/forms/<form_id>', methods=['GET', 'POST'])
@login_required
def submit_form(form_id):
    form_id = int(form_id)

    #if Submission.query.filter_by(user_id=current_user.id).filter_by(form_id=form_id).first() is not None:
    #    flash("Error: form already answered")
    #    return redirect(url_for('form.show_forms'))

    if request.method == 'GET':
        return render_template('form.html', form_id=form_id, form=Form.query.filter_by(id=form_id).first())
    else:
        form = Form.query.filter_by(id=form_id).first()
        request_form = request.form

        answers = []
        for question in form.questions:
            answer_ids = request_form.getlist(str(question.id))
            print(answer_ids)

            for answer in question.answers:
                if str(answer.id) in answer_ids:
                    if question.dependency_id is None or question.dependency_id in answers:
                        answers.append(answer.id)
                        answer.times_selected += 1

        submit = Submission(form_id=form.id, user_id=current_user.id)
        db.session.add(submit)
        db.session.commit()
        flash('Success! Your answers have been registered')
        return render_template('success.html')

@form.route('/forms/create', methods=['GET', 'POST'])
@login_required
def add_form():
    categories = Category.query.all()

    if request.method == 'GET':
        return render_template('form_create.html', categories=categories)
    else:
        # TODO: prevent creation of empty form
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        questions = request.form.get('questions')
        answers = request.form.get('answers')

        if (int(category) < 0 or Category.query.filter_by(id=category).first() is None):
            form = Form(name=title, description=description, creator_id=current_user.id)
        else :
            form = Form(name=title, description=description, category_id=category, creator_id=current_user.id)
        
        db.session.add(form)
        db.session.commit()

        return redirect(url_for('form.add_questions', form=form.id, questions=questions, answers=answers))

@form.route('/forms/create/<form>/<questions>/<answers>', methods=['GET', 'POST'])
@login_required
def add_questions(form, questions, answers):
    number_of_questions = int(questions)
    number_of_answers = int(answers)
    form_id = int(form)

    if current_user.id != Form.query.filter_by(id=form_id).first().creator_id:
        return "Forbidden: you must be the owner of the form to add questions", 403

    if Question.query.filter_by(form_id=form_id).first() is not None:
        return "Method Not Allowed: you have already created questions for this form", 405

    if request.method == 'GET':
        return render_template('form_create.html', form=form_id, questions=number_of_questions, answers=number_of_answers)
    else:
        # check if dependency order is respected
        request_form = request.form
        for i in range(0, number_of_questions):
            has_dependency = "on" == request_form.get('dependency' + str(i))
            dependency_question = request_form.get('question_dependency' + str(i))
            dependency_answer = request_form.get('answer_dependency' + str(i))

            if has_dependency:
                if int(dependency_question) >= i:
                    flash("Error: a question can't be dependent from an answer that comes after it")
                    return redirect(url_for('form.add_questions', form=form, questions=questions, answers=answers))
                
                if int(dependency_answer) >= number_of_answers:
                    flash("Error: a question can't be dependent from an answer doesn't exist")
                    return redirect(url_for('form.add_questions', form=form, questions=questions, answers=answers))

        # adds questions and answers to database
        question_ids = []
        for i in range(0, number_of_questions):
            question_text = request_form.get('question' + str(i))
            question_multiple = "on" == request_form.get('multiple' + str(i))
            has_dependency = "on" == request_form.get('dependency' + str(i))

            question = Question(text=question_text, form_id=form, multiple=question_multiple)

            if has_dependency:
                dependency_question = int(request_form.get('question_dependency' + str(i)))
                dependency_answer = int(request_form.get('answer_dependency' + str(i)))
                
                question.dependency_id = ((Answer.query.filter_by(question_id=question_ids[dependency_question]).all())[dependency_answer]).id

            db.session.add(question)
            db.session.commit()
            question_ids.append(question.id)

            for j in range(0, number_of_answers):
                answer_text = request_form.get('answer' + str(j) + '-question' + str(i))
                answer = Answer(text=answer_text, question_id=question.id)
                db.session.add(answer)

            db.session.commit()

        flash("Success! Your form has been added.")
        return render_template('success.html')

@form.route('/forms/<form_id>/delete')
@login_required
def delete_form(form_id):
    form_id = int(form_id)
    form = Form.query.filter_by(id=form_id).first()

    if form is None:
        return "Missing File: the form you are trying to delete does not exist", 404

    if current_user.id != form.creator_id:
        return "Forbidden: you must be the owner of the form to delete it", 403
    
    submissions = Submission.query.filter_by(form_id=form_id).all()
    for submission in submissions:
        db.session.delete(submission)

    db.session.commit()
    
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

@form.route('/forms/<form_id>/statistics')
@login_required
def get_data(form_id):
    form_id = int(form_id)
    form = Form.query.filter_by(id=form_id).first()

    if form is None:
        return "Missing File: the form" + str(form_id) + " does not exist", 404

    if form.number_of_submissions() == 0:
        flash("Error: the form '" + form.name + "' has never been answered")
        return redirect(url_for('user.show_user'))

    if current_user.id != form.creator_id:
        return "Forbidden: you must be the creator of the form to wiew it's statistics", 403

    return render_template('statistics.html', form=form)

@form.route('/forms/<form_id>/statistics/csv')
@login_required
def export_data(form_id):
    filename = form_id + '.csv'
    form_id = int(form_id)
    form = Form.query.filter_by(id=form_id).first()

    if form is None:
        return "Missing File: the form " + str(form_id) + " does not exist", 404

    if current_user.id != form.creator_id:
        return "Forbidden: you must be the creator of the form to wiew it's statistics", 403

    header = ['question text', 'answer text', 'times selected']
    data = []

    # fills data
    for question in form.questions:
        for answer in question.answers:
            data.append([question.text, answer.text, answer.times_selected])

    # write csv file
    with open(CSV_FOLDER_PATH + filename, 'w', encoding='UTF', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(header)
        writer.writerows(data)

    # send csv file
    return send_from_directory(directory=CSV_FOLDER_PATH, path=filename, as_attachment=True)