from flask import *
from flask_sqlalchemy import *

app = Flask(__name__)

app.config["SECRET_KEY"]="secret"

app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///medical_records.db"
database=SQLAlchemy(app)

app.config["SQLALCHEMY_BINDS"]={
    "user":"sqlite:///user.db"
}

class User(database.Model):
    __bind_key__ = 'user'
    id=database.Column(database.Integer, primary_key=True)
    username=database.Column(database.String, unique=True)
    password=database.Column(database.String)

    def __init__(self, username, password):
        self.username=username
        self.password=password

database.create_all()
database.session.commit()

class Medical_Records(database.Model):
    id=database.Column(database.Integer, primary_key=True)
    first_name=database.Column(database.String)
    middle_initial=database.Column(database.String)
    surname=database.Column(database.String)
    age=database.Column(database.String)
    admission_day=database.Column(database.String)
    admission_month=database.Column(database.String)
    admission_year=database.Column(database.String)
    admission_date=database.Column(database.String)
    case_number=database.Column(database.String)
    discharge_day=database.Column(database.String)
    discharge_month=database.Column(database.String)
    discharge_year=database.Column(database.String)
    discharge_date=database.Column(database.String)
    borrower=database.Column(database.String)
    borrowed_day=database.Column(database.String)
    borrowed_month=database.Column(database.String)
    borrowed_year=database.Column(database.String)
    borrowed_date=database.Column(database.String)
    returned_day=database.Column(database.String)
    returned_month=database.Column(database.String)
    returned_year=database.Column(database.String)
    returned_date=database.Column(database.String)

    def __init__(self, first_name, middle_initial, surname, age, admission_day, admission_month , admission_year , admission_date, case_number, discharge_day, discharge_month , discharge_year , discharge_date, borrower, borrowed_day, borrowed_month , borrowed_year , borrowed_date, returned_day, returned_month, returned_year, returned_date):
        self.first_name=first_name
        self.middle_initial=middle_initial
        self.surname=surname
        self.age=age
        self.admission_day=admission_day
        self.admission_month=admission_month
        self.admission_year=admission_year
        self.admission_date=admission_date
        self.case_number=case_number
        self.discharge_day=discharge_day
        self.discharge_month=discharge_month
        self.discharge_year=discharge_year
        self.discharge_date=discharge_date
        self.borrower=borrower
        self.borrowed_day=borrowed_day
        self.borrowed_month=borrowed_month
        self.borrowed_year=borrowed_year
        self.borrowed_date=borrowed_date
        self.returned_day=returned_day
        self.returned_month=returned_month
        self.returned_year=returned_year
        self.returned_date=returned_date


database.create_all()
database.session.commit()

@app.route("/", methods=['GET','POST'])

@app.route("/logs", methods=['GET','POST'])
def logs():
        
        if request.method=="POST":
            if "first_name" in request.form:
                first_name=request.form["first_name"]
                middle_initial=request.form["middle_initial"]
                surname=request.form["surname"]
                age=request.form["age"]
                case_number=request.form["case_number"]
                admission_day=request.form["admission_day"] 
                admission_month=request.form["admission_month"]
                admission_year=request.form["admission_year"]
                admission_date=admission_day + "/" + admission_month + "/" + admission_year
                discharge_day=request.form["discharge_day"]
                discharge_month=request.form["discharge_month"]
                discharge_year=request.form["discharge_year"]
                discharge_date=discharge_day + "/" + discharge_month + "/" + discharge_year
                borrower=request.form["borrower"]
                borrowed_day=request.form["borrowed_day"]
                borrowed_month=request.form["borrowed_month"]
                borrowed_year=request.form["borrowed_year"]
                borrowed_date=borrowed_day + "/" + borrowed_month + "/" + borrowed_year

                if "returned_day" in request.form and "returned_month" in request.form and "returned_year" in request.form:
                    returned_day=request.form["returned_day"]
                    returned_month=request.form["returned_month"]
                    returned_year=request.form["returned_year"]
                    returned_date=returned_day + "/" + returned_month + "/" + returned_year

                else:
                    returned_day = "N/A"
                    returned_month = "N/A"
                    returned_year = "N/A"
                    returned_date = "N/A"

                mr=Medical_Records(first_name, middle_initial, surname, age, admission_day, admission_month, admission_year, admission_date, case_number, discharge_day, discharge_month, discharge_year,discharge_date, borrower, borrowed_day, borrowed_month ,borrowed_year,borrowed_date, returned_day, returned_month, returned_year, returned_date)

                database.session.add(mr)
                database.session.commit()



         
        mr=Medical_Records.query.all()
        return render_template('logs.html', mr=mr)



