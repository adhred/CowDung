from flask import Flask, render_template, request, session, redirect
import random

app = Flask(__name__)
app.secret_key = 'carbon'


@app.route('/')
def index():
    if 'hide_digits' not in session:
        hide = random.randint(1000, 9999)
        hide_digits = [int(i) for i in str(hide)]
        session['hide_digits'] = hide_digits
        session['guesses'] = 0
        session['status'] = 'new'
    return render_template('index.html', status=session['status'])


@app.route('/guess', methods=['POST'])
def guess():
    user_input = int(request.form['guess-value'])
    list_of_digits = [int(i) for i in str(user_input)]

    hide_digits = session['hide_digits']

    cow = 0
    dung = 0

    hide_digits_copy = hide_digits.copy()

    for digit in list_of_digits:
        if digit in hide_digits_copy:
            cow += 1
            hide_digits_copy.remove(digit)

    for i in range(4):
        if hide_digits[i] == list_of_digits[i]:
            dung += 1

    session['guesses'] += 1

    if 'clues' not in session:
        session['clues'] = []

    session['clues'].append({'guess': user_input, 'cow': cow, 'dung': dung})

    if dung == 4:
        session['status'] = f'CORRECT - YOU GUESSED IN {session["guesses"]} MOVES'
    elif session['guesses'] == 15:
        session['status'] = f'Out of guesses! The hidden digits were: {"".join(str(digit) for digit in hide_digits)}'
    else:
        session['status'] = f'Cow: {cow}, Dung: {dung}'

    return redirect('/')


@app.route('/secret')
def secret():
    return "Shhh! Don't Tell Anyone"


@app.route('/admin')
def admin():
    return "By Carbon"


@app.route('/destroy_session')
def destroy():
    session.clear()
    return redirect('/')


@app.errorhandler(404)
def page_not_found():
    return 'Sorry! No response. Try again.'


if __name__ == '__main__':
    app.run(debug=True)
