import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from loan_calculations import calculate_emi

def plot_emi_vs_rate(principal: float, tenure_years: int):
    """
    Plots a line chart of EMI vs Interest Rate (6% to 20%).
    """
    rates = [r/10 for r in range(60, 205, 5)] # 6.0% to 20.0%
    emis = [calculate_emi(principal, r, tenure_years)["emi"] for r in rates]
    
    df = pd.DataFrame({"Interest Rate (%)": rates, "Monthly EMI": emis})
    
    fig = px.line(df, x="Interest Rate (%)", y="Monthly EMI", 
                  title="EMI Sensitivity Analysis",
                  template="plotly_dark",
                  line_shape="spline",
                  markers=True)
    
    fig.update_layout(
        font=dict(family="Inter, sans-serif"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)")
    )
    return fig

def plot_cibil_gauge(score: int):
    """
    Plots a gauge chart for the CIBIL score.
    """
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Credit Score (CIBIL)", 'font': {'size': 24}},
        gauge = {
            'axis': {'range': [300, 900], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "#4ade80"},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [300, 650], 'color': '#ef4444'},
                {'range': [650, 700], 'color': '#f59e0b'},
                {'range': [700, 750], 'color': '#3b82f6'},
                {'range': [750, 900], 'color': '#10b981'}],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': score}
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white", family="Inter, sans-serif"),
        height=300
    )
    return fig

def plot_loan_breakdown(principal: float, total_interest: float):
    """
    Plots a pie chart for Loan Principal vs Total Interest.
    """
    labels = ['Principal', 'Interest']
    values = [principal, total_interest]
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5,
                                 marker_colors=['#3b82f6', '#f87171'])])
    
    fig.update_layout(
        title="Payment Breakdown",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
    )
    return fig
