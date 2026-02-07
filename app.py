from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import os
import json

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Load models
def load_models():
    models = {}
    model_dir = 'models'
    
    if os.path.exists(model_dir):
        # Job Detection Models
        job_models = ['job_xgboost', 'job_catboost', 'job_gradient_boost', 'job_random_forest', 'job_decision_tree']
        for model in job_models:
            model_path = os.path.join(model_dir, f'{model}.pkl')
            if os.path.exists(model_path):
                models[model] = joblib.load(model_path)
        
        # Internship Detection Models
        internship_models = ['internship_svm', 'internship_random_forest', 'internship_xgboost']
        for model in internship_models:
            model_path = os.path.join(model_dir, f'{model}.pkl')
            if os.path.exists(model_path):
                models[model] = joblib.load(model_path)
        
        # Load scalers
        if os.path.exists(os.path.join(model_dir, 'job_scaler.pkl')):
            models['job_scaler'] = joblib.load(os.path.join(model_dir, 'job_scaler.pkl'))
        if os.path.exists(os.path.join(model_dir, 'internship_scaler.pkl')):
            models['internship_scaler'] = joblib.load(os.path.join(model_dir, 'internship_scaler.pkl'))
    
    return models

models = load_models()

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/job-detection')
def job_detection():
    return render_template('job_detection.html')

@app.route('/internship-detection')
def internship_detection():
    return render_template('internship_detection.html')

