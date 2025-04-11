import pandas as pd
from fpdf import FPDF
import smtplib
from email.message import EmailMessage

# Your email details
EMAIL_ADDRESS = "musonzaroshly@gmail.com"
EMAIL_PASSWORD = "qthcojmqzyluaixu"  # App password

# Function to send email


def send_email(to_email, filename, employee_name):
    try:
        msg = EmailMessage()
        msg['Subject'] = "Your Monthly Payslip"
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg.set_content(
            f"Hello {employee_name},\n\nPlease find attached your payslip for this month.\n\nRegards,\nYour Company")

        with open(filename, 'rb') as f:
            file_data = f.read()
            msg.add_attachment(file_data, maintype='application',
                               subtype='pdf', filename=filename)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print(f"✅ Email sent successfully to {to_email}")

    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")


# Step 1: Read Excel File
data = pd.read_excel("employees.xlsx")

# Step 2: Calculate Net Salary
data["Net Salary"] = data["Basic Salary"] + \
    data["Allowance"] - data["Deduction"]

# Step 3, 4, 5: Create Payslip and Send Email
for index, row in data.iterrows():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Payslip for {row['Name']}", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Employee ID: {row['ID']}", ln=True)
    pdf.cell(200, 10, txt=f"Email: {row['Email']}", ln=True)
    pdf.cell(200, 10, txt=f"Basic Salary: ${row['Basic Salary']}", ln=True)
    pdf.cell(200, 10, txt=f"Allowance: ${row['Allowance']}", ln=True)
    pdf.cell(200, 10, txt=f"Deduction: ${row['Deduction']}", ln=True)
    pdf.cell(200, 10, txt=f"Net Salary: ${row['Net Salary']}", ln=True)

    # Save as PDF
    filename = f"payslip_{row['ID']}.pdf"
    pdf.output(filename)

    # Send Email
    send_email(row['Email'], filename, row['Name'])
