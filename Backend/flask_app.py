# Importing necessary modules
from flask import Flask, render_template, request
import pymysql

# Creating a Flask application instance
app = Flask(__name__, template_folder="templates")

##### DATABASE #####

# Database class to handle database operations
class Database:
    def __init__(self):
        # Establishing connection parameters
        host = "khalid88888.mysql.pythonanywhere-services.com"
        user = "khalid88888"
        pwd = "Mazhar2@@1"
        db = "khalid88888$default"

        # Establishing connection with the database
        self.con = pymysql.connect(host=host, user=user, password=pwd, db=db, cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()

    # Method to select all records from the Student table
    def select(self):
        self.cur.execute("SELECT * FROM Student")
        result = self.cur.fetchall()
        return result

    # Method to select all records from the Patients table
    def selectpatients(self):
        self.cur.execute("SELECT * FROM Patients")
        result = self.cur.fetchall()
        return result

    # Method to select all records from the Staff table
    def selectstaff(self):
        self.cur.execute("SELECT * FROM Staff")
        result = self.cur.fetchall()
        return result

    # Method to select all records from the MedicalReports table
    def selectreport(self):
        self.cur.execute("SELECT * FROM MedicalReports")
        result = self.cur.fetchall()
        return result

    # Method to insert a new record into the Student table
    def insert(self, id, name, grade):
        self.cur.execute("INSERT INTO Student (id, name, grade) VALUES (%s, %s, %s)", (id, name, grade))
        self.con.commit()
        return "OK"

    # Method to insert a new record into the Patients table
    def insertPatients(self, patientid, name, age, gender):
        self.cur.execute("INSERT INTO Patients (patientid, name, age, gender) VALUES (%s, %s, %s, %s)", (patientid, name, age, gender))
        self.con.commit()
        return "Patient Added"

    # Method to insert a new record into the Staff table
    def insertstaff(self, staff_id, department_name, description):
        query = "INSERT INTO Staff (staffID, departmentName, description) VALUES (%s, %s, %s)"
        self.cur.execute(query, (staff_id, department_name, description))
        self.con.commit()
        return "Staff member added successfully."

    # Method to remove a staff member from the Staff table
    def removestaff(self, staff_id):
        try:
            query = "DELETE FROM Staff WHERE staffID = %s"
            self.cur.execute(query, (staff_id,))
            self.con.commit()
            return "Staff member removed successfully."
        except Exception as e:
            return f"Error removing staff member: {str(e)}"

    # Method to remove a patient from the Patients table
    def removepatient(self, patient_id):
        try:
            query = "DELETE FROM Patients WHERE patientid = %s"
            self.cur.execute(query, (patient_id,))
            self.con.commit()
            return "Patient removed successfully."
        except Exception as e:
            return f"Error removing patient: {str(e)}"

    # Method to update patient details in the Patients table
    def updatepatient(self, patient_id, name, age, gender):
        try:
            update_query = "UPDATE Patients SET name = %s, age = %s, gender = %s WHERE patientid = %s"
            self.cur.execute(update_query, (name, age, gender,))
            self.con.commit()
            return "Patient updated successfully."
        except Exception as e:
            return f"Error updating patient: {str(e)}"

    # Method to insert a new medical report into the MedicalReports table
    def insert_medical_report(self, report_id, report_date, report_type, description, test_results):
        try:
            insert_query = "INSERT INTO MedicalReports (ReportID, ReportDate, ReportType, Description, TestResults) VALUES (%s, %s, %s, %s, %s)"
            self.cur.execute(insert_query, (report_id, report_date, report_type, description, test_results))
            self.con.commit()
            return "Medical report added successfully."
        except Exception as e:
            return f"Error adding medical report: {str(e)}"

    # Method to delete a medical report from the MedicalReports table
    def delete_medical_report(self, report_id):
        try:
            delete_query = "DELETE FROM MedicalReports WHERE ReportID = %s"
            self.cur.execute(delete_query, (report_id,))
            self.con.commit()
            return "Medical report deleted successfully."
        except Exception as e:
            return f"Error deleting medical report: {str(e)}"

    # Method to update a medical report in the MedicalReports table
    def update_medical_report(self, report_id, report_date, report_type, description, test_results):
        try:
            update_query = "UPDATE MedicalReports SET ReportDate = %s, ReportType = %s, Description = %s, TestResults = %s WHERE ReportID = %s"
            self.cur.execute(update_query, (report_date, report_type, description, test_results, report_id))
            self.con.commit()
            return "Medical report updated successfully."
        except Exception as e:
            return f"Error updating medical report: {str(e)}"

    # Method to insert a new payment record into the Payments table
    def insert_payment(self, payment_id, payment_date, payment_amount, payment_method, payment_status, insurance):
        try:
            insert_query = "INSERT INTO Payments (PaymentID, PaymentDate, PaymentAmount, PaymentMethod, PaymentStatus, Insurance) VALUES (%s, %s, %s, %s, %s, %s)"
            self.cur.execute(insert_query, (payment_id, payment_date, payment_amount, payment_method, payment_status, insurance))
            self.con.commit()
            return "Payment added successfully."
        except Exception as e:
            return f"Error adding payment: {str(e)}"

    # Method to remove a payment record from the Payments table
    def remove_payment(self, payment_id):
        try:
            delete_query = "DELETE FROM Payments WHERE PaymentID = %s"
            self.cur.execute(delete_query, (payment_id,))
            self.con.commit()
            return "Payment removed successfully."
        except Exception as e:
            return f"Error removing payment: {str(e)}"

    # Method to update a payment record in the Payments table
    def update_payment(self, payment_id, payment_date, payment_amount, payment_method, payment_status, insurance):
        try:
            update_query = "UPDATE Payments SET PaymentDate = %s, PaymentAmount = %s, PaymentMethod = %s, PaymentStatus = %s, Insurance = %s WHERE PaymentID = %s"
            self.cur.execute(update_query, (payment_date, payment_amount, payment_method, payment_status, insurance, payment_id))
            self.con.commit()
            return "Payment updated successfully."
        except Exception as e:
            return f"Error updating payment: {str(e)}"

    # Method to retrieve all payments from the Payments table
    def list_payments(self):
        self.cur.execute("SELECT * FROM Payments")
        result = self.cur.fetchall()
        return result

    # Method to close the database connection
    def close_connection(self):
        self.con.close()

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to display the list of students
@app.route('/list')
def list():
    db = Database()
    result = db.select()
    return render_template('results.html', result=result)

# Route to display the list of patients
@app.route('/listpatients')
def listpatients():
    db = Database()
    result = db.selectpatients()
    return render_template('listpatients.html', result=result)

# Route to display the list of staff members
@app.route('/liststaff')
def liststaff():
    db = Database()
    result = db.selectstaff()
    return render_template('liststaff.html', result=result)

# Route to insert a new student record
@app.route('/insert', methods=['GET', 'POST'])
def insert():
    msg = ""
    if request.method == "POST":
        data = request.form
        id = data['id']
        name = data['name']
        grade = data['grade']

        db = Database()
        msg = db.insert(id, name, grade)

    return render_template('form.html', msg=msg)

# Route to insert a new patient record
@app.route('/insertpatients', methods=['GET', 'POST'])
def insertPatients():
    msg = ""
    if request.method == "POST":
        data = request.form
        patientid = data['patientid']
        name = data['name']
        age = data['age']
        gender = data['gender']

        db = Database()
        msg = db.insertPatients(patientid, name, age, gender)

    return render_template('patientform.html', msg=msg)

# Route to insert a new staff member
@app.route('/insertstaff', methods=['GET', 'POST'])
def insertStaff():
    msg = ""
    try:
        if request.method == 'POST':
            staffid = request.form['staffid']
            departmentname = request.form['departmentname']
            description = request.form['description']

            db = Database()
            msg = db.insertstaff(staffid, departmentname, description)
            db.close_connection()
    except Exception as e:
        msg = "An error occurred: " + str(e)
    return render_template('Staffform.html', msg=msg)

# Route to remove a staff member
@app.route('/removestaff', methods=['POST'])
def removestaff():
    if request.method == 'POST':
        staff_id = request.form['staff_id']
        db = Database()
        msg = db.remove_staff(staff_id)
        db.close_connection()
        return render_template('liststaff.html', msg=msg)
    else:
        return render_template('removestaff.html')

# Route to remove a patient
@app.route('/removepatient', methods=['GET', 'POST'])
def removepatient():
    if request.method == 'POST':
        patientid = request.form['patientid']
        db = Database()
        msg = db.removepatient(patientid)
        return render_template('listpatients.html', msg=msg)
    else:
        return render_template('removepatient.html')

# Route to update patient details
@app.route('/updatepatient', methods=['POST'])
def updatepatient():
    if request.method == 'POST':
        patientid = request.form['patientid']
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        db = Database()
        msg = db.update_patient(patientid, name, age, gender)
        db.close_connection()
        return render_template('updatepatient.html', msg=msg)

# Route to insert a new medical report
@app.route('/insertmedicalreport', methods=['POST'])
def insert_medical_report():
    if request.method == 'POST':
        report_id = request.form['report_id']
        report_date = request.form['report_date']
        report_type = request.form['report_type']
        description = request.form['description']
        test_results = request.form['test_results']
        db = Database()
        msg = db.insert_medical_report(report_id, report_date, report_type, description, test_results)
        db.close_connection()
        return render_template('reportform.html', msg=msg)

# Route to delete a medical report
@app.route('/deletemedicalreport', methods=['POST'])
def delete_medical_report():
    if request.method == 'POST':
        report_id = request.form['report_id']
        db = Database()
        msg = db.delete_medical_report(report_id)
        db.close_connection()
        return render_template('removereport.html', msg=msg)

# Route to update a medical report
@app.route('/updatemedicalreport', methods=['POST'])
def update_medical_report():
    if request.method == 'POST':
        report_id = request.form['report_id']
        report_date = request.form['report_date']
        report_type = request.form['report_type']
        description = request.form['description']
        test_results = request.form['test_results']
        db = Database()
        msg = db.update_medical_report(report_id, report_date, report_type, description, test_results)
        db.close_connection()
        return render_template('listreports.html', msg=msg)

# Route to insert a new payment record
@app.route('/insertpayment', methods=['POST'])
def insert_payment():
    if request.method == 'POST':
        payment_id = request.form['payment_id']
        payment_date = request.form['payment_date']
        payment_amount = request.form['payment_amount']
        payment_method = request.form['payment_method']
        payment_status = request.form['payment_status']
        insurance = request.form['insurance']
        db = Database()
        msg = db.insert_payment(payment_id, payment_date, payment_amount, payment_method, payment_status, insurance)
        db.close_connection()
        return render_template('paymentform.html', msg=msg)

# Route to remove a payment record
@app.route('/removepayment', methods=['POST'])
def remove_payment():
    if request.method == 'POST':
        payment_id = request.form['payment_id']
        db = Database()
        msg = db.remove_payment(payment_id)
        db.close_connection()
        return render_template('removepayment.html', msg=msg)

# Route to update a payment record
@app.route('/updatepayment', methods=['POST'])
def update_payment():
    if request.method == 'POST':
        payment_id = request.form['payment_id']
        payment_date = request.form['payment_date']
        payment_amount = request.form['payment_amount']
        payment_method = request.form['payment_method']
        payment_status = request.form['payment_status']
        insurance = request.form['insurance']
        db = Database()
        msg = db.update_payment(payment_id, payment_date, payment_amount, payment_method, payment_status, insurance)
        db.close_connection()
        return render_template('updatepayment.html', msg=msg)

# Route to display the list of payments
@app.route('/listpayments')
def list_payments():
    db = Database()
    payments = db.list_payments()
    db.close_connection()
    return render_template('listpayments.html', payments=payments)

# Main method to run the application
