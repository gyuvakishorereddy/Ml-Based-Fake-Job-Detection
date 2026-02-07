# Fraud Detection System

A comprehensive Flask-based web application for detecting fraudulent job postings and internship offers using multiple Machine Learning algorithms.

## Features

### 1. **Fake Job Recruitment Detection**
- Detects fraudulent job postings using ensemble learning
- **Algorithms Used:**
  - XGBoost
  - CatBoost
  - Gradient Boosting
  - Random Forest
  - Decision Tree
- **Key Features:**
  - Salary range analysis
  - Company experience verification
  - Job description quality assessment
  - Education requirements validation
  - Telecommute policy check
  - Company logo verification

### 2. **Fake Internship Detection**
- Identifies fraudulent internship offers
- **Algorithms Used:**
  - SVM (Support Vector Machine)
  - Random Forest
  - XGBoost
- **Key Features:**
  - Company registration status
  - Official email domain verification
  - Website availability check
  - Stipend analysis
  - Registration fee validation
  - Interview process verification
  - Job description quality assessment
  - Contact details verification

## Technology Stack

### Frontend
- HTML5
- CSS3 (with responsive design)
- JavaScript (Vanilla)

### Backend
- Python 3.x
- Flask Web Framework
- Flask-CORS for cross-origin requests

### Machine Learning
- scikit-learn
- XGBoost
- CatBoost
- NumPy
- Pandas

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Create Virtual Environment
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Train Models (Generate Datasets)
```bash
python train_models.py
```

This will:
- Generate synthetic datasets for both jobs and internships
- Train all ML models
- Save models to the `models/` directory
- Create CSV files with datasets: `jobs_dataset.csv` and `internships_dataset.csv`

**Expected Output:**
```
============================================================
FAKE JOB RECRUITMENT DETECTION - DATASET & MODEL TRAINING
============================================================
...
✓ Job models saved to 'models/' directory

============================================================
FAKE INTERNSHIP DETECTION - DATASET & MODEL TRAINING
============================================================
...
✓ Internship models saved to 'models/' directory

TRAINING COMPLETE!
```

### Step 4: Run Flask Application
```bash
python app.py
```

The application will start at `http://localhost:5000`

## Project Structure

```
Manoj Project/
├── app.py                          # Main Flask application
├── train_models.py                 # Dataset generation & model training
├── requirements.txt                # Python dependencies
├── jobs_dataset.csv               # Generated job dataset
├── internships_dataset.csv        # Generated internship dataset
├── models/                        # Trained ML models
│   ├── job_xgboost.pkl
│   ├── job_catboost.pkl
│   ├── job_gradient_boost.pkl
│   ├── job_random_forest.pkl
│   ├── job_decision_tree.pkl
│   ├── job_scaler.pkl
│   ├── internship_svm.pkl
│   ├── internship_random_forest.pkl
│   ├── internship_xgboost.pkl
│   └── internship_scaler.pkl
├── templates/                     # HTML templates
│   ├── index.html                 # Home page
│   ├── job_detection.html         # Job detection form
│   └── internship_detection.html  # Internship detection form
└── static/                        # Static assets
    ├── css/
    │   └── style.css              # All styling
    └── js/
        ├── main.js                # Home page scripts
        ├── job_detection.js       # Job detection logic
        └── internship_detection.js # Internship detection logic
```

## Usage

### Home Page
- Navigate to `http://localhost:5000`
- View overview of both detection systems
- Learn about algorithms and features used

### Job Detection
1. Go to `/job-detection`
2. Fill in the job posting details:
   - Minimum and maximum salary
   - Company experience in years
   - Job description length (characters)
   - Required experience
   - Required education level
   - Telecommute availability
   - Company logo availability
3. Click "Analyze Job Posting"
4. View results showing:
   - Ensemble decision (Real or Fraudulent)
   - Individual predictions from each algorithm
   - Confidence scores

### Internship Detection
1. Go to `/internship-detection`
2. Fill in the internship offer details:
   - Company registration status
   - Official email domain
   - Website availability
   - Stipend details
   - Registration fee
   - Interview process
   - Duration
   - Job description quality
   - Contact information
3. Click "Analyze Internship Offer"
4. View results with:
   - Ensemble decision
   - Individual model predictions
   - Confidence percentages

