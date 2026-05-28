from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Patient Table
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100))
    dob = db.Column(db.String(50))
    email = db.Column(db.String(100))
    glucose = db.Column(db.Float)
    haemoglobin = db.Column(db.Float)
    cholesterol = db.Column(db.Float)
    remarks = db.Column(db.String(200))
    score = db.Column(db.Integer)

# Home Page
@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':

        fullname = request.form['fullname']
        dob = request.form['dob']
        email = request.form['email']
        glucose = float(request.form['glucose'])
        haemoglobin = float(request.form['haemoglobin'])
        cholesterol = float(request.form['cholesterol'])

        # AI Prediction Logic
        if haemoglobin < 10:
            remarks = "Low Haemoglobin Risk"
            score = 75
        elif glucose > 140:
            remarks = "High Diabetes Risk"
            score = 90
        elif cholesterol > 200:
            remarks = "High Cholesterol Risk"
            score = 80
        else:
            remarks = "Normal"
            score = 20

        patient = Patient(
            fullname=fullname,
            dob=dob,
            email=email,
            glucose=glucose,
            haemoglobin=haemoglobin,
            cholesterol=cholesterol,
            remarks=remarks,
            score=score
        )

        db.session.add(patient)
        db.session.commit()

        return redirect('/')

    patients = Patient.query.all()

    return render_template('index.html', patients=patients)
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    patient = Patient.query.get(id)

    if request.method == 'POST':

        patient.fullname = request.form['fullname']
        patient.dob = request.form['dob']
        patient.email = request.form['email']
        patient.glucose = float(request.form['glucose'])
        patient.haemoglobin = float(request.form['haemoglobin'])
        patient.cholesterol = float(request.form['cholesterol'])

        # AI Logic
        if patient.haemoglobin < 10:
            patient.remarks = "Low Haemoglobin Risk"
            patient.score = 75

        elif patient.glucose > 140:
            patient.remarks = "High Diabetes Risk"
            patient.score = 90

        elif patient.cholesterol > 200:
            patient.remarks = "High Cholesterol Risk"
            patient.score = 80

        else:
            patient.remarks = "Normal"
            patient.score = 20

        db.session.commit()

        return redirect('/')

    return render_template('edit.html', patient=patient)

# Delete Route
@app.route('/delete/<int:id>')
def delete(id):
    patient = Patient.query.get(id)

    db.session.delete(patient)
    db.session.commit()

    return redirect('/')

# Run App
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
    