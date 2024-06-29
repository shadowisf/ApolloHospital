from flask import Blueprint, render_template,redirect,url_for,flash,request
import mysql.connector
from .auth_utils import db_config
from.test_reports import create_pdf_report_blood_test, create_pdf_report_fees,create_pdf_report_xray

views = Blueprint("views", __name__)

#Home page
@views.route("/")
def home():
    return render_template("general_webpages/index.html")

#Insert patient record
@views.route('/insert_patient', methods = ['GET', 'POST'])
def insert_patient():
   try:
        if request.method == "POST":
            fullname = request.form['fullname']
            gender = request.form['gender']
            email = request.form['email']
            phone = request.form['phone']
            dob = request.form['dob']
            address = request.form['address']
            conn =  mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            query = "INSERT INTO patient (fullname, phone, dob, address, gender, email) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (fullname, phone, dob, address, gender,email)
            cursor.execute(query, values)
            conn.commit()
            flash("patient record ADDED successfully!")
            return redirect(url_for("views.reception"))
   except mysql.connector.Error as err:
       flash("INVALID patient details " + str(err)) 
       return redirect(url_for("views.reception"))
   finally:
        cursor.close()
        conn.close()

#Update current Patietn record
@views.route('/update_patient/<int:patient_id>', methods= ['POST', 'GET'])
def update_patient(patient_id):
    try:
        if request.method == 'POST':
            fullname = request.form['fullname']
            gender = request.form['gender']
            email = request.form['email']
            phone = request.form['phone']
            dob = request.form['dob']
            address = request.form['address']
            conn =  mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            query = "UPDATE patient SET fullname=%s, phone=%s, dob=%s, address = %s, gender = %s, email = %s WHERE id=%s"
            values = (fullname, phone, dob, address, gender, email, patient_id)
            cursor.execute(query, values)
            conn.commit()
            flash("patient record UPDATED successfully!")
            return redirect(url_for('views.reception'))
    except Exception as err:
            flash("UNABLE to update patient record" + str(err))
            return redirect(url_for("views.reception"))
    finally:
        cursor.close()
        conn.close()

#Delete Patient record
@views.route('/delete/<int:patient_id>', methods=['GET'])
def delete_patient(patient_id):
   try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM patient WHERE id=%s", (patient_id,))
        conn.commit()
        flash("patient record DELETED successfully", 'success')
   except mysql.connector.Error as err:
       flash("error occurred: " + str(err), 'danger')
   finally:
       cursor.close()
       conn.close()
   return redirect(url_for("views.reception"))

#Patient authenticator 
@views.route('/search_patient', methods=['GET'])
def search_patient():
        patient_name = request.args.get('patient_name')
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        query = "SELECT id, fullname, gender, dob, email, phone, address FROM patient WHERE fullname LIKE %s"
        values = (f"%{patient_name}%",)
        cursor.execute(query, values)
        data = cursor.fetchall()
        #converts it back to dictionary
        #since this is a tuple value
        # search_results = [dict(zip([column[0] for column in cursor.description], row)) for row in search_results]

        if not data:
            flash("patient record NOT found")
        else:
            flash(f"patient record FOUND for patient {patient_name}")
        cursor.close()
        conn.close()
        return render_template("for_reception_webpages/receptionist.html", data=data)

#Patient authentication page
@views.route("/record_auth")
def record_auth():
    return render_template("for_reception_webpages/record_auth.html")

#Recption user page
@views.route("/reception", methods = ['GET', 'POST'])
def reception():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM patient"
    cursor.execute(query)
    data = cursor.fetchall()
    return render_template("for_reception_webpages/receptionist.html", data = data)

