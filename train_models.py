import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import os

# Create models directory
os.makedirs('models', exist_ok=True)

print("=" * 60)
print("FAKE JOB RECRUITMENT DETECTION - DATASET & MODEL TRAINING")
print("=" * 60)

# Generate synthetic job dataset
def generate_job_dataset(n_samples=1500):
    np.random.seed(123)  # Different seed for job data
    
    # More realistic feature generation
    data = {
        'salary_min': np.concatenate([
            np.random.normal(45000, 15000, int(n_samples*0.7)),  # Normal jobs
            np.random.uniform(5000, 25000, int(n_samples*0.3))   # Suspicious low salaries
        ]),
        'salary_max': [],
        'company_experience_years': np.concatenate([
            np.random.normal(12, 8, int(n_samples*0.8)),          # Established companies
            np.random.uniform(0, 3, int(n_samples*0.2))           # New/fake companies
        ]),
        'job_description_length': np.concatenate([
            np.random.normal(800, 300, int(n_samples*0.75)),      # Detailed descriptions
            np.random.uniform(50, 200, int(n_samples*0.25))       # Short/lazy descriptions
        ]),
        'required_experience_years': np.concatenate([
            np.random.poisson(3, int(n_samples*0.8)),             # Reasonable requirements  
            np.random.uniform(10, 25, int(n_samples*0.2))         # Unrealistic requirements
        ]),
        'required_education_level': np.random.choice([1,2,3,4], n_samples, p=[0.2, 0.5, 0.25, 0.05]),
        'telecommute_allowed': np.random.choice([0,1], n_samples, p=[0.6, 0.4]),
        'has_company_logo': np.random.choice([0,1], n_samples, p=[0.15, 0.85]),
    }
    
    # Generate salary_max relative to salary_min
    data['salary_max'] = []
    for min_sal in data['salary_min']:
        if min_sal < 20000:  # Suspicious jobs
            max_sal = np.random.uniform(min_sal + 5000, min_sal + 50000)
        else:  # Normal jobs
            max_sal = np.random.uniform(min_sal + 5000, min_sal + 30000)
        data['salary_max'].append(max_sal)
    
    # Ensure non-negative values and reasonable ranges
    data['salary_min'] = np.clip(data['salary_min'], 1000, 200000)
    data['salary_max'] = np.clip(data['salary_max'], 2000, 250000) 
    data['company_experience_years'] = np.clip(data['company_experience_years'], 0, 50).astype(int)
    data['job_description_length'] = np.clip(data['job_description_length'], 20, 3000).astype(int)
    data['required_experience_years'] = np.clip(data['required_experience_years'], 0, 20).astype(int)
    
    # Create features dataframe
    df = pd.DataFrame(data)
    
    # More sophisticated fraud detection rules
    fraud_score = np.zeros(len(df))
    
    # Salary red flags
    fraud_score += (df['salary_min'] < 18000).astype(int) * 2  # Very low minimum
    fraud_score += ((df['salary_max'] - df['salary_min']) > 80000).astype(int) * 2  # Unrealistic range
    fraud_score += (df['salary_max'] > 200000).astype(int) * 1  # Suspiciously high
    
    # Company credibility
    fraud_score += ((df['company_experience_years'] < 2) & (df['has_company_logo'] == 0)).astype(int) * 3
    fraud_score += (df['company_experience_years'] == 0).astype(int) * 2
    
    # Job description quality
    fraud_score += (df['job_description_length'] < 150).astype(int) * 2
    fraud_score += (df['job_description_length'] > 2500).astype(int) * 1
    
    # Experience requirements
    fraud_score += (df['required_experience_years'] > 15).astype(int) * 2
    fraud_score += ((df['required_experience_years'] > 10) & (df['salary_min'] < 30000)).astype(int) * 2
    
    # Education vs salary mismatch
    fraud_score += ((df['required_education_level'] >= 3) & (df['salary_min'] < 25000)).astype(int) * 1
    
    # Convert fraud score to label (threshold-based with noise)
    df['label'] = (fraud_score >= 3).astype(int)
    
    # Add realistic noise (15% chance of flipping)
    noise_indices = np.random.choice(df.index, size=int(0.15 * len(df)), replace=False)
    df.loc[noise_indices, 'label'] = 1 - df.loc[noise_indices, 'label']
    
    return df

