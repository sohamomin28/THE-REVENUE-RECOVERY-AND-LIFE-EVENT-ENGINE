# THE-REVENUE-RECOVERY-AND-LIFE-EVENT-ENGINE

Predictive Banking Strategy Engine identifying 127 high-priority leads and $265k in Revenue at Risk. Features an ML-powered Executive Dashboard (XGBoost/RF) with full Docker containerization 

THE STREAMLIT APP- https://the-revenue-recovery-and-life-event-engine-lpkevurq2yrcpreemhh.streamlit.app/



# Revenue Recovery & Life-Event Engine 🏦 🚀



**Predictive Banking Strategy Engine identifying 127 high-priority leads and $265k in Revenue at Risk.**



---



## 📌 Overview



The **Revenue Recovery & Life-Event Engine** serves as a strategic "financial radar" for modern banking institutions. It transforms raw, messy transaction data into actionable foresight by identifying "Silent Churn"—customers slowly migrating funds to fintech competitors—and "Life-Stage Triggers" such as home buying or starting a business. This project moves a bank from a reactive stance to a proactive one, allowing for targeted intervention before capital leaves the institution.



## ⚠️ The Problem: "Silent Churn"



Traditional banks like RBC or TD are losing deposits to nimble fintechs (Wealthsimple, EQ Bank). Often, banks only realize a customer is leaving when the account is closed. This engine identifies the "leakage" in real-time by detecting patterns in transaction descriptions and balance velocity.



## ✨ Features



* **Competitor Leakage Detection:** Uses NLP/Regex to flag outflows to competitors like Wealthsimple (WLT-SMPL) or Tangerine (TNG-TRF).





* **Life-Event Clustering:** Groups behavioral signals like spikes in "Furniture" and "Lawyer Fees" to identify "High Propensity Home Buyers".





* **Explainable AI (SHAP):** Provides transparent "Reason Codes" (e.g., *"Flagged due to 15% balance drop"*) to meet banking risk and governance standards.





* **Executive Dashboard:** A Streamlit interface featuring a **Revenue at Risk** gauge and a **Top 10 High-Value Lead List**.







## 🛠 Tech Stack



* **Data Science:** Python (Pandas, NumPy, Scikit-Learn)





* **Machine Learning:** XGBoost (Multi-task classification), SMOTE for class imbalance





* **Explainability:** SHAP Values





* **Backend & API:** FastAPI





* **Frontend:** Streamlit





* **DevOps:** Docker, GitHub Actions







## 🏗 System Architecture



The engine follows a 5-phase modular pipeline ensuring data integrity and model transparency:



1. **Data Factory:** Synthetic data generation with injected "leakage signals".





2. **Predictive Brain:** Multi-task XGBoost predicting both Churn Risk and Product Propensity.





3. **API Engine:** FastAPI wrapper for real-time customer action scoring.





4. **Interface:** Streamlit dashboard for stakeholder visualization.





5. **Deployment:** Containerized environment via Docker for production reliability.







---



## 📂 Folder Structure



```text

├── .github/workflows/       # CI/CD (GitHub Actions)

├── app.py                   # Streamlit Executive Dashboard

├── transaction_generator.py # Phase 1: Data & Signal Injection

├── feature_engineering.py   # Data preprocessing & behavioral tagging

├── model_training.py        # Phase 2: XGBoost & SHAP implementation

├── user_profiles.py         # Customer base demographic logic

├── Dockerfile               # Production containerization

├── requirements.txt         # Project dependencies

└── assets/                  # SHAP summary and performance plots



```



---



## 📈 Example Use Case



**The "Silent Churn" Intervention:**

A customer begins moving $2,000 monthly to a "WLT-SMPL" account. The engine flags this as **Competitor Leakage**. The SHAP reason code identifies a consistent 15% balance drop. The dashboard alerts a bank manager, who offers a **1% GIC rate bump**, successfully retaining the deposit within the bank.



## 🚀 Future Improvements



* **Real-time Stream Processing:** Integrating Kafka for sub-second transaction tagging.

* **LLM Integration:** Using Large Language Models to summarize customer "Life-Stories" for personal bankers.

* **Expansion of Triggers:** Adding signals for "New Parent" (pediatrician/nursery spend) and "Retirement" (pension inflows).



---



## 👤 Contact & Links



* **Project Lead:** Soha Momin

* **GitHub:** [sohamomin28](https://www.google.com/search?q=https://github.com/sohamomin28)

* **LinkedIn:** [soha-momin](https://www.linkedin.com/in/soha-momin/)

* **Streamlit App:** [Live Demo](https://the-revenue-recovery-and-life-event-engine-lpkevurq2yrcpreemhh.streamlit.app/)

*  **Email Id:** msoha28@my.yorku.ca
