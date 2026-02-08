"""
NLP-based Text Analyzer for Fake Job and Internship Detection
Analyzes job descriptions and recruitment messages for scam indicators
"""

import re
import string
from collections import Counter
import numpy as np

class ScamTextAnalyzer:
    """Analyzes text for scam indicators using NLP techniques"""
    
    # Scam indicator keywords
    SCAM_KEYWORDS = {
        'payment_requests': [
            'registration fee', 'processing fee', 'security deposit', 'upfront payment',
            'pay now', 'payment required', 'deposit required', 'advance payment',
            'training fee', 'certification fee', 'equipment fee', 'background check fee'
        ],
        'unrealistic_promises': [
            'guaranteed income', 'get rich quick', 'easy money', 'work from home',
            'no experience required', 'unlimited earnings', 'become rich', 'millionaire',
            'passive income', 'financial freedom', 'instant cash', 'make money fast',
            'guaranteed success', 'no skills needed', 'everyone qualified'
        ],
        'urgency_tactics': [
            'urgent', 'immediate', 'act now', 'limited time', 'hurry', 'don\'t miss',
            'expires soon', 'only today', 'last chance', 'apply immediately',
            'spots filling fast', 'limited positions', 'first come first serve'
        ],
        'vague_language': [
            'great opportunity', 'amazing offer', 'fantastic deal', 'too good to miss',
            'exclusive opportunity', 'secret method', 'special program', 'revolutionary',
            'life changing', 'once in lifetime'
        ],
        'suspicious_contact': [
            'whatsapp only', 'telegram', 'personal email', 'gmail', 'yahoo',
            'text me', 'call my personal', 'contact via', 'reach me at'
        ]
    }
    
    CREDIBILITY_INDICATORS = {
        'professional': [
            'responsibilities', 'qualifications', 'requirements', 'benefits',
            'company culture', 'team', 'project', 'skills', 'experience',
            'salary range', 'work hours', 'location', 'department', 'reporting',
            'collaboration', 'development', 'growth', 'training', 'support'
        ],
        'company_info': [
            'established', 'founded', 'years in business', 'industry leader',
            'recognized', 'certified', 'ISO', 'award', 'client', 'portfolio',
            'website', 'office', 'headquarters', 'branch', 'subsidiary'
        ]
    }
    
    def __init__(self):
        self.scam_indicators = []
        self.credibility_score = 0
        self.risk_factors = []
    
    def analyze_text(self, text):
        """
        Comprehensive text analysis for scam detection
        
        Args:
            text: Job description or recruitment message
            
        Returns:
            Dictionary with analysis results
        """
        if not text or len(text.strip()) < 20:
            return {
                'risk_score': 85,
                'category': 'Suspicious',
                'scam_indicators': ['Text too short or empty'],
                'credibility_score': 15,
                'explanation': 'Job description is too brief to be genuine',
                'features': self._get_default_features()
            }
        
        text_lower = text.lower()
        
        # Reset indicators
        self.scam_indicators = []
        self.credibility_score = 0
        self.risk_factors = []
        
        # Analyze various aspects
        payment_score = self._detect_payment_requests(text_lower)
        unrealistic_score = self._detect_unrealistic_claims(text_lower)
        urgency_score = self._detect_urgency_tactics(text_lower)
        vague_score = self._detect_vague_language(text_lower)
        contact_score = self._detect_suspicious_contact(text_lower)
        credibility = self._detect_credibility_indicators(text_lower)
        
        # Text quality analysis
        quality_score = self._analyze_text_quality(text)
        grammar_score = self._analyze_grammar_capitalization(text)
        email_phone_score = self._detect_email_phone_patterns(text_lower)
        
        # Calculate overall risk score (0-100, higher = more risky)
        risk_score = (
            payment_score * 20 +
            unrealistic_score * 15 +
            urgency_score * 10 +
            vague_score * 10 +
            contact_score * 15 +
            (100 - credibility) * 0.15 +
            quality_score * 10 +
            grammar_score * 5 +
            email_phone_score * 5
        )
        
        risk_score = min(100, max(0, risk_score))
        
        # Categorize based on risk score
        if risk_score >= 70:
            category = 'Fake'
        elif risk_score >= 40:
            category = 'Suspicious'
        else:
            category = 'Genuine'
        
        # Generate explanation
        explanation = self._generate_explanation(category, risk_score)
        
        # Extract NLP features for ML models
        features = self._extract_nlp_features(text, text_lower)
        
        return {
            'risk_score': round(risk_score, 1),
            'category': category,
            'scam_indicators': self.scam_indicators,
            'credibility_score': round(credibility, 1),
            'explanation': explanation,
            'risk_factors': self.risk_factors,
            'features': features
        }
    
    def _detect_payment_requests(self, text):
        """Detect payment request language"""
        found = []
        for keyword in self.SCAM_KEYWORDS['payment_requests']:
            if keyword in text:
                found.append(keyword)
        
        if found:
            self.scam_indicators.append(f"Payment requests detected: {', '.join(found[:3])}")
            self.risk_factors.append({
                'type': 'Payment Request',
                'severity': 'HIGH',
                'description': 'Legitimate employers never ask for upfront payments'
            })
        
        return len(found) / 3  # Normalize to 0-1
    
    def _detect_unrealistic_claims(self, text):
        """Detect unrealistic promises"""
        found = []
        for keyword in self.SCAM_KEYWORDS['unrealistic_promises']:
            if keyword in text:
                found.append(keyword)
        
        if found:
            self.scam_indicators.append(f"Unrealistic promises: {', '.join(found[:2])}")
            self.risk_factors.append({
                'type': 'Unrealistic Claims',
                'severity': 'HIGH',
                'description': 'Claims sound too good to be true'
            })
        
        return min(1.0, len(found) / 2)
    
    def _detect_urgency_tactics(self, text):
        """Detect urgency and pressure tactics"""
        found = []
        for keyword in self.SCAM_KEYWORDS['urgency_tactics']:
            if keyword in text:
                found.append(keyword)
        
        if len(found) >= 2:
            self.scam_indicators.append("Excessive urgency language detected")
            self.risk_factors.append({
                'type': 'Pressure Tactics',
                'severity': 'MEDIUM',
                'description': 'Scammers use urgency to prevent careful consideration'
            })
        
        return min(1.0, len(found) / 3)
    
    def _detect_vague_language(self, text):
        """Detect vague and non-specific language"""
        found = []
        for keyword in self.SCAM_KEYWORDS['vague_language']:
            if keyword in text:
                found.append(keyword)
        
        if found:
            self.scam_indicators.append("Vague job description")
            self.risk_factors.append({
                'type': 'Vague Information',
                'severity': 'MEDIUM',
                'description': 'Lacks specific job details and responsibilities'
            })
        
        return min(1.0, len(found) / 2)
    
    def _detect_suspicious_contact(self, text):
        """Detect suspicious contact methods"""
        found = []
        for keyword in self.SCAM_KEYWORDS['suspicious_contact']:
            if keyword in text:
                found.append(keyword)
        
        if found:
            self.scam_indicators.append("Suspicious contact methods (personal email/messaging apps)")
            self.risk_factors.append({
                'type': 'Contact Method',
                'severity': 'HIGH',
                'description': 'Professional companies use official communication channels'
            })
        
        return len(found) / 2
    
    def _detect_credibility_indicators(self, text):
        """Detect professional and credibility indicators"""
        score = 0
        
        for keyword in self.CREDIBILITY_INDICATORS['professional']:
            if keyword in text:
                score += 2
        
        for keyword in self.CREDIBILITY_INDICATORS['company_info']:
            if keyword in text:
                score += 3
        
        self.credibility_score = min(100, score)
        return self.credibility_score
    
    def _analyze_text_quality(self, text):
        """Analyze text length and structure"""
        length = len(text)
        
        if length < 100:
            self.scam_indicators.append("Very short job description")
            return 0.8
        elif length < 200:
            self.scam_indicators.append("Brief job description")
            return 0.5
        elif length > 3000:
            return 0.2
        
        return 0.0
    
    def _analyze_grammar_capitalization(self, text):
        """Analyze grammar and capitalization issues"""
        # Check for excessive capitalization
        caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        
        if caps_ratio > 0.3:
            self.scam_indicators.append("Excessive capitalization")
            return 0.6
        
        # Check for multiple exclamation marks
        exclamation_count = text.count('!')
        if exclamation_count > 3:
            self.scam_indicators.append("Excessive exclamation marks")
            return 0.4
        
        return 0.0
    
    def _detect_email_phone_patterns(self, text):
        """Detect email and phone number patterns"""
        # Check for personal email domains
        personal_domains = ['gmail', 'yahoo', 'hotmail', 'outlook']
        for domain in personal_domains:
            if f'@{domain}' in text:
                self.scam_indicators.append(f"Personal email domain detected ({domain})")
                self.risk_factors.append({
                    'type': 'Email Domain',
                    'severity': 'MEDIUM',
                    'description': 'Uses personal email instead of company domain'
                })
                return 0.7
        
        return 0.0
    
    def _generate_explanation(self, category, risk_score):
        """Generate human-readable explanation"""
        if category == 'Fake':
            return (
                f"⚠️ HIGH RISK: This posting shows multiple scam indicators. "
                f"Risk score: {risk_score:.0f}/100. "
                f"Exercise extreme caution and verify independently before proceeding."
            )
        elif category == 'Suspicious':
            return (
                f"⚡ MODERATE RISK: This posting contains some concerning elements. "
                f"Risk score: {risk_score:.0f}/100. "
                f"Verify company authenticity and avoid sharing personal information."
            )
        else:
            return (
                f"✓ LOW RISK: This posting appears genuine with professional content. "
                f"Risk score: {risk_score:.0f}/100. "
                f"Standard verification recommended as best practice."
            )
    
    def _extract_nlp_features(self, text, text_lower):
        """Extract numeric features from text for ML models"""
        words = text_lower.split()
        
        return {
            'text_length': len(text),
            'word_count': len(words),
            'avg_word_length': np.mean([len(w) for w in words]) if words else 0,
            'caps_ratio': sum(1 for c in text if c.isupper()) / max(len(text), 1),
            'exclamation_count': text.count('!'),
            'question_count': text.count('?'),
            'number_count': sum(1 for c in text if c.isdigit()),
            'special_char_ratio': sum(1 for c in text if c in string.punctuation) / max(len(text), 1),
            'has_email': 1 if '@' in text else 0,
            'has_phone': 1 if bool(re.search(r'\d{3}[-.]?\d{3}[-.]?\d{4}', text)) else 0,
            'has_url': 1 if bool(re.search(r'http[s]?://', text_lower)) else 0
        }
    
    def _get_default_features(self):
        """Return default features for empty text"""
        return {
            'text_length': 0,
            'word_count': 0,
            'avg_word_length': 0,
            'caps_ratio': 0,
            'exclamation_count': 0,
            'question_count': 0,
            'number_count': 0,
            'special_char_ratio': 0,
            'has_email': 0,
            'has_phone': 0,
            'has_url': 0
        }
