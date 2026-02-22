# 🛡️ AI-Based Fake Job & Internship Scam Detection System

## Cybersecurity Domain | Machine Learning | NLP | React + Flask

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/React-18.2+-61DAFB.svg)](https://reactjs.org/)
[![ML](https://img.shields.io/badge/ML-Ensemble-orange.svg)](https://scikit-learn.org/)
[![NLP](https://img.shields.io/badge/NLP-Powered-purple.svg)](https://www.nltk.org/)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup (Flask API)

```bash
# 1. Navigate to project root
cd "Manoj Project"

# 2. Create and activate virtual environment (Optional but recommended)
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Train ML models (one-time setup)
python train_models.py

# 5. Start Flask API server
python app.py
# API will run at: http://localhost:5000/api
```

### Frontend Setup (React)

```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install Node dependencies
npm install

# 3. Start React development server
npm run dev
# App will run at: http://localhost:3000
```

### Access the Application
Open your browser and navigate to: **http://localhost:3000**

---

## ✨ Key Features

🔍 **NLP Text Analysis** - Paste job descriptions for instant scam detection  
🤖 **8 ML Models** - Ensemble learning with XGBoost, CatBoost, Random Forest, SVM  
📊 **Risk Scoring** - 0-100 risk scores with 3-tier categorization (Genuine/Suspicious/Fake)  
💡 **Explainable AI** - Detailed scam indicators and explanations  
🎨 **Modern React UI** - Dynamic SPA with theme switching (Dark/Light/Black)  
📱 **Responsive Design** - Works seamlessly on all devices  
⚡ **Real-time Analysis** - Instant predictions with API integration

---

## 🏗️ Architecture

### Frontend (React)
- **Framework:** React 18 with Vite
- **Routing:** React Router v6
- **HTTP Client:** Axios
- **UI Components:** Custom components with Lucide icons
- **Styling:** CSS3 with CSS variables for theming
- **State Management:** React Context API

### Backend (Flask API)
- **Framework:** Flask 2.3+
- **API:** RESTful JSON API
- **CORS:** Flask-CORS for cross-origin requests
- **ML Models:** Scikit-learn, XGBoost, CatBoost
- **NLP:** NLTK, custom text analyzer

### Project Structure
```
Manoj Project/
├── app.py                      # Flask API server
├── nlp_analyzer.py            # NLP text analysis engine
├── train_models.py            # ML model training script
├── config.py                  # Configuration
├── requirements.txt           # Python dependencies
├── models/                    # Trained ML models
├── frontend/                  # React application
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   │   ├── Navbar.jsx
│   │   │   ├── Footer.jsx
│   │   │   └── FloatingOrbs.jsx
│   │   ├── pages/           # Page components
│   │   │   ├── Home.jsx
│   │   │   ├── TextAnalyzer.jsx
│   │   │   ├── JobDetection.jsx
│   │   │   └── InternshipDetection.jsx
│   │   ├── services/        # API service layer
│   │   │   └── api.js
│   │   ├── contexts/        # React contexts
│   │   │   └── ThemeContext.jsx
│   │   ├── App.jsx          # Main app component
│   │   └── main.jsx         # Entry point
│   ├── package.json
│   └── vite.config.js
└── datasets/
    ├── jobs_dataset.csv
    └── internships_dataset.csv
```

---

## 📁 Project Structure

```
├── app.py                          # Flask application
├── nlp_analyzer.py                 # NLP text analysis engine
├── train_models.py                 # Model training
├── requirements.txt                # Dependencies
├── models/                         # Trained ML models
├── templates/
│   ├── index.html                 # Home page
│   ├── text_analyzer.html         # Text analysis page
│   ├── job_detection.html         # Job analysis
│   └── internship_detection.html  # Internship analysis
└── static/
    ├── css/cyber_style.css        # Cybersecurity theme
    └── js/                        # JavaScript files
```

---

## 🔌 API Endpoints

- `POST /api/analyze-text` - NLP text analysis
- `POST /api/predict-job` - Job feature prediction
- `POST /api/predict-internship` - Internship prediction
- `GET /api/health` - Health check

---

## 🎓 Educational Value

Perfect for:
- **Students** learning ML/NLP
- **Placement cells** verifying offers
- **Job seekers** protecting themselves
- **Researchers** studying fraud detection
- **Educators** teaching cybersecurity

---

## 🛡️ Safety Recommendations

### For Fake Postings:
- 🚫 DO NOT proceed
- 🚫 DO NOT share personal information
- 📞 Report immediately

### For Suspicious Postings:
- ⚠️ Proceed with caution
- 🔍 Verify independently
- 💳 Never pay upfront fees

---

## 📚 Documentation

- **Full Documentation:** `PROJECT_DOCUMENTATION.md`
- **Upgrade Summary:** `UPGRADE_SUMMARY.md`
- **Quick Start:** This file

---

## 👥 Target Audience

🎓 Students  
💼 Job seekers  
🏫 Placement cells  
🏢 HR departments  
🔒 Cybersecurity enthusiasts  

---

## 🤝 Contributing

Contributions welcome! Improve:
- ML models and accuracy
- NLP features
- UI/UX design
- Documentation
- Test coverage

---

## 📝 Keywords

Fake Job Detection, Internship Scam Prevention, Machine Learning Models, Cyber Fraud Analytics, Online Safety Platform, Text Classification System, Web-Based Application, AI-Powered Scam Monitoring, Digital Trust & Security

---

## ⚡ System Requirements

- Python 3.8+
- 4GB RAM minimum
- Modern web browser
- Internet connection (for installation)

---

## 🚨 Disclaimer

This system is designed for educational and awareness purposes. Always verify job offers through multiple sources and official company channels.

---

## 🌟 Features Highlight

✅ **NLP-Powered** - Advanced text analysis  
✅ **Multi-Model Ensemble** - 8 ML models  
✅ **Real-Time Detection** - Instant results  
✅ **Explainable AI** - Clear explanations  
✅ **Risk Categorization** - 3-tier system  
✅ **Cybersecurity UI** - Professional design  
✅ **Mobile Responsive** - Works everywhere  
✅ **No Registration** - Use immediately  

---

**Built with ❤️ for digital safety and fraud prevention**

**Version 2.0** | **Domain: Cybersecurity** | **2026**
