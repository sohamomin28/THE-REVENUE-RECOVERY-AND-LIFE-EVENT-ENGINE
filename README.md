# CUSTOMER CHURN REVENUE RISK SYSTEM 🏦 🚀

Predictive Banking Strategy Engine identifying 127 high-priority leads and $265k in Revenue at Risk. Features an ML-powered Executive Dashboard (XGBoost) with full Docker containerization. 

THE STREAMLIT APP- https://the-revenue-recovery-and-life-event-engine-lpkevurq2yrcpreemhh.streamlit.app/

## 📌 Overview
The **Revenue Recovery & Life-Event Engine** serves as a strategic "financial radar" for modern banking institutions. It transforms raw transaction data into actionable foresight by identifying "Silent Churn"—customers migrating funds to fintech competitors—and "Life-Stage Triggers" such as home buying. This project moves a bank from a reactive stance to a proactive one.

## ⚠️ The Problem: "Silent Churn"
Traditional banks often only realize a customer is leaving when the account is closed. This engine identifies "leakage" in real-time by detecting patterns in transaction descriptions and balance velocity (e.g., outflows to Wealthsimple or Tangerine).

## ✨ Features
*   **Competitor Leakage Detection:** Uses NLP/Regex logic to flag outflows to fintech competitors.
*   **Life-Event Clustering:** Groups signals like "Furniture" and "Lawyer Fees" to identify "High Propensity Home Buyers."
*   **Explainable AI (SHAP):** Provides transparent "Reason Codes" (e.g., "Flagged due to 15% balance drop") to meet banking governance standards.
*   **Executive Dashboard:** A Streamlit interface featuring a **Revenue at Risk** gauge and a **Top 10 High-Value Lead List.**

## 🛠 Tech Stack
*   **Data Science:** Python (Pandas, NumPy, Scikit-Learn)
*   **Machine Learning:** XGBoost (Multi-task classification), SMOTE for class imbalance
*   **Explainability:** SHAP (Shapley Additive Explanations)
*   **UI & Inference:** Streamlit
*   **DevOps:** Docker, GitHub Actions (CI/CD)

## 🏗 System Architecture
The engine follows a modular pipeline ensuring data integrity and model transparency:
1.  **Data Factory:** Synthetic data generation with injected "leakage signals."
2.  **Predictive Brain:** Multi-task XGBoost predicting both Churn Risk and Product Propensity.
3.  **Inference Layer:** Integrated logic within Streamlit for real-time customer scoring and "Reason Code" generation.
4.  **Interface:** Executive dashboard for stakeholder visualization.
5.  **Deployment:** Containerized environment via Docker for production reliability.

## 📂 Folder Structure
├── .github/workflows/       # CI/CD (GitHub Actions)
├── app.py                   # Streamlit Executive Dashboard & Inference
├── transaction_generator.py # Phase 1: Data & Signal Injection
├── feature_engineering.py   # Data preprocessing & behavioral tagging
├── model_training.py        # Phase 2: XGBoost & SHAP implementation
├── user_profiles.py         # Customer base demographic logic
├── Dockerfile               # Production containerization
├── requirements.txt         # Project dependencies
└── assets/                  # SHAP summary and performance plots

## 📈 Example Use Case
**The "Silent Churn" Intervention:**
A customer begins moving $2,000 monthly to a competitor. The engine flags this as **Competitor Leakage**. The SHAP reason code identifies a consistent balance drop. The dashboard alerts a bank manager, who can then offer a retention incentive (e.g., a GIC rate bump) to keep the capital within the institution.

## 🚀 Future Improvements
*   **Real-time Stream Processing:** Integrating Kafka for sub-second transaction tagging.
*   **LLM Integration:** Using Large Language Models to summarize customer "Life-Stories" for personal bankers.
*   **Expansion of Triggers:** Adding signals for "New Parent" or "Retirement" inflows.

## 👤 Contact
**Project Lead:** Soha Momin  
**Email:** msoha28@my.yorku.ca
