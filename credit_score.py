def estimate_cibil_score(monthly_income: float, existing_emi: float, new_emi: float, tenure_years: int) -> dict:
    """
    Simulates a CIBIL score based on financial health indicators.
    Range: 300 - 900
    """
    if monthly_income <= 0:
        return {"score": 300, "category": "Poor", "dti": 1.0}

    total_emi = existing_emi + new_emi
    dti = total_emi / monthly_income
    
    # Base Score
    score = 650
    
    # DTI Impact (Major factor)
    if dti <= 0.20:
        score += 150
    elif dti <= 0.35:
        score += 80
    elif dti <= 0.50:
        score += 0
    elif dti <= 0.65:
        score -= 100
    else:
        score -= 200
        
    # Income Impact (Minor factor)
    if monthly_income > 150000:
        score += 50
    elif monthly_income > 75000:
        score += 25
        
    # Tenure Impact (Stability)
    if tenure_years >= 15:
        score += 30
    elif tenure_years >= 5:
        score += 15
        
    # Boundary constraints
    score = max(300, min(900, int(score)))
    
    # Categorization
    if score >= 750:
        category = "Excellent"
    elif score >= 700:
        category = "Good"
    elif score >= 650:
        category = "Fair"
    else:
        category = "Poor"
        
    return {
        "score": score,
        "category": category,
        "dti": round(dti * 100, 2)  # as percentage
    }
