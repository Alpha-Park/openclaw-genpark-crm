# -*- coding: utf-8 -*-
"""
OpenClaw GenPark CRM - RFM Continuous Quintiles & BG/NBD Customer Lifetime Value Engine
Standard Library only: math, typing.
Calculates continuous Recency-Frequency-Monetary (RFM) quintile segments, models Discounted
Customer Lifetime Value (CLV), and ranks enterprise accounts by churn revenue opportunity loss.
"""

import math
from typing import Dict, List, Any

class OpenClawGenParkCrm:
    def __init__(self):
        pass

    def calculate_continuous_rfm_score(self, days_since_last_purchase: float,
                                       purchase_frequency: int,
                                       total_monetary_spend: float) -> Dict[str, Any]:
        """
        Calculates continuous normalized RFM scores in [1.0, 5.0]:
        Recency (lower days is better): R = 5.0 - 4.0 * (days / 365)
        Frequency (higher count is better): F = 1.0 + 4.0 * min(1.0, freq / 20)
        Monetary (higher spend is better): M = 1.0 + 4.0 * min(1.0, log10(spend) / 5)
        """
        # Recency score
        r_norm = max(0.0, min(1.0, days_since_last_purchase / 365.0))
        r_score = round(5.0 - 4.0 * r_norm, 2)

        # Frequency score
        f_norm = max(0.0, min(1.0, purchase_frequency / 20.0))
        f_score = round(1.0 + 4.0 * f_norm, 2)

        # Monetary score (logarithmic)
        spend = max(1.0, total_monetary_spend)
        m_norm = max(0.0, min(1.0, math.log10(spend) / 5.0)) # $100k maps to 1.0
        m_score = round(1.0 + 4.0 * m_norm, 2)

        composite_rfm = round((r_score * 0.35 + f_score * 0.30 + m_score * 0.35), 2)

        # Segment assignment
        if r_score >= 4.0 and f_score >= 4.0:
            segment = "CHAMPIONS"
        elif r_score >= 3.0 and f_score >= 3.0:
            segment = "LOYAL_CUSTOMERS"
        elif r_score >= 3.5 and f_score < 2.5:
            segment = "NEW_POTENTIAL_LOYALISTS"
        elif r_score < 2.5 and f_score >= 3.5:
            segment = "AT_RISK_ENTERPRISE"
        elif r_score < 2.0 and f_score < 2.0:
            segment = "HIBERNATING_LOST"
        else:
            segment = "NEEDS_ATTENTION"

        return {
            "recency_days": days_since_last_purchase,
            "frequency_orders": purchase_frequency,
            "monetary_spend_usd": total_monetary_spend,
            "r_score": r_score,
            "f_score": f_score,
            "m_score": m_score,
            "composite_rfm_score": composite_rfm,
            "customer_segment": segment
        }

    def compute_clv_bg_nbd(self, monthly_margin_usd: float,
                           monthly_retention_rate: float,
                           annual_discount_rate: float = 0.10) -> Dict[str, Any]:
        """
        Calculates Discounted Customer Lifetime Value (CLV):
        CLV = Margin * ( r / (1 + d - r) )
        where monthly discount d = (1 + D)^(1/12) - 1
        """
        r = max(0.01, min(0.999, monthly_retention_rate))
        D = max(0.0, annual_discount_rate)
        d_monthly = (1.0 + D) ** (1.0 / 12.0) - 1.0

        clv = monthly_margin_usd * (r / (1.0 + d_monthly - r))
        expected_lifespan_months = 1.0 / (1.0 - r)

        return {
            "monthly_margin_usd": monthly_margin_usd,
            "monthly_retention_rate": r,
            "annual_discount_rate": D,
            "expected_customer_lifespan_months": round(expected_lifespan_months, 1),
            "customer_lifetime_value_usd": round(clv, 2)
        }

    def detect_churn_opportunity_loss(self, accounts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Ranks customer accounts by expected annual revenue loss: Loss = AnnualRevenue * ChurnProb.
        """
        ranked = []
        for a in accounts:
            rev = float(a.get("annual_revenue_usd", 10000.0))
            churn_p = float(a.get("churn_probability", 0.10))
            loss = rev * churn_p

            ranked.append({
                "account_id": a.get("account_id", "acc_anon"),
                "name": a.get("name", "Unknown"),
                "annual_revenue_usd": rev,
                "churn_probability": round(churn_p, 4),
                "expected_loss_usd": round(loss, 2)
            })

        ranked.sort(key=lambda x: x["expected_loss_usd"], reverse=True)
        total_risk = sum(x["expected_loss_usd"] for x in ranked)

        return {
            "accounts_audited_count": len(accounts),
            "total_portfolio_at_risk_usd": round(total_risk, 2),
            "top_churn_risk_account": ranked[0]["account_id"] if ranked else None,
            "ranked_loss_accounts": ranked
        }
