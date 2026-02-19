// Text Analyzer JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('textAnalyzerForm');
    const textArea = document.getElementById('jobText');
    const charCount = document.getElementById('charCount');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const results = document.getElementById('results');
    const tabButtons = document.querySelectorAll('.tab-button');
    let currentType = 'job';

    // Tab switching
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            tabButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            currentType = this.getAttribute('data-type');
        });
    });

    // Character counter
    if (textArea && charCount) {
        textArea.addEventListener('input', function() {
            charCount.textContent = this.value.length;
        });
    }

    // Form submission
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const text = textArea.value.trim();
            
            if (text.length < 50) {
                alert('Please provide at least 50 characters of text for accurate analysis.');
                return;
            }

            // Show loading
            loadingSpinner.classList.remove('hidden');
            results.classList.add('hidden');

            try {
                const response = await fetch('/api/analyze-text', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        text: text,
                        type: currentType
                    })
                });

                const data = await response.json();

                if (data.success) {
                    displayResults(data);
                } else {
                    alert('Error: ' + (data.error || 'Unknown error occurred'));
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Failed to analyze text. Please try again.');
            } finally {
                loadingSpinner.classList.add('hidden');
            }
        });
    }

    function displayResults(data) {
        const category = data.category;
        const riskScore = data.risk_score;
        const scamIndicators = data.scam_indicators || [];
        const explanation = data.explanation;
        const credibilityScore = data.credibility_score;
        const riskFactors = data.risk_factors || [];

        let statusClass = '';
        let riskClass = '';
        let statusLabel = '';

        if (category === 'Fake') {
            statusClass = 'status-fake';
            riskClass = 'risk-high';
            statusLabel = '⚠️ FAKE POSTING';
        } else if (category === 'Suspicious') {
            statusClass = 'status-suspicious';
            riskClass = 'risk-medium';
            statusLabel = '⚡ SUSPICIOUS';
        } else {
            statusClass = 'status-genuine';
            riskClass = 'risk-low';
            statusLabel = '✅ GENUINE';
        }

        let resultsHTML = `
            <div class="result-header">
                <div class="status-badge ${statusClass}">${statusLabel}</div>
                <div class="risk-score-display" style="color: ${category === 'Fake' ? 'var(--cyber-danger)' : category === 'Suspicious' ? 'var(--cyber-warning)' : 'var(--cyber-success)'}">
                    ${riskScore}/100
                </div>
                <div class="risk-meter">
                    <div class="risk-meter-fill ${riskClass}" style="width: ${riskScore}%"></div>
                </div>
                <p style="margin-top: 1.5rem; color: var(--text-secondary); font-size: 1.1rem;">
                    Credibility Score: <strong style="color: var(--cyber-primary)">${credibilityScore}/100</strong>
                </p>
            </div>

            <div class="explanation-box">
                ${explanation}
            </div>
        `;

        // Scam Indicators
        if (scamIndicators.length > 0) {
            resultsHTML += `
                <div style="margin: 2rem 0;">
                    <h3 style="color: var(--text-primary); margin-bottom: 1.5rem; text-transform: uppercase; letter-spacing: 1px;">
                        🚨 Detected Scam Indicators
                    </h3>
                    <div style="display: flex; flex-direction: column; gap: 1rem;">
            `;
            
            scamIndicators.forEach(indicator => {
                resultsHTML += `
                    <div style="background: rgba(255, 56, 100, 0.1); border-left: 3px solid var(--cyber-danger); padding: 1rem; border-radius: 8px;">
                        <span style="color: var(--text-secondary);">• ${indicator}</span>
                    </div>
                `;
            });
            
            resultsHTML += `
                    </div>
                </div>
            `;
        }

        // Risk Factors with Severity
        if (riskFactors.length > 0) {
            resultsHTML += `
                <div style="margin: 2rem 0;">
                    <h3 style="color: var(--text-primary); margin-bottom: 1.5rem; text-transform: uppercase; letter-spacing: 1px;">
                        ⚡ Risk Factors Analysis
                    </h3>
                    <div class="indicators-grid">
            `;
            
            riskFactors.forEach(factor => {
                const severityClass = `severity-${factor.severity.toLowerCase()}`;
                resultsHTML += `
                    <div class="indicator-card">
                        <div class="indicator-header">
                            <span class="severity-badge ${severityClass}">${factor.severity}</span>
                        </div>
                        <h4 style="color: var(--text-primary); margin-bottom: 0.5rem; font-size: 1.1rem;">
                            ${factor.type}
                        </h4>
                        <p style="color: var(--text-secondary);">
                            ${factor.description}
                        </p>
                    </div>
                `;
            });
            
            resultsHTML += `
                    </div>
                </div>
            `;
        }

        // Recommendations
        resultsHTML += `
            <div class="recommendations">
                <h3>📋 Recommendations</h3>
                <ul class="recommendation-list">
        `;

        const recommendations = getRecommendations(category);
        recommendations.forEach(rec => {
            resultsHTML += `<li>${rec}</li>`;
        });

        resultsHTML += `
                </ul>
            </div>
        `;

        // Feature Breakdown
        const features = data.features;
        if (features) {
            resultsHTML += `
                <div style="margin: 2rem 0;">
                    <h3 style="color: var(--text-primary); margin-bottom: 1.5rem; text-transform: uppercase; letter-spacing: 1px;">
                        📊 Text Analysis Metrics
                    </h3>
                    <div class="models-grid">
                        <div class="model-pill">
                            <div class="model-name">Text Length</div>
                            <div class="model-pred" style="color: var(--cyber-primary)">${features.text_length}</div>
                        </div>
                        <div class="model-pill">
                            <div class="model-name">Word Count</div>
                            <div class="model-pred" style="color: var(--cyber-primary)">${features.word_count}</div>
                        </div>
                        <div class="model-pill">
                            <div class="model-name">Avg Word Length</div>
                            <div class="model-pred" style="color: var(--cyber-primary)">${features.avg_word_length.toFixed(1)}</div>
                        </div>
                        <div class="model-pill">
                            <div class="model-name">Caps Ratio</div>
                            <div class="model-pred" style="color: ${features.caps_ratio > 0.3 ? 'var(--cyber-danger)' : 'var(--cyber-success)'}">
                                ${(features.caps_ratio * 100).toFixed(1)}%
                            </div>
                        </div>
                        <div class="model-pill">
                            <div class="model-name">Has Email</div>
                            <div class="model-pred pred-${features.has_email ? 'fraudulent' : 'genuine'}">
                                ${features.has_email ? 'Yes ⚠️' : 'No ✓'}
                            </div>
                        </div>
                        <div class="model-pill">
                            <div class="model-name">Has URL</div>
                            <div class="model-pred" style="color: var(--cyber-primary)">
                                ${features.has_url ? 'Yes' : 'No'}
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }

        results.innerHTML = resultsHTML;
        results.classList.remove('hidden');
        results.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function getRecommendations(category) {
        const recommendations = {
            'Fake': [
                '🚫 DO NOT proceed with this opportunity under any circumstances',
                '🚫 DO NOT share personal information, financial details, or make any payments',
                '📞 Report this posting to the platform administrators immediately',
                '🔍 Search for similar scam reports online using the company name',
                '⚠️ Block and avoid all further communication with this poster',
                '👥 Warn others in your network about this scam'
            ],
            'Suspicious': [
                '⚠️ Proceed with extreme caution and verify all information independently',
                '🔍 Thoroughly verify company registration, address, and legitimacy through official sources',
                '📧 Confirm all communication happens through verified official company channels only',
                '💳 Never make upfront payments for jobs, training, or equipment',
                '👥 Research company reviews, employee feedback, and ratings on multiple platforms',
                '🤝 Request detailed written contract and verify terms before proceeding',
                '📞 Contact the company directly through their official website contact information'
            ],
            'Genuine': [
                '✅ Posting appears legitimate with professional content and credibility indicators',
                '🔍 Still verify company details independently as standard best practice',
                '📝 Carefully review all employment terms, benefits, and responsibilities',
                '💼 Confirm role details, reporting structure, and expectations in writing',
                '🤝 Ensure all communication happens through official company channels',
                '📋 Request and review employment contract before accepting any offer'
            ]
        };
        
        return recommendations[category] || recommendations['Suspicious'];
    }
});