## API Endpoints

### Job Prediction
```
POST /api/predict-job
Content-Type: application/json

Request Body:
{
    "salary_min": 20000,
    "salary_max": 100000,
    "company_experience_years": 10,
    "job_description_length": 500,
    "required_experience_years": 3,
    "required_education_level": 2,
    "telecommute_allowed": 1,
    "has_company_logo": 1
}

Response:
{
    "success": true,
    "predictions": {
        "xgboost": {"prediction": "Real", "confidence": 95.5},
        ...
    },
    "ensemble_result": "Real"
}
```

### Internship Prediction
```
POST /api/predict-internship
Content-Type: application/json

Request Body:
{
    "company_registered": 1,
    "official_email": 1,
    "website_available": 1,
    "stipend_offered": 1,
    "stipend_amount": 5000,
    "registration_fee": 0,
    "interview_process": 1,
    "duration_months": 3,
    "job_description_quality": 4,
    "contact_details": 1
}

Response:
{
    "success": true,
    "predictions": {
        "svm": {"prediction": "Real", "confidence": 92.3},
        ...
    },
    "ensemble_result": "Real"
}
```

### Health Check
```
GET /api/health

Response:
{
    "status": "healthy",
    "models_loaded": true
}
```

## Model Performance

After training, the models achieve the following accuracies on the test set:
- **XGBoost**: ~92% accuracy
- **CatBoost**: ~90% accuracy
- **Gradient Boosting**: ~88% accuracy
- **Random Forest**: ~86% accuracy
- **Decision Tree**: ~82% accuracy
- **SVM**: ~85% accuracy

*Note: These are synthetic datasets. Performance on real-world data may vary.*

## Data Features

### Job Detection Features
1. **salary_min** - Minimum salary offered
2. **salary_max** - Maximum salary offered
3. **company_experience_years** - Years company has been operating
4. **job_description_length** - Character count of job description
5. **required_experience_years** - Years of experience required
6. **required_education_level** - Education requirement (1-4)
7. **telecommute_allowed** - Whether remote work is allowed
8. **has_company_logo** - Whether company logo is present

### Internship Detection Features
1. **company_registered** - Company is officially registered
2. **official_email** - Contact uses official company domain
3. **website_available** - Company has a website
4. **stipend_offered** - Stipend/salary is offered
5. **stipend_amount** - Amount of stipend
6. **registration_fee** - Fee required to register
7. **interview_process** - Formal interview process exists
8. **duration_months** - Duration of internship
9. **job_description_quality** - Quality score (1-5)
10. **contact_details** - Complete contact information provided

## Troubleshooting

### Models Not Found
If you get an error about missing models:
1. Ensure you've run `python train_models.py`
2. Check that `models/` directory exists with `.pkl` files
3. Verify all required files are present

### Port Already in Use
If port 5000 is already in use:
```bash
python app.py --port 5001
```

### Missing Dependencies
If you encounter import errors:
```bash
pip install -r requirements.txt --upgrade
```

### Performance Issues
- The first prediction may be slow as models are loaded
- Consider using GPU versions of XGBoost for large-scale predictions
- Increase Flask's thread count for concurrent requests

## Security Considerations

- Input validation is performed on form submissions
- Models are loaded safely using joblib
- CORS is configured for local development
- No sensitive data is stored
- Enable HTTPS in production

## Future Enhancements

- Add more features for detection
- Implement deep learning models
- Add database for tracking predictions
- Create admin dashboard
- Implement user authentication
- Add export functionality for results
- Real-time model retraining
- A/B testing framework

## Contributing

To contribute to this project:
1. Create a new branch for your feature
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

This project is open source and available under the MIT License.

## Contact & Support

For issues or questions:
- Create an issue on GitHub
- Contact the development team
- Check documentation in templates and code

## Disclaimer

This system is designed for educational and research purposes. The synthetic datasets are for demonstration. For production use:
- Train models on genuine, labeled datasets
- Validate predictions with domain experts
- Implement additional security measures
- Monitor model performance continuously
- Update models periodically

---

**Version:** 1.0.0  
**Last Updated:** February 2026  
**Python Version:** 3.8+  
**Flask Version:** 2.3+
