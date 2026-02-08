from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import os
import json
from nlp_analyzer import ScamTextAnalyzer

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize NLP analyzer
nlp_analyzer = ScamTextAnalyzer()

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

@app.route('/text-analyzer')
def text_analyzer():
    return render_template('text_analyzer.html')

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
        
        print(f"Internship predictions: {predictions}")
        
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
        
        result = {
            'success': True,
            'predictions': predictions,
            'ensemble_result': ensemble_prediction,
            'ensemble_confidence': round(ensemble_confidence, 1),
            'vote_breakdown': {
                'fraudulent_votes': fraudulent_votes,
                'real_votes': vote_count - fraudulent_votes,
                'total_models': vote_count
            }
        }
        
        print(f"Returning internship result: {result}")
        return jsonify(result)
    
    except Exception as e:
        print(f"ERROR in internship prediction: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/analyze-text', methods=['POST'])
def analyze_text():
    """Analyze job/internship text for scam indicators using NLP"""
    try:
        data = request.json
        text = data.get('text', '')
        analysis_type = data.get('type', 'job')  # 'job' or 'internship'
        
        if not text:
            return jsonify({
                'success': False,
                'error': 'No text provided'
            }), 400
        
        # Analyze text using NLP
        analysis_result = nlp_analyzer.analyze_text(text)
        
        # Add analysis type
        analysis_result['analysis_type'] = analysis_type
        analysis_result['success'] = True
        
        return jsonify(analysis_result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/comprehensive-analysis', methods=['POST'])
def comprehensive_analysis():
    """
    Comprehensive analysis combining NLP text analysis and ML model predictions
    """
    try:
        data = request.json
        text = data.get('text', '')
        analysis_type = data.get('type', 'job')
        
        if not text:
            return jsonify({
                'success': False,
                'error': 'No text provided'
            }), 400
        
        # Step 1: NLP Text Analysis
        text_analysis = nlp_analyzer.analyze_text(text)
        
        # Step 2: Extract features from text analysis
        nlp_features = text_analysis['features']
        
        # Step 3: Combine with form data if provided
        features_dict = data.get('features', {})
        
        # Calculate final risk score
        nlp_risk = text_analysis['risk_score']
        
        # If ML features are provided, combine with NLP analysis
        ml_predictions = None
        ensemble_risk = nlp_risk
        
        if features_dict and analysis_type == 'job':
            # Get ML model predictions for jobs
            try:
                features = np.array([[
                    features_dict.get('salary_min', 0),
                    features_dict.get('salary_max', 0),
                    features_dict.get('company_experience_years', 0),
                    features_dict.get('job_description_length', len(text)),
                    features_dict.get('required_experience_years', 0),
                    features_dict.get('required_education_level', 2),
                    features_dict.get('telecommute_allowed', 0),
                    features_dict.get('has_company_logo', 1)
                ]])
                
                if 'job_scaler' in models:
                    features = models['job_scaler'].transform(features)
                    
                    ml_predictions = {}
                    fraud_votes = 0
                    total_models = 0
                    
                    for model_name in ['job_xgboost', 'job_catboost', 'job_random_forest']:
                        if model_name in models:
                            pred = models[model_name].predict(features)[0]
                            prob = models[model_name].predict_proba(features)[0]
                            ml_predictions[model_name.replace('job_', '')] = {
                                'prediction': 'Fraudulent' if pred == 1 else 'Genuine',
                                'confidence': float(max(prob) * 100)
                            }
                            if pred == 1:
                                fraud_votes += 1
                            total_models += 1
                    
                    # Calculate ML risk score
                    ml_risk = (fraud_votes / total_models) * 100 if total_models > 0 else 50
                    
                    # Combine NLP and ML risk (weighted average)
                    ensemble_risk = (nlp_risk * 0.6) + (ml_risk * 0.4)
            except Exception as ml_error:
                print(f"ML prediction error: {ml_error}")
        
        # Determine final category based on ensemble risk
        if ensemble_risk >= 70:
            final_category = 'Fake'
            alert_level = 'danger'
        elif ensemble_risk >= 40:
            final_category = 'Suspicious'
            alert_level = 'warning'
        else:
            final_category = 'Genuine'
            alert_level = 'success'
        
        return jsonify({
            'success': True,
            'nlp_analysis': text_analysis,
            'ml_predictions': ml_predictions,
            'ensemble_risk_score': round(ensemble_risk, 1),
            'final_category': final_category,
            'alert_level': alert_level,
            'recommendation': _generate_recommendation(final_category, ensemble_risk)
        })
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/health', methods=['GET'])
def _generate_recommendation(category, risk_score):
    """Generate actionable recommendations based on analysis"""
    recommendations = {
        'Fake': [
            '🚫 DO NOT proceed with this opportunity',
            '🚫 DO NOT share personal information or make any payments',
            '📞 Report this posting to the platform administrators',
            '🔍 Search for similar scam reports online',
            '⚠️ Block and avoid all communication with this poster'
        ],
        'Suspicious': [
            '⚠️ Proceed with extreme caution',
            '🔍 Verify company registration and legitimacy independently',
            '📧 Confirm communication through official company channels',
            '💳 Never make upfront payments',
            '👥 Research company reviews and employee feedback online',
            '🤝 Request detailed written contract before proceeding'
        ],
        'Genuine': [
            '✅ Posting appears legitimate',
            '🔍 Still verify company details as standard practice',
            '📝 Review employment terms carefully',
            '💼 Confirm role and responsibilities in writing',
            '🤝 Professional communication through official channels only'
        ]
    }
    
    return recommendations.get(category, [])

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'models_loaded': len(models) > 0,
        'nlp_analyzer': 'active'
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