#Doctor availability
@views.route("/doctor", methods=['GET','POST'])
def doctor():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM doctors")
        data = cursor.fetchall()
        if request.method == 'POST':
            day = request.form['day']
            query = "SELECT * FROM doctors WHERE JSON_CONTAINS(doctors.availability, %s)"
            value = ('["' + day + '"]',)
            cursor.execute(query, value)
            data = cursor.fetchall()
            flash(f"doctors availble for {day} are now DISPLAYED")
            data = sorted(data, key=lambda x: x['specialty'])
    except Exception as err:
        flash("error " + str(err))
    finally:
        cursor.close()
        conn.close()
    return render_template("for_reception_webpages/doctor.html", data = data)

#appointment records display
@views.route("/appointment", methods=['GET', 'POST'])
def appointment():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        patient_query = "SELECT id, fullname FROM patient ORDER BY fullname"
        doctor_query = "SELECT id, room_number, name FROM doctors ORDER BY name"
        cursor.execute(patient_query)
        p_data = cursor.fetchall()
        cursor.execute(doctor_query)
        d_data = cursor.fetchall()
        appointment_query = """
            SELECT
                a.id AS appointment_id,
                p.fullname AS patient_name,
                d.name AS doctor_name,
                a.appointment_day,
                TIME_FORMAT(a.appointment_time, '%h:%i %p') AS appointment_time,
                a.room_number
            FROM appointments AS a
            LEFT JOIN patient AS p ON a.patient_id = p.id
            LEFT JOIN doctors AS d ON a.doctor_id = d.id
        """
        cursor.execute(appointment_query)
        appointment_data = cursor.fetchall()
        if not appointment_data:
            flash('appointment record NOT found')
    except Exception as err:
        flash("error " + str(err))
    finally:
        cursor.close()
        conn.close()
    return render_template("for_reception_webpages/appointment.html", appointment_data = appointment_data, p_data = p_data, d_data = d_data)

#add appointment
@views.route("/insert_appointment_record", methods=['POST'])
def insert_appointment_record():
    if request.method == 'POST':
        patient_id = request.form["patient_name"]
        doctor_id = request.form["doctor_name"]
        appointment_day = request.form["appointment_day"]
        appointment_time = request.form["appointment_time"]
        room_no = request.form['room_no']
        existing_appointment_query = """
            SELECT id FROM appointments
            WHERE appointment_day = %s AND appointment_time = %s
        """
        existing_appointment_data = (appointment_day, appointment_time)
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute(existing_appointment_query, existing_appointment_data)
            existing_appointment = cursor.fetchone()
            if existing_appointment:
                flash("appointment slot already TAKEN", "error")
            else:
                insert_query = "INSERT INTO appointments (patient_id, doctor_id, appointment_day, appointment_time, room_number) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(insert_query, (patient_id, doctor_id, appointment_day, appointment_time, room_no))
                conn.commit()
                flash("appointment record ADDED successfully", "success")
        except Exception as err:
            flash("error: " + str(err))
        finally:
            cursor.close()
            conn.close()
    return redirect(url_for('views.appointment'))

@views.route("/search_appointment", methods=['GET', 'POST'])
def search_appointment():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        # Fetch data for populating the dropdown
        patient_query = "SELECT id, fullname FROM patient ORDER BY fullname"
        doctor_query = "SELECT id, room_number, name FROM doctors ORDER BY name"
        cursor.execute(patient_query)
        p_data = cursor.fetchall()
        cursor.execute(doctor_query)
        d_data = cursor.fetchall()
        if request.method == 'POST':
            search_term = request.form['patient_name']
            # Check if the search term is empty
            if search_term:
                # Query to search for appointment records by patient name
                search_query = """
                    SELECT
                        a.id AS appointment_id,
                        p.fullname AS patient_name,
                        d.name AS doctor_name,
                        a.appointment_day,
                        a.appointment_time,
                        a.room_number
                    FROM appointments AS a
                    LEFT JOIN patient AS p ON a.patient_id = p.id
                    LEFT JOIN doctors AS d ON a.doctor_id = d.id
                    WHERE p.fullname LIKE %s
                """
                cursor.execute(search_query, (f'%{search_term}%',))
                appointment_data = cursor.fetchall()
                
                if appointment_data:
                    flash(f"appointment record FOUND for patient {search_term}")
            else:
                # If the search term is empty, return all appointments
                appointment_query = """
                    SELECT
                        a.id AS appointment_id,
                        p.fullname AS patient_name,
                        d.name AS doctor_name,
                        a.appointment_day,
                        a.appointment_time,
                        a.room_number
                    FROM appointments AS a
                    LEFT JOIN patient AS p ON a.patient_id = p.id
                    LEFT JOIN doctors AS d ON a.doctor_id = d.id
                """
                cursor.execute(appointment_query)
                appointment_data = cursor.fetchall()
        else:
            appointment_data = []  # Initialize the data when no search is performed
        # Check if no appointments were found and display a message
        if not appointment_data:
            flash("appointment record NOT found")
        return render_template("for_reception_webpages/appointment.html", appointment_data=appointment_data, p_data=p_data, d_data=d_data)
    except Exception as err:
        flash("error " + str(err))
        return render_template("for_reception_webpages/appointment.html")
    finally:
        cursor.close()
        conn.close()


