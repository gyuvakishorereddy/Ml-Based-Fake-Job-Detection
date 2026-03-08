import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { ThemeProvider } from './contexts/ThemeContext'
import Navbar from './components/Navbar'
import Footer from './components/Footer'
import FloatingOrbs from './components/FloatingOrbs'
import Home from './pages/Home'
import TextAnalyzer from './pages/TextAnalyzer'
import JobDetection from './pages/JobDetection'
import InternshipDetection from './pages/InternshipDetection'
import './App.css'

function App() {
  return (
    <ThemeProvider>
      <Router>
        <div className="App">
          <FloatingOrbs />
          <Navbar />
          <main className="main-content">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/text-analyzer" element={<TextAnalyzer />} />
              <Route path="/job-detection" element={<JobDetection />} />
              <Route path="/internship-detection" element={<InternshipDetection />} />
            </Routes>
          </main>
          <Footer />
        </div>
      </Router>
    </ThemeProvider>
  )
}

export default App
