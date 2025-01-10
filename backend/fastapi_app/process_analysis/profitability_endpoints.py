from fastapi import APIRouter
from analytics.economic.services.metrics import get_economic_metrics

router = APIRouter()

@router.post("/profitability")
def profitability_analysis(cash_flows: list, discount_rate: float, initial_investment: float, gain_from_investment: float, cost_of_investment: float):
    metrics = get_economic_metrics(cash_flows, discount_rate, initial_investment, gain_from_investment, cost_of_investment)
    return metrics