@app.route('/api/predict-job', methods=['POST'])
def predict_job():
    """Predict if job is real or fraudulent"""
    try:
        data = request.json
        
        # Extract features in the same order as training
        features = np.array([[
            data.get('salary_min', 0),
            data.get('salary_max', 0),
            data.get('company_experience_years', 0),
            data.get('job_description_length', 0),
            data.get('required_experience_years', 0),
            data.get('required_education_level', 0),
            data.get('telecommute_allowed', 0),
            data.get('has_company_logo', 0)
        ]])
        
        # Apply feature scaling using the trained scaler
        if 'job_scaler' in models:
            features = models['job_scaler'].transform(features)
        else:
            return jsonify({
                'success': False,
                'error': 'Job scaler not found. Please retrain models.'
            }), 400
        
        predictions = {}
        
        # XGBoost prediction
        if 'job_xgboost' in models:
            pred = models['job_xgboost'].predict(features)[0]
            prob = models['job_xgboost'].predict_proba(features)[0]
            predictions['xgboost'] = {
                'prediction': 'Fraudulent' if pred == 1 else 'Real',
                'confidence': float(max(prob) * 100)
            }
        
        # CatBoost prediction
        if 'job_catboost' in models:
            pred = models['job_catboost'].predict(features)[0]
            prob = models['job_catboost'].predict_proba(features)[0]
            predictions['catboost'] = {
                'prediction': 'Fraudulent' if pred == 1 else 'Real', 
                'confidence': float(max(prob) * 100)
            }
        
        # Gradient Boost prediction
        if 'job_gradient_boost' in models:
            pred = models['job_gradient_boost'].predict(features)[0]
            prob = models['job_gradient_boost'].predict_proba(features)[0]
            predictions['gradient_boost'] = {
                'prediction': 'Fraudulent' if pred == 1 else 'Real',
                'confidence': float(max(prob) * 100)
            }
        
        # Random Forest prediction
        if 'job_random_forest' in models:
            pred = models['job_random_forest'].predict(features)[0]
            prob = models['job_random_forest'].predict_proba(features)[0]
            predictions['random_forest'] = {
                'prediction': 'Fraudulent' if pred == 1 else 'Real',
                'confidence': float(max(prob) * 100)
            }
        
        # Decision Tree prediction
        if 'job_decision_tree' in models:
            pred = models['job_decision_tree'].predict(features)[0]
            prob = models['job_decision_tree'].predict_proba(features)[0]
            predictions['decision_tree'] = {
                'prediction': 'Fraudulent' if pred == 1 else 'Real',
                'confidence': float(max(prob) * 100)
            }
        
        # Ensemble decision (majority vote with confidence tracking)
        fraudulent_votes = 0
        total_confidence = 0
        vote_count = 0
        
        for model_pred in predictions.values():
            vote_count += 1
            if model_pred['prediction'] == 'Fraudulent':
                fraudulent_votes += 1
            total_confidence += model_pred['confidence']
        
        # Determine ensemble result
        if vote_count > 0:
            ensemble_prediction = 'Fraudulent' if fraudulent_votes > vote_count / 2 else 'Real'
            ensemble_confidence = total_confidence / vote_count
        else:
            ensemble_prediction = 'Real'
            ensemble_confidence = 50.0
        
        return jsonify({
            'success': True,
            'predictions': predictions,
            'ensemble_result': ensemble_prediction,
            'ensemble_confidence': round(ensemble_confidence, 1),
            'vote_breakdown': {
                'fraudulent_votes': fraudulent_votes,
                'real_votes': vote_count - fraudulent_votes,
                'total_models': vote_count
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/predict-internship', methods=['POST'])
def predict_internship():
    """Predict if internship is real or fraudulent"""
    try:
        print("\n=== INTERNSHIP PREDICTION REQUEST ===")
        data = request.json
        print(f"Received data: {data}")
        
        if not data:
            print("ERROR: No JSON data received")
            return jsonify({
                'success': False,
                'error': 'No data received'
            }), 400
        
        # Extract features in the same order as training
        features = np.array([[
            data.get('company_registered', 0),
            data.get('official_email', 0),
            data.get('website_available', 0),
            data.get('stipend_offered', 0),
            data.get('stipend_amount', 0),
            data.get('registration_fee', 0),
            data.get('interview_process', 0),
            data.get('duration_months', 0),
            data.get('job_description_quality', 0),
            data.get('social_media_presence', 0)
        ]])
        
        print(f"Features before scaling: {features}")
        
        # Apply feature scaling using the trained scaler
        if 'internship_scaler' in models:
            features = models['internship_scaler'].transform(features)
            print(f"Features after scaling: {features}")
        else:
            print("ERROR: Internship scaler not found")
            return jsonify({
                'success': False,
                'error': 'Internship scaler not found. Please retrain models.'
            }), 400
        
        predictions = {}
        
        # SVM prediction
        if 'internship_svm' in models:
            pred = models['internship_svm'].predict(features)[0]
            try:
                # For SVM, use predict_proba if available
                prob = models['internship_svm'].predict_proba(features)[0]
                confidence = float(max(prob) * 100)
            except:
                # Fallback to decision function
                decision = abs(models['internship_svm'].decision_function(features)[0])
                confidence = float(min(100, max(50, decision * 20)))
            
            predictions['svm'] = {
                'prediction': 'Fraudulent' if pred == 1 else 'Real',
                'confidence': confidence
            }
        
        # Random Forest prediction
        if 'internship_random_forest' in models:
            pred = models['internship_random_forest'].predict(features)[0]
            prob = models['internship_random_forest'].predict_proba(features)[0]
            predictions['random_forest'] = {
                'prediction': 'Fraudulent' if pred == 1 else 'Real',
                'confidence': float(max(prob) * 100)
            }
        
        # XGBoost prediction
        if 'internship_xgboost' in models:
            pred = models['internship_xgboost'].predict(features)[0]
            prob = models['internship_xgboost'].predict_proba(features)[0]
            predictions['xgboost'] = {
                'prediction': 'Fraudulent' if pred == 1 else 'Real',
                'confidence': float(max(prob) * 100)
            }
        
        # Ensemble decision (majority vote with confidence tracking)
        fraudulent_votes = 0
        total_confidence = 0
        vote_count = 0
        
        for model_pred in predictions.values():
            vote_count += 1
            if model_pred['prediction'] == 'Fraudulent':
                fraudulent_votes += 1
            total_confidence += model_pred['confidence']
        
        # Determine ensemble result
        if vote_count > 0:
            ensemble_prediction = 'Fraudulent' if fraudulent_votes > vote_count / 2 else 'Real'
            ensemble_confidence = total_confidence / vote_count
        else:
            ensemble_prediction = 'Real'
            ensemble_confidence = 50.0
        
        return jsonify({
            'success': True,
            'predictions': predictions,
            'ensemble_result': ensemble_prediction,
            'ensemble_confidence': round(ensemble_confidence, 1),
            'vote_breakdown': {
                'fraudulent_votes': fraudulent_votes,
                'real_votes': vote_count - fraudulent_votes,
                'total_models': vote_count
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'models_loaded': len(models) > 0
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    os.makedirs('models', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
