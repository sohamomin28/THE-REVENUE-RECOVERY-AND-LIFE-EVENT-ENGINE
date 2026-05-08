import pandas as pd
import numpy as np

# Load the injected data we created
df = pd.read_csv('transactions.csv')
df['date'] = pd.to_datetime(df['date'])

# 1. CATEGORY RATIOS (What % of spend goes where?)
print("Calculating Category Ratios...")
category_pivot = df.pivot_table(
    index='user_id', 
    columns='category', 
    values='amount', 
    aggfunc='sum', 
    fill_value=0
)
# Convert to percentages
category_ratios = category_pivot.div(category_pivot.sum(axis=1), axis=0)
category_ratios.columns = [f'pct_{col.lower().replace(" ", "_")}' for col in category_ratios.columns]

# 2. COMPETITOR VELOCITY (The "Secret Sauce" extraction)
print("Extracting Competitor Signals...")
fintech_keywords = ['WLT-SMPL', 'EQ-BNK', 'TNG-TRF', 'COINBASE']
df['is_competitor'] = df['merchant_description'].str.contains('|'.join(fintech_keywords), regex=True)

competitor_counts = df.groupby('user_id')['is_competitor'].sum().rename('competitor_txn_count')

# 3. BALANCE VELOCITY (First 3 months vs Last 3 months)
print("Analyzing Balance Velocity...")
df['month'] = df['date'].dt.month
first_3_months = df[df['month'] <= 3].groupby('user_id')['amount'].sum()
last_3_months = df[df['month'] >= 10].groupby('user_id')['amount'].sum()

# We calculate the 'velocity' - a ratio > 1 means they are spending more/draining funds recently
balance_velocity = (last_3_months / first_3_months).rename('spend_velocity_index').fillna(1)

# 4. MERGING IT ALL INTO THE MASTER FEATURE TABLE
print("Creating Master Feature Table...")
features_df = pd.concat([category_ratios, competitor_counts, balance_velocity], axis=1).reset_index()

# Handle potential infinities or NaNs from the velocity calculation
features_df = features_df.replace([np.inf, -np.inf], 0).fillna(0)

# Save for XGBoost
features_df.to_csv('user_features.csv', index=False)

print(f"Success! Created {features_df.shape[1]} features for {len(features_df)} users.")
print(features_df.head())