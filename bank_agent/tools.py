from datetime import datetime, timedelta
from bank_agent.data import ACCOUNTS, TRANSACTIONS, MERCHANTS

# In prod, this is assumed to be from the verified JWT / OAuth2 session token.
CUSTOMER_ID = "CUST-001"


def get_balance() -> dict:
    """Get the current account balance for the authenticated customer."""
    account = ACCOUNTS.get(CUSTOMER_ID)
    if not account:
        return {"error": "Account not found"}
    return {
        "account": account["masked"],
        "available_balance_gbp": account["available"],
        "current_balance_gbp": account["current"],
        "currency": account["currency"],
        "as_of": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }


def get_transactions(days: int = 30, merchant_filter: str = "", limit: int = 10) -> dict:
    """Get recent transactions for the authenticated customer.

    Args:
        days: How many days back to search (1–90, default 30).
        merchant_filter: Optional partial merchant name to filter by (case-insensitive).
        limit: Maximum number of transactions to return (1–25, default 10).
    """
    days = min(max(int(days), 1), 90)
    limit = min(max(int(limit), 1), 25)
    cutoff = datetime.now() - timedelta(days=days)

    txns = [
        t for t in TRANSACTIONS.get(CUSTOMER_ID, [])
        if datetime.fromisoformat(t["date"]) >= cutoff
    ]
    if merchant_filter:
        txns = [t for t in txns if merchant_filter.lower() in t["merchant"].lower()]

    txns = sorted(txns, key=lambda x: x["date"], reverse=True)[:limit]
    return {
        "transactions": txns,
        "count": len(txns),
        "days_searched": days,
        "filter_applied": merchant_filter or None,
    }


def lookup_merchant(merchant_name: str) -> dict:
    """Look up information about an unfamiliar merchant name from a transaction.

    Args:
        merchant_name: The merchant string exactly as it appears on the transaction.
    """
    name_lower = merchant_name.lower()
    for key, info in MERCHANTS.items():
        if key in name_lower or name_lower in key:
            return {"found": True, "merchant_key": key, **info}
    return {
        "found": False,
        "merchant_name": merchant_name,
        "advice": (
            "This merchant isn't in our database. "
            "If you believe this charge is fraudulent, please call 0800 XXX XXXX "
            "or visit a branch to raise a dispute."
        ),
    }