# Generate synthetic internship dataset
def generate_internship_dataset(n_samples=1500):
    np.random.seed(456)  # Different seed for internship data
    
    # More realistic feature generation
    data = {
        'company_registered': np.random.choice([0,1], n_samples, p=[0.1, 0.9]),  # Most companies registered
        'official_email': np.random.choice([0,1], n_samples, p=[0.2, 0.8]),  # Most have official emails
        'website_available': np.random.choice([0,1], n_samples, p=[0.15, 0.85]),  # Most have websites
        'stipend_offered': np.random.choice([0,1], n_samples, p=[0.3, 0.7]),  # Many offer stipends
        'stipend_amount': [],
        'registration_fee': [],
        'interview_process': np.random.choice([0,1], n_samples, p=[0.25, 0.75]),  # Most have interviews
        'duration_months': np.random.choice([1,2,3,4,6,8,12], n_samples, p=[0.1,0.15,0.25,0.2,0.2,0.05,0.05]),
        'job_description_quality': np.random.choice([1,2,3,4,5], n_samples, p=[0.05,0.1,0.3,0.4,0.15]),
        'social_media_presence': np.random.choice([0,1,2], n_samples, p=[0.2, 0.5, 0.3]),  # Fixed field name
    }
    
    # Generate stipend amounts based on whether stipend is offered
    stipend_offers = data['stipend_offered']
    for offer in stipend_offers:
        if offer == 1:  # Stipend offered
            amount = np.random.normal(8000, 3000)  # Normal internship stipends
            if np.random.random() < 0.1:  # 10% chance of suspicious high stipend
                amount = np.random.uniform(25000, 100000)  
        else:
            amount = 0
        data['stipend_amount'].append(max(0, amount))
    
    # Generate registration fees (most legitimate internships = $0)
    for i in range(n_samples):
        if np.random.random() < 0.8:  # 80% no fee (legitimate)
            fee = 0
        elif np.random.random() < 0.9:  # Small processing fee
            fee = np.random.uniform(50, 500) 
        else:  # Suspicious high fees
            fee = np.random.uniform(1000, 10000)
        data['registration_fee'].append(fee)
    
    df = pd.DataFrame(data)
    
    # Sophisticated fraud scoring
    fraud_score = np.zeros(len(df))
    
    # Company legitimacy indicators 
    fraud_score += (df['company_registered'] == 0).astype(int) * 4  # Major red flag
    fraud_score += (df['official_email'] == 0).astype(int) * 3
    fraud_score += (df['website_available'] == 0).astype(int) * 2
    fraud_score += (df['social_media_presence'] == 0).astype(int) * 1
    
    # Financial red flags
    fraud_score += (df['registration_fee'] > 2000).astype(int) * 4  # High reg fee = major red flag
    fraud_score += ((df['registration_fee'] > 500) & (df['registration_fee'] <= 2000)).astype(int) * 2  
    fraud_score += (df['stipend_amount'] > 20000).astype(int) * 3  # Unrealistic stipend
    fraud_score += ((df['stipend_offered'] == 0) & (df['registration_fee'] > 0)).astype(int) * 2  # No pay but fees
    
    # Process quality indicators
    fraud_score += (df['interview_process'] == 0).astype(int) * 1
    fraud_score += (df['job_description_quality'] <= 2).astype(int) * 2
    fraud_score += (df['duration_months'] > 10).astype(int) * 1  # Unusually long
    
    # Convert to labels
    df['label'] = (fraud_score >= 4).astype(int)  # Threshold for fraud
    
    # Add realistic noise
    noise_indices = np.random.choice(df.index, size=int(0.12 * len(df)), replace=False)
    df.loc[noise_indices, 'label'] = 1 - df.loc[noise_indices, 'label']
    
    return df

# Train job detection models
print("\nGenerating Job Dataset...")
job_df = generate_job_dataset(n_samples=3000)  # Increased sample size
print(f"Job Dataset shape: {job_df.shape}")
print(f"Fraudulent jobs: {(job_df['label'] == 1).sum()} ({((job_df['label'] == 1).sum() / len(job_df) * 100):.1f}%)")
print(f"Real jobs: {(job_df['label'] == 0).sum()} ({((job_df['label'] == 0).sum() / len(job_df) * 100):.1f}%)")

# Save dataset
job_df.to_csv('jobs_dataset.csv', index=False)
print("Job dataset saved to 'jobs_dataset.csv'")

X_job = job_df.drop('label', axis=1)
y_job = job_df['label']

X_train_job, X_test_job, y_train_job, y_test_job = train_test_split(
    X_job, y_job, test_size=0.2, random_state=42
)

scaler_job = StandardScaler()
X_train_job_scaled = scaler_job.fit_transform(X_train_job)
X_test_job_scaled = scaler_job.transform(X_test_job)

# Job Models
print("\n" + "-" * 60)
print("Training Job Detection Models...")
print("-" * 60)

job_models = {}

# XGBoost
print("\nTraining XGBoost...")
xgb_job = XGBClassifier(n_estimators=100, random_state=42, eval_metric='logloss')
xgb_job.fit(X_train_job_scaled, y_train_job)
job_models['xgboost'] = xgb_job
y_pred = xgb_job.predict(X_test_job_scaled)
print(f"XGBoost Accuracy: {accuracy_score(y_test_job, y_pred):.4f}")

# CatBoost
print("\nTraining CatBoost...")
catb_job = CatBoostClassifier(iterations=100, random_state=42, verbose=False)
catb_job.fit(X_train_job_scaled, y_train_job)
job_models['catboost'] = catb_job
y_pred = catb_job.predict(X_test_job_scaled)
print(f"CatBoost Accuracy: {accuracy_score(y_test_job, y_pred):.4f}")

