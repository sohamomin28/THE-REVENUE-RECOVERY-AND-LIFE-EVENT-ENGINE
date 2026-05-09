import pandas as pd
import numpy as np
import xgboost as xgb
import shap
import matplotlib.pyplot as plt
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score


# STEP 1: LOAD DATA
print("Loading data...")

features_df = pd.read_csv('user_features.csv')
profiles_df = pd.read_csv('user_profiles.csv')

master_df = pd.merge(features_df, profiles_df, on='user_id', how='inner')

# STEP 2: TARGET CREATION
master_df['target_churn'] = (
    (master_df['competitor_txn_count'] > 0) |
    (master_df['spend_velocity_index'] < 0.5)
).astype(int)

# Keep only numeric columns
numeric_cols = master_df.select_dtypes(include=[np.number]).columns
data_for_model = master_df[numeric_cols]

X = data_for_model.drop(columns=['user_id', 'target_churn'], errors='ignore')
y = data_for_model['target_churn']

print(f"Features used: {list(X.columns)}")


# STEP 3: TRAIN / TEST SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# STEP 4: SMOTE 
sm = SMOTE(random_state=42)
X_train_res, y_train_res = sm.fit_resample(X_train, y_train)

# IMPORTANT FIX: restore DataFrame structure
X_train_res = pd.DataFrame(X_train_res, columns=X.columns)

print("SMOTE applied successfully.")


# STEP 5: TRAIN XGBOOST MODEL
print("Training XGBoost model...")

model = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=4,
    learning_rate=0.05,
    random_state=42,
    eval_metric='logloss'
)

model.fit(X_train_res, y_train_res)


# STEP 6: EVALUATION
y_pred = model.predict(X_test)

print("\n--- MODEL PERFORMANCE ---")
print(f"Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
print(classification_report(y_test, y_pred))


# STEP 7: SHAP EXPLANATION 
print("\nGenerating SHAP explanation...")

explainer = shap.TreeExplainer(model)
shap_values = explainer(X_test)

plt.figure(figsize=(10, 6))
shap.summary_plot(shap_values, X_test, show=False)
plt.title("Feature Importance (SHAP)")
plt.savefig("shap_summary.png", dpi =300, bbox_inches='tight')
plt.show()


# STEP 8: PRODUCT PROPENSITY ENGINE (LIFE-EVENTS)
print("\n--- Starting Life-Event Engine (Product Propensity) ---")

# Define Product Needs based on the behavioral signals we injected
# 0: None, 1: Mortgage (Shopping Spike), 2: Education/Family (Food/Drink Spike)
def assign_product(row):
    if row['pct_shopping'] > 0.35: 
        return 1  # Logic: Large retail spikes indicate home buying/renovation
    elif row['pct_food_&_drink'] > 0.30: 
        return 2  # Logic: High grocery/dining spend often correlates with family expansion
    else:
        return 0

master_df['target_product'] = master_df.apply(assign_product, axis=1)

# Prepare data for Task B
y_prod = master_df['target_product']
X_train_p, X_test_p, y_train_p, y_test_p = train_test_split(
    X, y_prod, test_size=0.2, random_state=42, stratify=y_prod
)

# Train the Propensity Model
print("Training Product Propensity Model...")
prod_model = xgb.XGBClassifier(
    objective='multi:softmax', 
    num_class=3, 
    n_estimators=100, 
    learning_rate=0.05
)
prod_model.fit(X_train_p, y_train_p)

# Explain the Life-Event Logic
print("Generating SHAP for Life-Events...")
explainer_p = shap.Explainer(prod_model)
shap_values_p = explainer_p(X_test_p)

# We visualize 'Class 1' (Mortgage) to see if pct_shopping is the driver
plt.figure(figsize=(10, 6))
# For multi-class, we index the shap_values for the specific class (1 = Mortgage)
shap.summary_plot(shap_values_p[:, :, 1], X_test_p, show=False)
plt.title("Life-Event Drivers for Mortgage Propensity")
plt.savefig("shap_life_event_mortgage.png", dpi=300, bbox_inches='tight')
plt.show()

print("Phase 3: Executing Comprehensive Strategy Engine")

# Create Strategy Dataset
strategy_df = X_test.copy()

strategy_df['user_id'] = master_df.loc[
    X_test.index,
    'user_id'
]

# Probability Scores
# Binary churn probability
strategy_df['churn_prob'] = model.predict_proba(X_test)[:, 1]

# Multi-class product probabilities
prod_probs = prod_model.predict_proba(X_test)

strategy_df['mortgage_prob'] = prod_probs[:, 1]
strategy_df['family_edu_prob'] = prod_probs[:, 2]

# Strategy Decision Engine
def assign_action(row):

    # CHURN PREVENTION
    if row['churn_prob'] > 0.85:

        if row['competitor_txn_count'] > 2:
            return "RETENTION: Fintech Match Offer"

        return "RETENTION: Loyalty Bonus Offer"

    # HOME BUYING SIGNAL
    elif row['mortgage_prob'] > 0.75:

        if row['annual_income'] > 70000:
            return "SALES: Mortgage Pre-Approval"

        return "SALES: FHSA Invite"

    # FAMILY / EDUCATION SIGNAL
    elif (
        row['family_edu_prob'] > 0.75 or
        row['pct_food_&_drink'] > 0.35
    ):

        if row['age'] < 25:
            return "UPSELL: Student Credit Bundle"

        return "SALES: RESP & Insurance Review"

    # HIGH VALUE CLIENTS
    elif (
        row['annual_income'] > 120000 and
        row['churn_prob'] < 0.30
    ):

        return "PREMIER: Wealth Management Invite"

    # DEFAULT
    else:
        return "STABLE: Standard Marketing"

# Apply Strategy Engine
strategy_df['recommended_action'] = strategy_df.apply(
    assign_action,
    axis=1
)

# Export Priority Customers
final_hitlist = strategy_df[
    strategy_df['recommended_action']
    != "STABLE: Standard Marketing"
].copy()

cols_to_save = [
    'user_id',
    'churn_prob',
    'mortgage_prob',
    'family_edu_prob',
    'recommended_action'
]

final_hitlist[cols_to_save].to_csv(
    'bank_priority_hitlist.csv',
    index=False
)

# Output Summary
print(
    f"DONE! Strategic hit-list saved "
    f"with {len(final_hitlist)} priority customers."
)

print("Sample Output")

print(
    final_hitlist[
        ['user_id', 'recommended_action']
    ].head(10)
)