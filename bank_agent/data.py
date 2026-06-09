from datetime import datetime, timedelta


def _ago(days, hour=10):
    return (
        datetime.now() - timedelta(days=days)
    ).replace(hour=hour, minute=0, second=0, microsecond=0).isoformat()


ACCOUNTS = {
    "CUST-001": {
        "masked": "****4821",
        "available": 2847.63,
        "current": 2847.63,
        "currency": "GBP",
    }
}

TRANSACTIONS = {
    "CUST-001": [
        {"id": "T001", "date": _ago(1),  "merchant": "TESCO STORES",          "amount": -47.82,  "currency": "GBP", "category": "Groceries"},
        {"id": "T002", "date": _ago(2),  "merchant": "AMZN MKTP UK",           "amount": -19.99,  "currency": "GBP", "category": "Shopping"},
        {"id": "T003", "date": _ago(2),  "merchant": "NETFLIX.COM",            "amount": -10.99,  "currency": "GBP", "category": "Entertainment"},
        {"id": "T004", "date": _ago(3),  "merchant": "SALARY BACS PAYMENT",    "amount":  4500.00,"currency": "GBP", "category": "Income"},
        {"id": "T005", "date": _ago(4),  "merchant": "TFL TRAVEL CHARGE",      "amount": -32.40,  "currency": "GBP", "category": "Transport"},
        {"id": "T006", "date": _ago(5),  "merchant": "CAFFE NERO",           "amount": -4.75,   "currency": "GBP", "category": "Dining"},
        {"id": "T007", "date": _ago(7),  "merchant": "AMZN MKTP UK",           "amount": -34.99,  "currency": "GBP", "category": "Shopping"},
        {"id": "T008", "date": _ago(8),  "merchant": "DELIVEROO",              "amount": -22.50,  "currency": "GBP", "category": "Dining"},
        {"id": "T009", "date": _ago(10), "merchant": "SPOTIFY AB",             "amount": -9.99,   "currency": "GBP", "category": "Entertainment"},
        {"id": "T010", "date": _ago(12), "merchant": "SHELL PETROL",           "amount": -68.20,  "currency": "GBP", "category": "Transport"},
        {"id": "T011", "date": _ago(15), "merchant": "OCADO RETAIL LTD",       "amount": -89.43,  "currency": "GBP", "category": "Groceries"},
        {"id": "T012", "date": _ago(18), "merchant": "PAYPAL *EBAY",           "amount": -14.00,  "currency": "GBP", "category": "Shopping"},
        {"id": "T013", "date": _ago(20), "merchant": "GOOGLE *ONE STORAGE",    "amount": -1.59,   "currency": "GBP", "category": "Tech"},
        {"id": "T014", "date": _ago(25), "merchant": "JOHN LEWIS PLC",         "amount": -120.00, "currency": "GBP", "category": "Shopping"},
        {"id": "T015", "date": _ago(28), "merchant": "BRITISH GAS DD",         "amount": -85.00,  "currency": "GBP", "category": "Utilities"},
    ]
}

MERCHANTS = {
    "amzn mktp uk": {
        "full_name": "Amazon UK Marketplace",
        "description": "'AMZN MKTP UK' is Amazon's standard UK billing descriptor for marketplace purchases.",
        "website": "amazon.co.uk",
        "legitimate": True,
    },
    "netflix": {
        "full_name": "Netflix",
        "description": "Monthly Netflix streaming subscription.",
        "website": "netflix.com",
        "legitimate": True,
    },
    "spotify": {
        "full_name": "Spotify",
        "description": "Monthly Spotify Premium music subscription.",
        "website": "spotify.com",
        "legitimate": True,
    },
    "tfl": {
        "full_name": "Transport for London",
        "description": "TfL contactless or Oyster card travel charge.",
        "website": "tfl.gov.uk",
        "legitimate": True,
    },
    "deliveroo": {
        "full_name": "Deliveroo",
        "description": "Food delivery order placed via Deliveroo.",
        "website": "deliveroo.co.uk",
        "legitimate": True,
    },
    "google": {
        "full_name": "Google",
        "description": "Google service (e.g. Google One storage). Check myaccount.google.com/payments to identify the product.",
        "website": "google.com",
        "legitimate": True,
    },
    "paypal": {
        "full_name": "PayPal",
        "description": "PayPal payment — check your PayPal account at paypal.com for the underlying merchant.",
        "website": "paypal.com",
        "legitimate": True,
    },
    "caffenero": {
        "full_name": "Caffe Nero",
        "description": "Caffe Nero in-store or drive-through purchase.",
        "website": "caffenero.com",
        "legitimate": True,
    },
}
