import random
from flask import Flask, render_template, request, flash, redirect, url_for, session
# from linux_questions import quiz as quiz_questions
from questions import quiz as quiz_questions

app = Flask(__name__)
app.secret_key = 'secretkey'

random.shuffle(quiz_questions)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['answers'] = {}
        session['questions_remaining'] = len(quiz_questions)
        return redirect(url_for('quiz', current_question=0))

    return render_template('index.html')

@app.route('/quiz/<int:current_question>', methods=['GET', 'POST'])
def quiz(current_question):
    if current_question >= len(quiz_questions):
        return redirect(url_for('result'))

    question_data = quiz_questions[current_question]
    question = question_data['question']
    options = question_data['options']

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'submit':
            selected_option_index = request.form.get('option')
            if selected_option_index is not None:
                if 'answers' not in session:
                    session['answers'] = {}
                session['answers'][str(current_question)] = int(selected_option_index)

                selected_option = options[session['answers'][str(current_question)]].split(')')[0].strip().lower()
                correct_answer = question_data['answer'].split(')')[0].strip().lower()
                if selected_option == correct_answer:
                    flash('Your answer is correct!', 'success')
                else:
                    flash('Your answer is incorrect. Correct answer: {}'.format(question_data['answer']), 'danger')

        elif action == 'next':
            session['questions_remaining'] = session.get('questions_remaining', len(quiz_questions)) - 1
            return redirect(url_for('quiz', current_question=current_question+1))

    questions_remaining = session.get('questions_remaining', len(quiz_questions) - current_question)

    return render_template('quiz.html', question=question, options=options, current_question=current_question, questions_remaining=questions_remaining)

@app.route('/result')
def result():
    score = 0
    if 'answers' in session:
        for i, question in enumerate(quiz_questions):
            if str(i) in session['answers']:
                user_answer = quiz_questions[i]['options'][session['answers'][str(i)]].split(')')[0].strip().lower()
                correct_answer = question['answer'].split(')')[0].strip().lower()
                if user_answer == correct_answer:
                    score += 1

    total_questions = len(quiz_questions)
    return render_template('result.html', score=score, total_questions=total_questions)

if __name__ == '__main__':
    app.run(debug=True)
