from fpdf import FPDF
import datetime

class LoanReport(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 20)
        self.set_text_color(40, 70, 150)
        self.cell(0, 10, 'SMART LOAN INTELLIGENCE REPORT', 0, 1, 'C')
        self.set_font('Helvetica', 'I', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f'Generated on: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_loan_report(data: dict):
    """
    Generates a professional PDF report.
    data includes: loan_details, credit_details, bank_comparison, savings
    """
    pdf = LoanReport()
    pdf.add_page()
    
    # 1. Loan Overview Section
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 10, ' 1. LOAN OVERVIEW', 0, 1, 'L', fill=True)
    pdf.ln(5)
    
    pdf.set_font('Helvetica', '', 12)
    pdf.cell(95, 10, f"Loan Amount: {data['principal']:,.2f}", 0, 0)
    pdf.cell(95, 10, f"Tenure: {data['tenure_years']} Years", 0, 1)
    pdf.cell(95, 10, f"Monthly EMI: {data['emi']:,.2f}", 0, 0)
    pdf.cell(95, 10, f"Total Interest: {data['total_interest']:,.2f}", 0, 1)
    pdf.ln(10)
    
    # 2. Credit Analysis
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, ' 2. CREDIT ANALYSIS', 0, 1, 'L', fill=True)
    pdf.ln(5)
    
    pdf.set_font('Helvetica', '', 12)
    pdf.cell(95, 10, f"Estimated CIBIL Score: {data['cibil_score']}", 0, 0)
    pdf.cell(95, 10, f"Category: {data['cibil_category']}", 0, 1)
    pdf.cell(95, 10, f"Debt-to-Income (DTI): {data['dti']}%", 0, 1)
    pdf.ln(10)
    
    # 3. Bank Recommendations
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, ' 3. TOP RECOMMENDATIONS', 0, 1, 'L', fill=True)
    pdf.ln(5)
    
    pdf.set_font('Helvetica', '', 12)
    for rec in data['recommendations']:
        pdf.cell(0, 8, f"- {rec}", 0, 1)
    pdf.ln(10)
    
    # 4. Bank Comparison Table
    pdf.set_font('Helvetica', 'B', 14)
    pdf.cell(0, 10, ' 4. BANK COMPARISON TABLE', 0, 1, 'L', fill=True)
    pdf.ln(5)
    
    # Table Header
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(40, 10, 'Bank', 1)
    pdf.cell(30, 10, 'Rate (%)', 1)
    pdf.cell(40, 10, 'EMI', 1)
    pdf.cell(40, 10, 'Total Int.', 1)
    pdf.cell(40, 10, 'Total Repay.', 1)
    pdf.ln()
    
    # Table Data
    pdf.set_font('Helvetica', '', 10)
    for bank in data['comparison']:
        pdf.cell(40, 8, str(bank['Bank']), 1)
        pdf.cell(30, 8, str(bank['Interest Rate (%)']), 1)
        pdf.cell(40, 8, f"{bank['Monthly EMI']:,.2f}", 1)
        pdf.cell(40, 8, f"{bank['Total Interest']:,.2f}", 1)
        pdf.cell(40, 8, f"{bank['Total Repayment']:,.2f}", 1)
        pdf.ln()
    
    pdf.ln(10)
    
    # 5. Savings Insight
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(0, 150, 0)
    pdf.cell(0, 10, f" SAVINGS OPPORTUNITY: {data['savings_amount']:,.2f} ({data['savings_percent']}%)", 0, 1, 'L')
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Helvetica', 'I', 10)
    pdf.cell(0, 10, f"By choosing {data['best_bank']} instead of {data['worst_bank']}.", 0, 1)

    return pdf.output()
