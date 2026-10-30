# -*- coding: utf-8 -*-
from client import OpenClawGenParkCrm

crm = OpenClawGenParkCrm()

# 1. RFM Scoring
rfm = crm.calculate_continuous_rfm_score(days_since_last_purchase=12, purchase_frequency=15, total_monetary_spend=24500.0)
print(f"RFM Analysis: Segment={rfm['customer_segment']} (R={rfm['r_score']}, F={rfm['f_score']}, M={rfm['m_score']})")

# 2. Customer Lifetime Value
clv = crm.compute_clv_bg_nbd(monthly_margin_usd=1200.0, monthly_retention_rate=0.97, annual_discount_rate=0.08)
print(f"\nCLV: ${clv['customer_lifetime_value_usd']} (Lifespan: {clv['expected_customer_lifespan_months']} months)")

# 3. Churn Loss Ranking
accounts = [
    {"account_id": "acc_01", "name": "Venture Corp", "annual_revenue_usd": 120000.0, "churn_probability": 0.35},
    {"account_id": "acc_02", "name": "Apex AI", "annual_revenue_usd": 500000.0, "churn_probability": 0.12},
    {"account_id": "acc_03", "name": "SmallBiz", "annual_revenue_usd": 15000.0, "churn_probability": 0.80}
]
churn = crm.detect_churn_opportunity_loss(accounts)
print(f"\nPortfolio Churn Loss: Total ${churn['total_portfolio_at_risk_usd']} at risk (Top: {churn['top_churn_risk_account']})")
