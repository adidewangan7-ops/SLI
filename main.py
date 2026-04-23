import streamlit as st
import pandas as pd
import datetime
from loan_calculations import calculate_emi, get_amortization_schedule
from credit_score import estimate_cibil_score
from banks import compare_banks, get_recommendations, calculate_savings
from visuals import plot_emi_vs_rate, plot_cibil_gauge, plot_loan_breakdown
from pdf_report import generate_loan_report

# Page Config
st.set_page_config(page_title="Smart Loan Intelligence Dashboard", layout="wide", page_icon="🏦")

# Custom CSS for Fintech Premium Look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .main { background-color: #0f172a; color: white; }
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); }
    
    /* KPI Cards */
    .kpi-container {
        display: flex;
        justify-content: space-between;
        gap: 20px;
        margin-bottom: 30px;
    }
    .kpi-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        flex: 1;
        text-align: center;
        transition: transform 0.3s ease;
    }
    .kpi-card:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.08);
        border-color: #3b82f6;
    }
    .kpi-value { font-size: 24px; font-weight: 700; color: #3b82f6; }
    .kpi-label { font-size: 14px; color: #94a3b8; margin-top: 5px; }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Custom Headers */
    .section-header {
        font-size: 22px;
        font-weight: 600;
        margin-top: 30px;
        margin-bottom: 20px;
        border-left: 4px solid #3b82f6;
        padding-left: 15px;
        color: #f1f5f9;
    }
    
    /* Dataframe Styling */
    .stDataFrame { border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.1); }
    </style>
""", unsafe_allow_html=True)

# Sidebar Inputs
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2830/2830284.png", width=80)
    st.title("Loan Parameters")
    
    st.subheader("Loan Details")
    loan_amount = st.number_input("Loan Amount (₹)", min_value=10000, value=1000000, step=50000)
    annual_rate = st.slider("Interest Rate (%)", min_value=5.0, max_value=20.0, value=8.5, step=0.1)
    tenure_years = st.slider("Tenure (Years)", min_value=1, max_value=30, value=15)
    
    st.divider()
    
    st.subheader("Personal Finance")
    monthly_income = st.number_input("Monthly Income (₹)", min_value=10000, value=75000, step=5000)
    existing_emi = st.number_input("Existing EMIs (₹)", min_value=0, value=0, step=1000)

# Calculations
loan_summary = calculate_emi(loan_amount, annual_rate, tenure_years)
credit_data = estimate_cibil_score(monthly_income, existing_emi, loan_summary["emi"], tenure_years)
comparison_results = compare_banks(loan_amount, tenure_years)
recommendations = get_recommendations(credit_data["score"])
savings_data = calculate_savings(comparison_results)

# --- MAIN DASHBOARD ---
st.title("🏦 SMART LOAN INTELLIGENCE DASHBOARD")
st.markdown("Professional Fintech Advisory & Credit Scoring System")

# KPI Section
st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-value">₹ {loan_summary['emi']:,.2f}</div>
            <div class="kpi-label">Monthly EMI</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-value">{credit_data['score']}</div>
            <div class="kpi-label">CIBIL Score ({credit_data['category']})</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-value">{credit_data['dti']}%</div>
            <div class="kpi-label">DTI Ratio</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-value" style="color: #4ade80;">₹ {savings_data['savings']:,.2f}</div>
            <div class="kpi-label">Potential Savings</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Layout: 2 Columns for overview and charts
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown('<div class="section-header">Loan Overview</div>', unsafe_allow_html=True)
    ov_c1, ov_c2 = st.columns(2)
    ov_c1.metric("Total Interest", f"₹ {loan_summary['total_interest']:,.2f}")
    ov_c2.metric("Total Repayment", f"₹ {loan_summary['total_repayment']:,.2f}")
    
    st.markdown('<div class="section-header">Credit Analysis & Eligibility</div>', unsafe_allow_html=True)
    st.write(f"Based on your profile, your credit rating is **{credit_data['category']}**.")
    st.plotly_chart(plot_cibil_gauge(credit_data["score"]), use_container_width=True)

with col2:
    st.markdown('<div class="section-header">Financial Distribution</div>', unsafe_allow_html=True)
    st.plotly_chart(plot_loan_breakdown(loan_amount, loan_summary["total_interest"]), use_container_width=True)

# Bank Recommendations
st.markdown('<div class="section-header">Bank Recommendations</div>', unsafe_allow_html=True)
rec_cols = st.columns(len(recommendations))
for i, bank in enumerate(recommendations):
    with rec_cols[i]:
        st.info(f"🏆 {bank}")

# Comparison Engine
st.markdown('<div class="section-header">Bank Comparison Engine</div>', unsafe_allow_html=True)
df_comparison = pd.DataFrame(comparison_results)
st.dataframe(df_comparison.style.highlight_min(subset=["Monthly EMI"], color="#10b981").format({"Monthly EMI": "₹ {:,.2f}", "Total Interest": "₹ {:,.2f}", "Total Repayment": "₹ {:,.2f}"}), use_container_width=True)

# Visualization Section
st.markdown('<div class="section-header">Interest Rate Sensitivity</div>', unsafe_allow_html=True)
st.plotly_chart(plot_emi_vs_rate(loan_amount, tenure_years), use_container_width=True)

# Amortization Table
with st.expander("📄 View Amortization Schedule"):
    schedule = get_amortization_schedule(loan_amount, annual_rate, tenure_years)
    st.dataframe(schedule.style.format({"EMI": "₹ {:,.2f}", "Principal Paid": "₹ {:,.2f}", "Interest Paid": "₹ {:,.2f}", "Balance": "₹ {:,.2f}"}), use_container_width=True)

# Report Generation
st.divider()
if st.button("📥 Generate & Download Professional PDF Report"):
    report_data = {
        "principal": loan_amount,
        "tenure_years": tenure_years,
        "emi": loan_summary["emi"],
        "total_interest": loan_summary["total_interest"],
        "cibil_score": credit_data["score"],
        "cibil_category": credit_data["category"],
        "dti": credit_data["dti"],
        "recommendations": recommendations,
        "comparison": comparison_results,
        "savings_amount": savings_data["savings"],
        "savings_percent": savings_data["percentage"],
        "best_bank": savings_data["best_bank"],
        "worst_bank": savings_data["worst_bank"]
    }
    
    pdf_bytes = generate_loan_report(report_data)
    st.download_button(
        label="Download PDF",
        data=pdf_bytes,
        file_name=f"Loan_Intelligence_Report_{datetime.datetime.now().strftime('%Y%m%d')}.pdf",
        mime="application/pdf"
    )
