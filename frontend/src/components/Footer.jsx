import './Footer.css'

function Footer() {
  return (
    <footer className="footer">
      <div className="container">
        <p>&copy; 2024 AI Scam Detection System. Protecting you from recruitment fraud.</p>
        <p className="footer-tech">
          Built with React + Flask | ML Models: XGBoost, CatBoost, Random Forest, SVM
        </p>
      </div>
    </footer>
  )
}

export default Footer
