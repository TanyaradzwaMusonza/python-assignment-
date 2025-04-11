# 🧾 Payslip Generator – Python Automation Project

This project automates the generation and distribution of employee payslips using Python. It reads employee data from an Excel file, calculates net salaries, creates styled PDF payslips, and sends them via email to each employee. Built for educational purposes at **Uncommon.org**, the project showcases real-world use of Python for file processing, PDF generation, and email automation.

---

## 📌 Features

- ✅ Reads employee data from an Excel file using **pandas**
- ✅ Automatically calculates **Net Salary**
- ✅ Generates **professional PDF payslips** with company branding
- ✅ Emails each employee their payslip using **smtplib**
- ✅ Handles exceptions and errors gracefully
- ✅ Easy to configure and run from VS Code

---

## 📂 Input File Format

The program requires an Excel file named `employees.xlsx` in the same directory. The sheet must include the following columns:

| Column Name     | Description                       |
|------------------|-----------------------------------|
| `ID`             | Employee ID                      |
| `Name`           | Full name of the employee         |
| `Email`          | Employee's email address          |
| `Basic Salary`   | Monthly base pay (numeric)        |
| `Allowance`      | Additional earnings (numeric)     |
| `Deduction`      | Any deductions (numeric)          |

---

## 🧮 Salary Calculation Formula

```python
Net Salary = Basic Salary + Allowance - Deduction

📄 Output
A personalized, styled PDF payslip for each employee is saved in the payslips/ folder.

Each PDF contains:

Company Header (Uncommon.org)

Employee details (Name, ID, Email)

Salary Breakdown

Net Salary Highlight

Footer with HR contact

✉️ Emailing
Each payslip is automatically emailed as a PDF attachment to the respective employee.

Email subject: Your Payslip for This Month

Email body: Brief message with contact info

Emails are sent securely via Gmail SMTP (SSL on port 465)

⚙️ Setup & Running the Script
Install dependencies
Open your terminal and run:

bash
Copy

Edit
pip install pandas fpdf openpyxl
Configure your email
Replace the placeholder email/password in the script:

python
Copy

Edit
EMAIL_ADDRESS = "youremail@gmail.com"
EMAIL_PASSWORD = "your_app_password"
💡 Use an App Password if you're using Gmail.

Add your employees.xlsx file
Ensure it's in the root directory with correct column headers.

Run the script In your terminal or VS Code:

bash
Copy

Edit
python payslip_generator.py
🛡️ Error Handling
❌ Missing email/password → Console warning

❌ Excel formatting issues → Validation error

❌ Email send failure → Caught with detailed message

✅ All errors handled with try/except blocks

📁 Project Structure
Copy

Edit
📦 payslip-generator
├── employees.xlsx
├── payslip_generator.py
├── README.md
└── payslips/
    └── payslip_001.pdf
🎓 Educational Purpose
This project was created as part of a Python Programming Assignment at Uncommon.org. It applies real-world Python skills like:

Data handling (pandas)

Document formatting (FPDF)

Email integration (smtplib)

Automation and exception handling

✅ Submission Checklist
 Python script payslip_generator.py

 Excel input file employees.xlsx

 Generated PDF payslips in payslips/

 Well-documented README.md


---

🟩 **How to Add This in VS Code:**

1. Right-click in your project folder.
2. Click **New File**, name it `README.md`
3. Paste the above code.
4. Save it.