#cancel appointment
@views.route("/cancel_appointment/<int:appointment_id>", methods=['GET'])
def cancel_appointment(appointment_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        delete_query = "DELETE FROM appointments WHERE id = %s"
        cursor.execute(delete_query, (appointment_id,))
        conn.commit()
        flash("appointment CANCELLED successfully", "success")
    except Exception as err:
        flash("UNABLE to cancel appointment error: " + str(err), "error")
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('views.appointment'))


#views all the  selected doctor appointments
@views.route("/doctor_app", methods=['GET', 'POST'])
def doctor_app():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        doctor_query = "SELECT id, specialty, name FROM doctors ORDER BY name"
        cursor.execute(doctor_query)
        d_data = cursor.fetchall()
        if request.method == 'POST':
            doctor_name = request.form.get("doctor_name")
            appointment_query = """
                SELECT
                    a.id AS appointment_id,
                    p.fullname AS patient_name,
                    d.name AS doctor_name,
                    a.appointment_day,
                    TIME_FORMAT(a.appointment_time, '%h:%i %p') AS appointment_time,
                    a.room_number
                FROM appointments AS a
                LEFT JOIN patient AS p ON a.patient_id = p.id
                LEFT JOIN doctors AS d ON a.doctor_id = d.id
                WHERE d.name = %s
            """
            cursor.execute(appointment_query, (doctor_name,))
            appointment_data = cursor.fetchall()

            
            
            if not appointment_data:
                flash(f"appointment records NOT found for {doctor_name}")
                
            else:
                flash(f"appointment records FOUND for {doctor_name}")
        else:
            appointment_query = """
                SELECT
                    a.id AS appointment_id,
                    p.fullname AS patient_name,
                    d.name AS doctor_name,
                    a.appointment_day,
                    TIME_FORMAT(a.appointment_time, '%h:%i %p') AS appointment_time,
                    a.room_number
                FROM appointments AS a
                LEFT JOIN patient AS p ON a.patient_id = p.id
                LEFT JOIN doctors AS d ON a.doctor_id = d.id
            """
            cursor.execute(appointment_query)
            appointment_data = cursor.fetchall()
    except Exception as err:
        flash("error: " + str(err))
    finally:
        cursor.close()
        conn.close()
    return render_template("for_doctor_webpages/doctor_app.html", appointment_data=appointment_data, d_data=d_data)

#insert medical records
@views.route("/insert_medical_record", methods=['POST'])
def insert_medical_record():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        if request.method == "POST":
            patientName = request.form['patientName']
            doctorName = request.form['doctorName']
            symptoms = request.form['symptoms']
            prescription = request.form['prescription']
            medicalTest = request.form['medicalTest']
            query = "INSERT INTO medical_records (patient_name, doctor_name, symptoms, prescription, medical_test) VALUES (%s, %s, %s, %s,%s)"
            values = (patientName, doctorName, symptoms, prescription, medicalTest)
            cursor.execute(query, values)
            conn.commit()
            flash("medical record ADDED successfully!")
    except Exception as err:
        flash("error " + str(err))
    finally:
        pass
        cursor.close()
        conn.close()
    return redirect(url_for('views.doctor_app'))

