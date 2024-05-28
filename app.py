from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import urllib.parse

app = Flask(__name__)

# Define the Azure SQL Database connection string
params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};"
                                 "SERVER=tcp:shfergusql1.database.windows.net,1433;"
                                 "DATABASE=caseapp;"
                                 "UID=shfergu;"
                                 "PWD=iwbi86iSG!")

app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc:///?odbc_connect={params}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class SupportCase(db.Model):
    __tablename__ = 'support_case'
    id = db.Column(db.Integer, primary_key=True)
    case_number = db.Column(db.String(50), unique=True, nullable=False)
    reason = db.Column(db.String(200), nullable=False)
    more_tickets = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        case_number = request.form['case_number']
        reason = request.form['reason']
        more_tickets = 'more_tickets' in request.form
        new_case = SupportCase(case_number=case_number, reason=reason, more_tickets=more_tickets)
        db.session.add(new_case)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('submit.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        case_number = request.form.get('case_number')
        search_term = request.form.get('search_term')
        more_tickets = request.form.get('more_tickets')

        query = SupportCase.query

        if case_number:
            query = query.filter(SupportCase.case_number.contains(case_number))

        if search_term:
            query = query.filter(
                (SupportCase.case_number.contains(search_term)) |
                (SupportCase.reason.contains(search_term))
            )

        if more_tickets and more_tickets != 'all':
            more_tickets_value = more_tickets == 'true'
            query = query.filter(SupportCase.more_tickets == more_tickets_value)

        results = query.all()
    return render_template('search.html', results=results)

@app.route('/delete_cases', methods=['POST'])
def delete_cases():
    case_ids = request.form.getlist('delete_cases')
    if case_ids:
        for case_id in case_ids:
            case = SupportCase.query.get(case_id)
            if case:
                db.session.delete(case)
        db.session.commit()
    return redirect(url_for('search'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
