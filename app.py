from flask import Flask, render_template, request
from scraper import get_result
from datetime import datetime
current_year = datetime.now().year

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        exam = request.form['exam']
        year = request.form['year']
        board = request.form['board']
        roll = request.form['roll']
        reg = request.form['reg']
        result = get_result(exam, year, board, roll, reg)
        return render_template('result.html', result=result)

    # Pass current year to generate year list dynamically
    current_year = datetime.now().year
    return render_template('index.html', current_year=current_year)


if __name__ == '__main__':
    app.run(debug=True)
