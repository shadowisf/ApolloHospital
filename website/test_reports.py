from flask import Response
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Function to create a PDF report
def create_pdf_report_blood_test(id, patient_name, doctor_name, prescription, medical_test):
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)

    # Set title and subtitle
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(300, 750, "Apollo Hospital")
    c.setFont("Helvetica", 14)
    c.drawCentredString(300, 725, "Blood Test Medical Report")

    # Center-align patient name and other details
    c.setFont("Helvetica", 12)
    c.drawString(100, 670, f'Patient Name: {patient_name}')
    c.drawString(100, 650, f'Doctor Name: {doctor_name}')

    # Right side: Prescription and Medical Test
    c.setFont("Helvetica", 12)
    c.drawString(100, 630, f'Prescription: {prescription}')
    c.drawString(100, 610, f'Medical Test: {medical_test}')

    # Add the blood test format
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, 550, "Blood Test: ")
    blood_test_format = [
        "W.B.C:                                                      x1000/mm^3",
        "R.B.C:                                                      Mill/mm^3",
        "Hb:                                                           gm/dl",
        "Hot:                                                          %",
        "M.C.V:                                                      fL",
        "M.C.H:                                                      Pgm",
        "M.C.H.C:                                                   &",
        "Platelet:                                                   x1000/mm^3",
        "PBS:",
    ]
    line_y = 530
    for test_line in blood_test_format:
        line_y -= 20
        c.drawString(120, line_y, test_line)
        c.line(100, line_y - 5, 500, line_y - 5)  # Add a line after each row
    # Add the signature label
    c.setFont("Helvetica", 10)
    c.drawCentredString(300, 305, "Apollo Radiologist Signature:                                    Apollo Mecial staff signature: ")

    # Save the PDF file
    c.showPage()
    c.save()
    pdf_buffer.seek(0)

    # Create a Flask response to send the PDF as a download
    response = Response(pdf_buffer.read(), content_type='application/pdf')
    response.headers['Content-Disposition'] = f'attachment; filename=Blood_test_report_{id}_{patient_name}.pdf'
    return response


def create_pdf_report_fees(id,patient_name, doctor_name, prescription, medical_test, medical_fees):
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    # Set title and subtitle
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(300, 750, "Apollo Hospital")
    c.setFont("Helvetica", 14)
    c.drawCentredString(300, 725, "Medical Fees Report")
    # Center-align patient name and other details
    c.setFont("Helvetica", 12)
    c.drawCentredString(300, 670, f'Patient Name: {patient_name}')
    c.drawCentredString(300, 650, f'Doctor Name: {doctor_name}')
    c.drawCentredString(300, 630, f'Prescription: {prescription}')
    c.drawCentredString(300, 610, f'Medical Test: {medical_test}')
    c.drawCentredString(300, 590, f'Medical Fees: {medical_fees}')
    # Add more space below the patient details
    c.setFont("Helvetica", 12)
    c.drawCentredString(300, 2150, " ")  # Add some space
    #  signature line
    c.line(150, 560, 450, 560)  # Draw a line
    # Add the signature label
    c.setFont("Helvetica", 10)
    c.drawCentredString(300, 550, "Apollo Medical Signature")
    # Save the PDF file
    c.showPage()  # Start a new page (if needed)
    c.save()
    pdf_buffer.seek(0)
    # Create a Flask response to send the PDF as a download
    response = Response(pdf_buffer.read(), content_type='application/pdf')
    response.headers['Content-Disposition'] = f'attachment; filename=Medical_Bill_{id}_{patient_name}.pdf'
    return response


def create_pdf_report_xray(id, patient_name, doctor_name, prescription, medical_test):
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)

    # Set title and subtitle
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(300, 750, "Apollo Hospital")
    c.setFont("Helvetica", 14)
    c.drawCentredString(300, 725, "Blood Test Medical Report")
   
    c.setFont("Helvetica", 12)
    c.drawString(100, 670, f'Patient Name: {patient_name}')
    c.drawString(100, 650, f'Doctor Name: {doctor_name}')

    # Right side: Prescription and Medical Test
    c.setFont("Helvetica", 12)
    c.drawString(100, 630, f'Prescription: {prescription}')
    c.drawString(100, 610, f'Medical Test: {medical_test}')
    
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, 560, "Impression:")
    c.drawString(100, 550, "")
    c.drawString(100, 540, "")
    c.drawString(100, 530, "")
    c.drawString(100, 520, "")

    c.drawString(100, 510, "Findings:")
    c.drawString(100, 500, "") 
    c.drawString(100, 490, "")  
    c.drawString(100, 480, "") 
    c.drawString(100, 470, "")  
    c.drawString(100, 460, "")  

    # Add Labels
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, 430, "Labels:")
    c.drawString(100, 420, "")
    c.drawString(100, 410, "")


    c.setFont("Helvetica", 10)
    c.drawCentredString(300, 305, "Apollo Radiologist Signature:                                    Apollo Medical Staff Signature: ")

    c.showPage()
    c.save()
    pdf_buffer.seek(0)
    
    response = Response(pdf_buffer.read(), content_type='application/pdf')
    response.headers['Content-Disposition'] = f'attachment; filename=xray_report_{id}_{patient_name}.pdf'
    return response
