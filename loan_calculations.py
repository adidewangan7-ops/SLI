import pandas as pd
import numpy as np

def calculate_emi(principal: float, annual_rate: float, tenure_years: int) -> dict:
    """
    Calculates EMI, Total Repayment, and Total Interest.
    
    Args:
        principal: Loan amount
        annual_rate: Annual interest rate (e.g., 8.5 for 8.5%)
        tenure_years: Tenure in years
        
    Returns:
        Dictionary containing emi, total_repayment, and total_interest
    """
    if principal <= 0 or annual_rate <= 0 or tenure_years <= 0:
        return {"emi": 0, "total_repayment": 0, "total_interest": 0}

    monthly_rate = annual_rate / (12 * 100)
    tenure_months = tenure_years * 12
    
    # EMI Formula: P * r * (1+r)^n / ((1+r)^n - 1)
    emi = (principal * monthly_rate * (1 + monthly_rate)**tenure_months) / ((1 + monthly_rate)**tenure_months - 1)
    
    total_repayment = emi * tenure_months
    total_interest = total_repayment - principal
    
    return {
        "emi": round(emi, 2),
        "total_repayment": round(total_repayment, 2),
        "total_interest": round(total_interest, 2)
    }

def get_amortization_schedule(principal: float, annual_rate: float, tenure_years: int) -> pd.DataFrame:
    """
    Generates a monthly amortization schedule.
    """
    monthly_rate = annual_rate / (12 * 100)
    tenure_months = tenure_years * 12
    emi = calculate_emi(principal, annual_rate, tenure_years)["emi"]
    
    schedule = []
    remaining_balance = principal
    
    for month in range(1, tenure_months + 1):
        interest_payment = remaining_balance * monthly_rate
        principal_payment = emi - interest_payment
        remaining_balance -= principal_payment
        
        # Correct negative balance due to rounding
        if remaining_balance < 0:
            remaining_balance = 0
            
        schedule.append({
            "Month": month,
            "EMI": emi,
            "Principal Paid": round(principal_payment, 2),
            "Interest Paid": round(interest_payment, 2),
            "Balance": round(remaining_balance, 2)
        })
        
        if remaining_balance == 0:
            break
            
    return pd.DataFrame(schedule)
