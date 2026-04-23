from loan_calculations import calculate_emi

BANKS_DATA = [
    {"name": "SBI", "base_rate": 8.50},
    {"name": "HDFC Bank", "base_rate": 8.75},
    {"name": "ICICI Bank", "base_rate": 8.80},
    {"name": "Axis Bank", "base_rate": 8.95},
    {"name": "PNB", "base_rate": 8.40},
    {"name": "Bank of Baroda", "base_rate": 8.45},
]

def compare_banks(principal: float, tenure_years: int) -> list:
    """
    Calculates EMI and Total Repayment for all banks.
    """
    results = []
    for bank in BANKS_DATA:
        calc = calculate_emi(principal, bank["base_rate"], tenure_years)
        results.append({
            "Bank": bank["name"],
            "Interest Rate (%)": bank["base_rate"],
            "Monthly EMI": calc["emi"],
            "Total Interest": calc["total_interest"],
            "Total Repayment": calc["total_repayment"]
        })
    
    # Sort by EMI (lowest first)
    return sorted(results, key=lambda x: x["Monthly EMI"])

def get_recommendations(cibil_score: int) -> list:
    """
    Suggests banks based on CIBIL score tier.
    """
    if cibil_score >= 750:
        return ["SBI", "HDFC Bank", "ICICI Bank", "Axis Bank"]
    elif cibil_score >= 700:
        return ["PNB", "Bank of Baroda", "Axis Bank"]
    elif cibil_score >= 650:
        return ["PNB", "Bank of Baroda"]
    else:
        return ["No immediate recommendations (High Risk)"]

def calculate_savings(comparison_results: list) -> dict:
    """
    Calculates savings between the best and worst bank options.
    """
    if not comparison_results:
        return {"savings": 0, "best_bank": "N/A", "percentage": 0}
        
    best = comparison_results[0]
    worst = comparison_results[-1]
    
    savings = worst["Total Repayment"] - best["Total Repayment"]
    percentage = (savings / worst["Total Repayment"]) * 100 if worst["Total Repayment"] > 0 else 0
    
    return {
        "savings": round(savings, 2),
        "best_bank": best["Bank"],
        "worst_bank": worst["Bank"],
        "percentage": round(percentage, 2)
    }
