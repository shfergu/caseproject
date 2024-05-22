from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        case_number = request.form['case_number']
        reason = request.form['reason']
        more_tickets = 'more_tickets' in request.form
        # For now, just print these values to the console
        print(f'Case Number: {case_number}, Reason: {reason}, More Tickets: {more_tickets}')
        return redirect(url_for('index'))
    return render_template('submit.html')

if __name__ == '__main__':
    app.run(debug=True)
