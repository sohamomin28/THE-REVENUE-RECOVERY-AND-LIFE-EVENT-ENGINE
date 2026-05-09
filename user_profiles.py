from faker import Faker
import numpy as np
import pandas as pd
import random

fake = Faker('en_CA')
Faker.seed(20)
random.seed(20)
np.random.seed(20) # to ensure I have the same random numbers each time I run the code

NUMBER_OF_USERS = 1000
real_cities = [
    "Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa", 
    "Edmonton", "Winnipeg", "Quebec City", "Halifax", 
    "Saskatoon", "Mississauga", "Brampton", "Hamilton", "Victoria"
]


def generate_user_profiles(num_users):
    """ Creates a foundation of user profiles with realistic data. """
    user_profiles = []
    for i in range(num_users):
        age = int(np.random.normal(loc=35, scale=25))  # Average age around 35 with some variation
        age = np.clip(age, 18, 70)  # Ensure age is between 18 and 70'
        salary = np.random.lognormal(mean=11, sigma=0.5)  # Log-normal distribution for salary
        salary = round(salary, 2)  # Round salary to 2 decimal places
        loyalty_base = np.random.uniform(0.1, 0.8)  # Loyalty score between 0.1 and 0.8
        age_bonus = (age/100) * 0.2  
        loyalty_score = round(min(1.0, loyalty_base + age_bonus), 2)  # Final loyalty score capped at 1.0
        user_profile = {
            'user_id': i,  
            'name': fake.name(),
            'age': age,
            'annual_income': salary,
            'city': random.choice(real_cities),
            'loyalty_score': loyalty_score,
            'is_student': 1 if age < 25 and random.random() < 0.4 else 0,  # Higher chance of being a student if under 25
           }
        user_profiles.append(user_profile)
    return pd.DataFrame(user_profiles)

#2. Execution 
if __name__ == "__main__":
    print("Generating foundational user profiles...")
    
    df = generate_user_profiles(num_users=1000)

    # 3. Save the Foundation
    df.to_csv('user_profiles.csv', index=False)
    
    # 4. Verification (The "Sanity Check")
    print("\n--- Process Complete ---")
    print(f"File Saved: user_profiles.csv ({len(df)} rows)")
    print("\nSample Data:")
    print(df.head())
    print("\nStatistical Summary:")
    print(df[['age', 'annual_income', 'loyalty_score']].describe())
    