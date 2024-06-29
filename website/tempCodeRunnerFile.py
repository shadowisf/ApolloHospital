@views.route('/search_patient', methods=['GET'])
def search_patient():
    patient_name = request.args.get('patient_name')
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Assuming "Patient" is your table name in the database
    query = "SELECT id, fullname, gender, dob, email, phone, address FROM patient WHERE fullname LIKE %s"
    values = (f"%{patient_name}%",)

    cursor.execute(query, values)
    search_results = cursor.fetchall()

    if not search_results:
        flash("Patient Not Found!")
    else:
        flash("Patient Record Available!")

    cursor.close()
    conn.close()

    return render_template("for_reception_webpages/record_auth.html", search_results=search_results)