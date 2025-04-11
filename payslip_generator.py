import pandas as pd
from fpdf import FPDF
import smtplib
from email.message import EmailMessage
import os

# Email credentials
EMAIL_ADDRESS = "musonzaroshly@gmail.com"
EMAIL_PASSWORD = "qthcojmqzyluaixu"  # App password

# Send email function


def send_email(to_email, filename, employee_name):
    try:
        msg = EmailMessage()
        msg['Subject'] = "Your Payslip for This Month"
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg.set_content(
            f"Dear {employee_name},\n\nAttached is your payslip for this month. If you have any questions, feel free to contact HR.\n\nBest regards,\nUncommon Payroll Team"
        )

        with open(filename, 'rb') as f:
            msg.add_attachment(f.read(), maintype='application',
                               subtype='pdf', filename=filename)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print(f"✅ Payslip emailed to {employee_name} ({to_email})")
    except Exception as e:
        print(f"❌ Failed to send email to {employee_name}: {e}")


# Read employee data
data = pd.read_excel("employees.xlsx")
data["Net Salary"] = data["Basic Salary"] + \
    data["Allowance"] - data["Deduction"]

# Create output directory
if not os.path.exists("payslips"):
    os.makedirs("payslips")

# Custom PDF class with header/footer


class PayslipPDF(FPDF):
    def header(self):
        self.set_fill_color(0, 102, 204)  # Blue header
        self.set_text_color(255, 255, 255)
        self.set_font("Arial", 'B', 16)
        self.cell(0, 12, "UNCOMMON.ORG", ln=True, align='C', fill=True)
        self.set_font("Arial", '', 10)
        self.cell(0, 8, "Education | Technology | Purpose",
                  ln=True, align='C', fill=True)
        self.ln(10)
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-20)
        self.set_font("Arial", 'I', 8)
        self.set_text_color(100, 100, 100)
        self.cell(
            0, 10, "This is a computer-generated payslip. For queries, contact payroll@uncommon.org", align='C')


# Generate payslips
for index, row in data.iterrows():
    pdf = PayslipPDF()
    pdf.add_page()

    # Employee info section
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"Payslip for: {row['Name']}", ln=True)

    pdf.set_font("Arial", '', 11)
    pdf.cell(100, 8, f"Employee ID: {row['ID']}")
    pdf.cell(0, 8, f"Email: {row['Email']}", ln=True)
    pdf.ln(5)

    # Draw salary breakdown box
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Salary Breakdown", ln=True)

    pdf.set_font("Arial", '', 11)
    pdf.cell(60, 8, "Basic Salary:", border=1)
    pdf.cell(0, 8, f"${row['Basic Salary']:.2f}", ln=True, border=1, fill=True)

    pdf.cell(60, 8, "Allowance:", border=1)
    pdf.cell(0, 8, f"${row['Allowance']:.2f}", ln=True, border=1, fill=True)

    pdf.cell(60, 8, "Deduction:", border=1)
    pdf.cell(0, 8, f"${row['Deduction']:.2f}", ln=True, border=1, fill=True)

    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 153, 0)
    pdf.cell(60, 10, "Net Salary:", border=1)
    pdf.cell(0, 10, f"${row['Net Salary']:.2f}", ln=True, border=1, fill=True)
    pdf.set_text_color(0, 0, 0)

    # Save to file
    filename = f"payslips/payslip_{row['ID']}.pdf"
    pdf.output(filename)

    # Email the PDF
    send_email(row['Email'], filename, row['Name'])
