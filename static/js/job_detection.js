document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('jobForm');
    if (!form) {
        console.error('Job form not found!');
        return;
    }
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        console.log('Job form submitted');
        
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
                salary_min: parseFloat(document.getElementById('salary_min').value),
                salary_max: parseFloat(document.getElementById('salary_max').value),
                company_experience_years: parseInt(document.getElementById('company_experience_years').value),
                job_description_length: parseInt(document.getElementById('job_description_length').value),
                required_experience_years: parseInt(document.getElementById('required_experience_years').value),
                required_education_level: parseInt(document.getElementById('required_education_level').value),
                telecommute_allowed: parseInt(document.getElementById('telecommute_allowed').value),
                has_company_logo: parseInt(document.getElementById('has_company_logo').value),
            };
            
            console.log('Sending job data:', formData);
            
            const response = await fetch('/api/predict-job', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('Received job data:', data);
            
            if (!data.success) throw new Error(data.error || 'Prediction failed');
            
            displayJobResults(data);
        } catch (error) {
            console.error('Job prediction error:', error);
            alert('Error: ' + error.message);
        } finally {
            loadingSpinner.classList.add('hidden');
        }
    });
});

function displayJobResults(data) {
    const results = document.getElementById('results');
    const isReal = data.ensemble_result === 'Real';
    const confidence = data.ensemble_confidence;
    
    const statusClass = isReal ? 'status-genuine' : 'status-fake';
    const statusLabel = isReal ? '✅ GENUINE JOB' : '⚠️ FRAUDULENT JOB';
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
                ? '✅ Our ensemble analysis indicates this job posting follows patterns of legitimate recruitment. The salary range, company details, and requirements appear professional and realistic.' 
                : '⚠️ Warning: Multiple models detected high-risk patterns in this job posting. The features suggest characteristics common in fraudulent recruitment. Verify company authenticity independently before proceeding.'}
        </div>

        <div style="margin: 2rem 0;">
            <h3 style="color: var(--text-primary); margin-bottom: 1.5rem; text-transform: uppercase; letter-spacing: 1px;">
                🤖 Model Predictions
            </h3>
            <div class="models-grid">
    `;

    const modelNames = {
        'xgboost': 'XGBoost',
        'catboost': 'CatBoost',
        'gradient_boost': 'Gradient Boosting',
        'random_forest': 'Random Forest',
        'decision_tree': 'Decision Tree'
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
            <h3>📋 Recommendations</h3>
            <ul class="recommendation-list">
    `;

    const recommendations = isReal ? [
        '✅ Job posting shows professional characteristics',
        '🔍 Verify company details through official website',
        '📝 Review employment contract carefully before signing',
        '🤝 Confirm communication through official channels',
        '💼 Check company reviews and employee feedback',
        '📞 Verify job posting through company HR department'
    ] : [
        '🚫 DO NOT proceed with this job opportunity',
        '🚫 DO NOT share personal or financial information',
        '⚠️ Multiple fraud indicators detected',
        '📞 Report this posting to platform administrators',
        '🔍 Search for scam reports about this company',
        '👥 Warn your network about this fraudulent posting'
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
            </div>
        `;
        modelBreakdown.appendChild(pill);
    });
    
    results.classList.remove('hidden');
    results.scrollIntoView({ behavior: 'smooth' });
}