# Gradient Boost
print("\nTraining Gradient Boosting...")
gb_job = GradientBoostingClassifier(n_estimators=100, random_state=42)
gb_job.fit(X_train_job_scaled, y_train_job)
job_models['gradient_boost'] = gb_job
y_pred = gb_job.predict(X_test_job_scaled)
print(f"Gradient Boosting Accuracy: {accuracy_score(y_test_job, y_pred):.4f}")

# Random Forest
print("\nTraining Random Forest...")
rf_job = RandomForestClassifier(n_estimators=100, random_state=42)
rf_job.fit(X_train_job_scaled, y_train_job)
job_models['random_forest'] = rf_job
y_pred = rf_job.predict(X_test_job_scaled)
print(f"Random Forest Accuracy: {accuracy_score(y_test_job, y_pred):.4f}")

# Decision Tree
print("\nTraining Decision Tree...")
dt_job = DecisionTreeClassifier(random_state=42)
dt_job.fit(X_train_job_scaled, y_train_job)
job_models['decision_tree'] = dt_job
y_pred = dt_job.predict(X_test_job_scaled)
print(f"Decision Tree Accuracy: {accuracy_score(y_test_job, y_pred):.4f}")

# Save job models
joblib.dump(xgb_job, 'models/job_xgboost.pkl')
joblib.dump(catb_job, 'models/job_catboost.pkl')
joblib.dump(gb_job, 'models/job_gradient_boost.pkl')
joblib.dump(rf_job, 'models/job_random_forest.pkl')
joblib.dump(dt_job, 'models/job_decision_tree.pkl')
joblib.dump(scaler_job, 'models/job_scaler.pkl')

print("\n✓ Job models saved to 'models/' directory")

# Train internship detection models
print("\n" + "=" * 60)
print("FAKE INTERNSHIP DETECTION - DATASET & MODEL TRAINING")
print("=" * 60)

print("\nGenerating Internship Dataset...")
internship_df = generate_internship_dataset(n_samples=3000)  # Increased sample size
print(f"Internship Dataset shape: {internship_df.shape}")
print(f"Fraudulent internships: {(internship_df['label'] == 1).sum()} ({((internship_df['label'] == 1).sum() / len(internship_df) * 100):.1f}%)")
print(f"Real internships: {(internship_df['label'] == 0).sum()} ({((internship_df['label'] == 0).sum() / len(internship_df) * 100):.1f}%)")

# Save dataset
internship_df.to_csv('internships_dataset.csv', index=False)
print("Internship dataset saved to 'internships_dataset.csv'")

X_internship = internship_df.drop('label', axis=1)
y_internship = internship_df['label']

X_train_int, X_test_int, y_train_int, y_test_int = train_test_split(
    X_internship, y_internship, test_size=0.2, random_state=42
)

scaler_int = StandardScaler()
X_train_int_scaled = scaler_int.fit_transform(X_train_int)
X_test_int_scaled = scaler_int.transform(X_test_int)

# Internship Models
print("\n" + "-" * 60)
print("Training Internship Detection Models...")
print("-" * 60)

internship_models = {}

# SVM
print("\nTraining SVM...")
svm_int = SVC(kernel='rbf', random_state=42, probability=True)
svm_int.fit(X_train_int_scaled, y_train_int)
internship_models['svm'] = svm_int
y_pred = svm_int.predict(X_test_int_scaled)
print(f"SVM Accuracy: {accuracy_score(y_test_int, y_pred):.4f}")

# Random Forest
print("\nTraining Random Forest...")
rf_int = RandomForestClassifier(n_estimators=100, random_state=42)
rf_int.fit(X_train_int_scaled, y_train_int)
internship_models['random_forest'] = rf_int
y_pred = rf_int.predict(X_test_int_scaled)
print(f"Random Forest Accuracy: {accuracy_score(y_test_int, y_pred):.4f}")

# XGBoost
print("\nTraining XGBoost...")
xgb_int = XGBClassifier(n_estimators=100, random_state=42, eval_metric='logloss')
xgb_int.fit(X_train_int_scaled, y_train_int)
internship_models['xgboost'] = xgb_int
y_pred = xgb_int.predict(X_test_int_scaled)
print(f"XGBoost Accuracy: {accuracy_score(y_test_int, y_pred):.4f}")

# Save internship models
joblib.dump(svm_int, 'models/internship_svm.pkl')
joblib.dump(rf_int, 'models/internship_random_forest.pkl')
joblib.dump(xgb_int, 'models/internship_xgboost.pkl')
joblib.dump(scaler_int, 'models/internship_scaler.pkl')

print("\n✓ Internship models saved to 'models/' directory")

print("\n" + "=" * 60)
print("TRAINING COMPLETE!")
print("=" * 60)
print("\nGenerated Files:")
print("  - jobs_dataset.csv")
print("  - internships_dataset.csv")
print("  - models/")
print("    ├── job_xgboost.pkl")
print("    ├── job_catboost.pkl")
print("    ├── job_gradient_boost.pkl")
print("    ├── job_random_forest.pkl")
print("    ├── job_decision_tree.pkl")
print("    ├── job_scaler.pkl")
print("    ├── internship_svm.pkl")
print("    ├── internship_random_forest.pkl")
print("    ├── internship_xgboost.pkl")
print("    └── internship_scaler.pkl")
