document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('internshipForm');
    if (!form) {
        console.error('Internship form not found!');
        return;
    }
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        console.log('Internship form submitted');
        
        const loadingSpinner = document.getElementById('loadingSpinner');
        const results = document.getElementById('results');
        
        if (!loadingSpinner || !results) {
            console.error('Required form elements not found!');
            return;
        }
        
        // Hide previous results
        results.classList.add('hidden');
        
        // Show loading spinner
        loadingSpinner.classList.remove('hidden');
        
        try {
            const formData = {
                company_registered: parseInt(document.getElementById('company_registered').value),
                official_email: parseInt(document.getElementById('official_email').value),
                website_available: parseInt(document.getElementById('website_available').value),
                stipend_offered: parseInt(document.getElementById('stipend_offered').value),
                stipend_amount: parseFloat(document.getElementById('stipend_amount').value),
                registration_fee: parseFloat(document.getElementById('registration_fee').value),
                interview_process: parseInt(document.getElementById('interview_process').value),
                duration_months: parseInt(document.getElementById('duration_months').value),
                job_description_quality: parseInt(document.getElementById('job_description_quality').value),
                social_media_presence: parseInt(document.getElementById('social_media_presence').value),
            };
            
            console.log('Sending internship data:', formData);
            
            const response = await fetch('/api/predict-internship', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });
            
            console.log('Response status:', response.status);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('Received internship data:', data);
            
            if (!data.success) throw new Error(data.error || 'Prediction failed');
            
            displayInternshipResults(data);
        } catch (error) {
            console.error('Internship prediction error:', error);
            alert('Error: ' + error.message);
        } finally {
            loadingSpinner.classList.add('hidden');
        }
    });
});

function displayInternshipResults(data) {
    const results = document.getElementById('results');
    const isReal = data.ensemble_result === 'Real';
    const confidence = data.ensemble_confidence;
    
    const statusClass = isReal ? 'status-genuine' : 'status-fake';
    const statusLabel = isReal ? '✅ GENUINE INTERNSHIP' : '⚠️ FRAUDULENT INTERNSHIP';
    const riskScore = isReal ? Math.max(0, 100 - confidence) : confidence;
    const riskClass = riskScore >= 70 ? 'risk-high' : riskScore >= 40 ? 'risk-medium' : 'risk-low';

    let resultsHTML = `
        <div class="result-header">
            <div class="status-badge ${statusClass}">${statusLabel}</div>
            <div class="risk-score-display" style="color: ${isReal ? 'var(--cyber-success)' : 'var(--cyber-danger)'}">
                ${confidence.toFixed(1)}%
            </div>
            <p style="margin-top: 1rem; color: var(--text-secondary); font-size: 1.1rem;">
                Ensemble Confidence
            </p>
            <div class="risk-meter" style="margin-top: 2rem;">
                <div class="risk-meter-fill ${riskClass}" style="width: ${confidence}%"></div>
            </div>
        </div>

        <div class="explanation-box">
            ${isReal 
                ? '✅ This internship offer passes our security checks. The registration fee (if any), company verification, and offer structure appear legitimate. However, always verify through the company\'s official website.' 
                : '⚠️ Warning: Multiple fraud indicators detected. This internship offer shows patterns common in scams targeting students. Be cautious of registration fees, personal email domains, or lack of company verification.'}
        </div>

        <div style="margin: 2rem 0;">
            <h3 style="color: var(--text-primary); margin-bottom: 1.5rem; text-transform: uppercase; letter-spacing: 1px;">
                🤖 Model Predictions
            </h3>
            <div class="models-grid">
    `;

    const modelNames = {
        'svm': 'SVM Classifier',
        'random_forest': 'Random Forest',
        'xgboost': 'XGBoost'
    };

    Object.entries(data.predictions).forEach(([key, val]) => {
        const name = modelNames[key] || key;
        const predClass = val.prediction === 'Real' ? 'pred-genuine' : 'pred-fraudulent';
        resultsHTML += `
            <div class="model-pill">
                <div class="model-name">${name}</div>
                <div class="model-pred ${predClass}">${val.prediction}</div>
                <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 0.5rem;">
                    ${val.confidence.toFixed(1)}% Confidence
                </div>
                <div class="percentage-bar">
                    <div class="percentage-fill" style="width: ${val.confidence}%"></div>
                </div>
            </div>
        `;
    });

    resultsHTML += `
            </div>
        </div>

        <div style="margin: 2rem 0;">
            <h3 style="color: var(--text-primary); margin-bottom: 1.5rem; text-transform: uppercase; letter-spacing: 1px;">
                📊 Vote Breakdown
            </h3>
            <div class="models-grid">
                <div class="model-pill" style="border-color: var(--cyber-danger);">
                    <div class="model-name">Fraudulent Votes</div>
                    <div class="model-pred pred-fraudulent">${data.vote_breakdown.fraudulent_votes}</div>
                </div>
                <div class="model-pill" style="border-color: var(--cyber-success);">
                    <div class="model-name">Genuine Votes</div>
                    <div class="model-pred pred-genuine">${data.vote_breakdown.real_votes}</div>
                </div>
                <div class="model-pill" style="border-color: var(--cyber-primary);">
                    <div class="model-name">Total Models</div>
                    <div class="model-pred" style="color: var(--cyber-primary)">${data.vote_breakdown.total_models}</div>
                </div>
            </div>
        </div>

        <div class="recommendations">
            <h3>📋 Safety Recommendations</h3>
            <ul class="recommendation-list">
    `;

    const recommendations = isReal ? [
        '✅ Internship offer shows legitimate characteristics',
        '🔍 Verify offer through company\'s official careers page',
        '📧 Confirm all communication via official company email',
        '📝 Review internship agreement thoroughly',
        '👥 Research company reviews and intern experiences',
        '🎓 Check if internship aligns with your academic goals',
        '⚠️ Never pay registration or training fees'
    ] : [
        '🚫 DO NOT proceed with this internship offer',
        '🚫 DO NOT make any payments or share financial details',
        '⚠️ Multiple fraud indicators detected in this offer',
        '📞 Report to your college placement cell immediately',
        '🔍 Search online for scam reports about this company',
        '👥 Warn fellow students about this fraudulent offer',
        '🎓 Seek internships through verified college programs'
    ];

    recommendations.forEach(rec => {
        resultsHTML += `<li>${rec}</li>`;
    });

    resultsHTML += `
            </ul>
        </div>
    `;

    results.innerHTML = resultsHTML;
    results.classList.remove('hidden');
    results.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}
