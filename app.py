from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import urllib.parse  # Correct import statement for urllib

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
    __tablename__ = 'support_case'  # Explicitly specify the table name
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
        # Print the submitted data to the console for debugging
        print(f'Case Number: {case_number}, Reason: {reason}, More Tickets: {more_tickets}')

        # Create a new SupportCase instance
        new_case = SupportCase(case_number=case_number, reason=reason, more_tickets=more_tickets)

        try:
            # Add the new case to the session and commit to the database
            db.session.add(new_case)
            db.session.commit()
            print("Data committed successfully")
        except Exception as e:
            # Print the error to the console
            print(f"Error: {e}")
            db.session.rollback()  # Rollback the session in case of error

        return redirect(url_for('index'))
    return render_template('submit.html')

 

@app.route('/query', methods=['GET', 'POST'])
def query_cases():
    results = []
    if request.method == 'POST':
        case_number = request.form['case_number']
        results = SupportCase.query.filter_by(case_number=case_number).all()
    return render_template('query.html', results=results)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)