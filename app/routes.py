from flask import Blueprint
from domains import spending_patterns, revenue_forecast, cash_flow

router = Blueprint('router', __name__)

# Spending Patterns Endpoints
router.add_url_rule(
    '/spending-patterns/train', 'train_spending_patterns', spending_patterns.train, methods=['POST']
)
router.add_url_rule(
    '/spending-patterns/insights', 'get_spending_insights', spending_patterns.get_insights, methods=['GET']
)

# Revenue Forecast Endpoints
router.add_url_rule(
    '/revenue-forecast/train', 'train_revenue_forecast', revenue_forecast.train, methods=['POST']
)
# router.add_url_rule(
#     '/revenue-forecast/predict', 'get_revenue_forecast', revenue_forecast.predict, methods=['GET']
# )

# Cash Flow Endpoints
# router.add_url_rule(
#     '/cash-flow/train', 'train_cash_flow', cash_flow.train, methods=['POST']
# )
# router.add_url_rule(
#     '/cash-flow/predict', 'get_cash_flow_forecast', cash_flow.predict, methods=['GET']
# )