@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id):

    delete_id = Medical_Records.query.get_or_404(id)
    database.session.delete(delete_id)
    database.session.commit()
    med=Medical_Records.query.all()

    return redirect(url_for('logs', mr=med))

@app.route("/return/<int:id>", methods=["GET", "POST"])
def returned(id):

    if request.method == "POST":

        return_id = Medical_Records.query.get_or_404(id)
        return_id.returned_day = request.form["returned_day"]
        return_id.returned_month = request.form["returned_month"]
        return_id.returned_year = request.form["returned_year"]
        return_id.returned_date = request.form["returned_day"] + "/" + request.form["returned_month"] + "/" + request.form["returned_year"]
            
        database.session.commit()

    
    med=Medical_Records.query.all()

    return redirect(url_for("logs", mr=med))



@app.route('/search', methods=['GET' , 'POST'])
def search():
    if  request.method == 'POST':
        
        form= request.form
        search_value = form['search_string']
        search = "%{}%".format(search_value)
        results = Medical_Records.query.filter((
                Medical_Records.borrower.like(search)) |
                (Medical_Records.first_name.like(search)) |
                (Medical_Records.case_number.like(search)) |
                (Medical_Records.returned_date.like(search)) |
                (Medical_Records.surname.like(search))).all()


        return render_template('logs.html', mr=results)
    else:
        return redirect('logs')
    
  

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    mr = Medical_Records.query.get_or_404(id)

    if request.method == 'POST':
        if "edit" in request.form:
            first_name = request.form.get('first_name')
            middle_initial = request.form.get('middle_initial')
            surname = request.form.get('surname')
            age = request.form.get('age')
            admission_day = request.form.get('admission_day')
            admission_month = request.form.get('admission_month')
            admission_year = request.form.get('admission_year')
            case_number = request.form.get('case_number')
            discharge_day = request.form.get('discharge_day')
            discharge_month = request.form.get('discharge_month')
            discharge_year = request.form.get('discharge_year')
            borrower = request.form.get('borrower')
            borrowed_day = request.form.get('borrowed_day')
            borrowed_month = request.form.get('borrowed_month')
            borrowed_year = request.form.get('borrowed_year')
            returned_day = request.form.get('returned_day')
            returned_month = request.form.get('returned_month')
            returned_year = request.form.get('returned_year')

            if first_name:
                mr.first_name = first_name
            if middle_initial:
                mr.middle_initial = middle_initial
            if surname:
                mr.surname = surname

            if age:
                mr.age = age

            if admission_day and admission_month and admission_year:
                mr.admission_date= admission_day + "/" + admission_month + "/" + admission_year
            
            if case_number:
                mr.case_number = case_number
            if discharge_day and discharge_month and discharge_year:
                mr.discharge_date= discharge_day + "/" + discharge_month + "/" + discharge_year
            if borrower:
                mr.borrower = borrower
            if borrowed_day and borrowed_month and borrowed_year:
                mr.borrowed_date= borrowed_day + "/" + borrowed_month + "/" + borrowed_year
            if returned_day and returned_month and returned_year:
                mr.returned_date= returned_day + "/" + returned_month + "/" + returned_year

            database.session.commit()

            return redirect(url_for('logs'))

    return render_template('update.html', mr=mr)



if __name__ == "__main__":
    app.run()