import { Link } from 'react-router-dom'
import { Search, BarChart, GraduationCap, Zap, Target, FileText } from 'lucide-react'
import './Home.css'

function Home() {
  return (
    <div className="home-page">
      <div className="container">
        {/* Hero Section */}
        <section className="hero">
          <span className="badge badge-primary">🔒 AI-Powered Protection</span>
          <h1>Fake Job & Internship Scam Detection</h1>
          <p className="subtitle">
            Protect yourself from recruitment fraud with AI and NLP
          </p>
          <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', marginTop: '2rem', flexWrap: 'wrap' }}>
            <Link to="/text-analyzer" className="btn btn-primary">
              <Search size={20} /> Analyze Text
            </Link>
            <Link to="/job-detection" className="btn btn-outline">
              <BarChart size={20} /> Job Analysis
            </Link>
          </div>
        </section>

        {/* Stats Section */}
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-value primary">98.5%</div>
            <div className="stat-label">Accuracy</div>
          </div>
          <div className="stat-card">
            <div className="stat-value secondary">8</div>
            <div className="stat-label">ML Models</div>
          </div>
          <div className="stat-card">
            <div className="stat-value success">Real-time</div>
            <div className="stat-label">Analysis</div>
          </div>
          <div className="stat-card">
            <div className="stat-value warning">68+</div>
            <div className="stat-label">Indicators</div>
          </div>
        </div>

        {/* Features Section */}
        <section className="features-section">
          <h2 className="section-title">Key Features</h2>
          <div className="grid grid-3">
            <div className="card">
              <div className="card-icon"><Search size={48} /></div>
              <h3>Text Analysis</h3>
              <p>NLP-powered analysis detecting payment requests, unrealistic claims, and suspicious patterns</p>
              <Link to="/text-analyzer" className="btn btn-primary mt-2">Launch</Link>
            </div>

            <div className="card">
              <div className="card-icon"><BarChart size={48} /></div>
              <h3>Job Verification</h3>
              <p>Multi-model ensemble with XGBoost, CatBoost, and Random Forest</p>
              <Link to="/job-detection" className="btn btn-secondary mt-2">Verify</Link>
            </div>

            <div className="card">
              <div className="card-icon"><GraduationCap size={48} /></div>
              <h3>Internship Guard</h3>
              <p>Specialized scam detection protecting students from predatory practices</p>
              <Link to="/internship-detection" className="btn btn-secondary mt-2">Check</Link>
            </div>

            <div className="card">
              <div className="card-icon"><Zap size={48} /></div>
              <h3>Scam Indicators</h3>
              <p>Detects payment requests, vague language, personal emails, and red flags</p>
            </div>

            <div className="card">
              <div className="card-icon"><Target size={48} /></div>
              <h3>Risk Scoring</h3>
              <p>Classification into Genuine, Suspicious, or Fake with 0-100 scores</p>
            </div>

            <div className="card">
              <div className="card-icon"><FileText size={48} /></div>
              <h3>Explainable AI</h3>
              <p>Clear explanations with actionable safety recommendations</p>
            </div>
          </div>
        </section>

        {/* Detection Pipeline */}
        <section className="features-section">
          <h2 className="section-title">Detection Pipeline</h2>
          <div className="grid grid-3">
            <div className="card pipeline-step">
              <h3>1️⃣ Input</h3>
              <p>Paste job text or enter details</p>
            </div>
            <div className="card pipeline-step">
              <h3>2️⃣ NLP Scan</h3>
              <p>Analyzes keywords and patterns</p>
            </div>
            <div className="card pipeline-step">
              <h3>3️⃣ ML Models</h3>
              <p>8 models vote on prediction</p>
            </div>
            <div className="card pipeline-step">
              <h3>4️⃣ Risk Score</h3>
              <p>Combines NLP and ML results</p>
            </div>
            <div className="card pipeline-step">
              <h3>5️⃣ Report</h3>
              <p>Detailed findings & indicators</p>
            </div>
            <div className="card pipeline-step">
              <h3>6️⃣ Decision</h3>
              <p>Make informed choices</p>
            </div>
          </div>
        </section>

        {/* What We Detect */}
        <section className="features-section">
          <h2 className="section-title">What We Detect</h2>
          <div className="grid grid-2">
            <div className="card">
              <h3>💳 Payment Requests</h3>
              <p>Registration fees, deposits, upfront payments</p>
            </div>
            <div className="card">
              <h3>🎯 Unrealistic Promises</h3>
              <p>Guaranteed income, get-rich-quick schemes</p>
            </div>
            <div className="card">
              <h3>⚡ Urgency Tactics</h3>
              <p>Limited time offers, pressure techniques</p>
            </div>
            <div className="card">
              <h3>📧 Suspicious Contacts</h3>
              <p>Personal emails, WhatsApp-only communication</p>
            </div>
            <div className="card">
              <h3>📝 Vague Descriptions</h3>
              <p>Lack of specific job details</p>
            </div>
            <div className="card">
              <h3>🏢 Company Credibility</h3>
              <p>Missing verification, poor online presence</p>
            </div>
          </div>
        </section>
      </div>
    </div>
  )
}

export default Home
