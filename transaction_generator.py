import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

user_df = pd.read_csv('user_profiles.csv')
user_ids = user_df['user_id'].tolist()

merchants = {
    "Food & Drink": ["STARBUCKS #124", "MCDONALDS 0092", "WHOLEFOODS MKT", "CHIPOTLE 22"],
    "Transport": ["UBER *TRIP", "LYFT *RIDE", "SHELL OIL", "CITY-TRANSIT-AUTH"],
    "Shopping": ["AMZN MKTP US", "TARGET STORE", "WALMART.COM", "APPLE.COM/BILL"],
    "Bills": ["VERIZON WIRELESS", "COMCAST CABLE", "GEICO-INSURE", "CON-EDISON NY"]
}

event_clusters = {
    "Relocation": [
        ("U-HAUL RENTAL CAN", 150, 500, "Transport"),
        ("IKEA NORTH YORK", 800, 25000, "Shopping"),
        ("PROPERTY MGMT DEPOSIT", 20000, 45000, "Bills"),
        ("HOME DEPOT", 100, 40000, "Shopping")
    ],
    "Career_Transition": [
        ("YORK-U-TUITION", 4000, 80000, "Bills"),
        ("HARRY ROSEN", 400, 1200, "Shopping"),
        ("APPLE STORE EATON", 1500, 3500, "Shopping"),
        ("LINKEDIN PREMIUM", 40, 600, "Bills")
    ],
    "Family_Expansion": [
        ("BABIES-R-US", 500, 1500, "Shopping"),
        ("HOSPITAL-PARKING", 40, 100, "Transport"),
        ("AMAZON-DIAPER-SUB", 100, 2000, "Shopping"),
        ("UPPABABY-STROLLER", 900, 1800, "Shopping")
    ],
    "Retirement": [
        ("VIKING-CRUISES", 3000, 70000, "Shopping"),
        ("GOLF-TOWN", 500, 2000, "Shopping"),
        ("TRAVEL-INSURANCE", 200, 600, "Bills")
    ]
}

# --- Signal Injection Definitions ---
fintech_competitors = ["WLT-SMPL-TRFR", "EQ-BNK-INT", "TNG-TRF-P2P", "COINBASE-CRPT"]

all_transactions = []
base_date = datetime(2025, 1, 1)

for u_id in user_ids:
    is_at_risk = random.random() < 0.20 # 20% of users are at risk of competitor leakage
    
    num_txns = random.randint(200, 500)

    # 1. Generate Baseline Transactions
    for _ in range(num_txns):
        category = random.choice(list(merchants.keys()))
        merchant = random.choice(merchants[category])
        
        # INJECTION: Competitor Leakage
        # If user is at risk, 10% chance to swap a regular merchant for a fintech competitor
        if is_at_risk and random.random() < 0.10:
            merchant = random.choice(fintech_competitors)
            amount = random.uniform(500, 5000) # Transfers are usually larger than coffee!
        else:
            amount = np.random.lognormal(mean=2.5, sigma=1.0)

        days_to_add = random.randint(0, 364)
        txn_date = base_date + timedelta(days=days_to_add)

        all_transactions.append({
            'user_id': u_id,
            'date': txn_date,
            'amount': round(amount, 2),
            'merchant_description': merchant,
            'category': category
        })

    # 2. INJECTION: Life-Event Clusters (Behavioral Spikes)
    if random.random() < 0.60:
        event = random.choice(list(event_clusters.keys()))
        
        # For 'Homebuyer' (Relocation) or 'Parent' (Family), we ensure they hit specific months
        # Otherwise, random window between day 30 and 330
        event_start_day = random.randint(30, 330)
        event_base_date = base_date + timedelta(days=event_start_day)
        
        for merch, min_a, max_a, cat in event_clusters[event]:
            # Generate 2-3 transactions per signal merchant to create a "dense" cluster
            for _ in range(random.randint(2, 3)):
                offset = random.randint(0, 14)
                txn_date = event_base_date + timedelta(days=offset)
                
                # Apply 300% spike to the upper range to make the signal stand out to XGBoost
                amount = random.uniform(min_a, max_a) * 3.0 
                
                all_transactions.append({
                    'user_id': u_id,
                    'date': txn_date,
                    'amount': round(amount, 2),
                    'merchant_description': merch,
                    'category': cat
                })

transactions_df = pd.DataFrame(all_transactions)
transactions_df = transactions_df.sort_values(by=['user_id', 'date'])
transactions_df['date'] = transactions_df['date'].dt.strftime('%Y-%m-%d')
transactions_df.to_csv('transactions.csv', index=False)

print(f"Success! Generated {len(transactions_df)} transactions with injected signals for {len(user_ids)} users.")