#generate bill form
@views.route("/generate_bill", methods=['GET', 'POST'])
def generate_bill():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM medical_records"
    cursor.execute(query)
    data = cursor.fetchall()
    return render_template("for_reception_webpages/generate_bill.html", data = data)

#seqrch a patient medical record for billing
@views.route("/search_patient_bill", methods=['GET', 'POST'])
def search_patient_bill():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        if request.method == "POST":
            patient_medical_bill = request.form['patient_medical_record']
            query = "SELECT * FROM medical_records WHERE patient_name LIKE %s"
            value = (patient_medical_bill,)
            cursor.execute(query, (f'%{patient_medical_bill}%',))
            data = cursor.fetchall()
            if not patient_medical_bill:
                flash("medical record NOT found")
            else:
                flash(f"medical record FOUND for patient {patient_medical_bill}")
    except Exception as err:
        flash("error " + str(err))
    finally:
        cursor.close()
        conn.close()
    return render_template("for_reception_webpages/generate_bill.html", data=data)

#print the bill form as a PDF file
@views.route("/printBill", methods=['POST'])
def printBill():
    if request.method == "POST":
        id = request.form['id']
        patient_name = request.form['patient_name']
        doctor_name = request.form['doctor_name']
        prescription = request.form['prescription']
        medical_test = request.form['medicalTest']
        medical_fees = request.form['medicalFees']
        result = create_pdf_report_fees(id, patient_name, doctor_name, prescription, medical_test, medical_fees)
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("DELETE FROM medical_records WHERE id=%s", (id,))
        conn.commit()
    except Exception as err:
        flash("Error, " + err)
    return result


@views.route("/staff", methods=['GET', 'POST'])
def staff():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM medical_records"
    cursor.execute(query)
    data = cursor.fetchall()
    return render_template("for_staff_webpages/staff.html", data = data)

@views.route("/staff1", methods=['GET', 'POST'])
def staff1():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM medical_records"
    cursor.execute(query)
    data = cursor.fetchall()
    return render_template("for_staff_webpages/staff1.html", data = data)

@views.route("/search_medical_record", methods=['GET', 'POST'])
def search_medical_record():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        if request.method == "POST":
            patient_medical_bill = request.form['patient_medical_record']
            query = "SELECT * FROM medical_records WHERE patient_name LIKE %s"
            value = (patient_medical_bill,)
            cursor.execute(query, (f'%{patient_medical_bill}%',))
            data = cursor.fetchall()
            if not patient_medical_bill:
                flash("patient medical record NOT found")
            else:
                flash(f"patient medical record FOUND for patient {patient_medical_bill}")
    except Exception as err:
        flash("error " + str(err))
    finally:
        cursor.close()
        conn.close()
    return render_template("for_staff_webpages/staff.html", data=data)


@views.route("/print_generate_blood_test", methods=['GET','POST'])
def print_generate_blood_test():
    if request.method == "POST":
        id = request.form['id']
        patient_name = request.form['patient_name']
        doctor_name = request.form['doctor_name']
        prescription = request.form['prescription']
        medical_test = request.form['medicalTest']
        results = create_pdf_report_blood_test(id, patient_name, doctor_name, prescription, medical_test)
    return results


@views.route("/print_generate_xray", methods=['GET', 'POST'])
def print_generate_xray():
    if request.method == "POST":
        id = request.form['id']
        patient_name = request.form['patient_name']
        doctor_name = request.form['doctor_name']
        prescription = request.form['prescription']
        medical_test = request.form['medicalTest']
        results = create_pdf_report_xray(id, patient_name, doctor_name, prescription, medical_test)
    return results
        









