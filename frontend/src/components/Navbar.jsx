import { Link, useLocation } from 'react-router-dom'
import { useState, useEffect, useRef } from 'react'
import { useTheme } from '../contexts/ThemeContext'
import { Shield, Moon, Sun, Circle } from 'lucide-react'
import './Navbar.css'

function Navbar() {
  const location = useLocation()
  const { theme, toggleTheme } = useTheme()
  const [showThemeDropdown, setShowThemeDropdown] = useState(false)
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const dropdownRef = useRef(null)

  const isActive = (path) => location.pathname === path

  const getThemeIcon = () => {
    switch (theme) {
      case 'light':
        return <Sun size={20} />
      case 'black':
        return <Circle size={20} />
      default:
        return <Moon size={20} />
    }
  }

  const getThemeLabel = () => {
    switch (theme) {
      case 'light':
        return 'Light'
      case 'black':
        return 'Black'
      default:
        return 'Dark'
    }
  }

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setShowThemeDropdown(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  return (
    <nav className="navbar">
      <div className="container">
        <Link to="/" className="nav-brand">
          <Shield size={24} />
          <span>Scam Guardian</span>
        </Link>

        <button 
          className="mobile-menu-toggle"
          onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          aria-label="Toggle menu"
        >
          <span></span>
          <span></span>
          <span></span>
        </button>

        <ul className={`nav-links ${isMobileMenuOpen ? 'active' : ''}`}>
          <li>
            <Link 
              to="/" 
              className={isActive('/') ? 'active' : ''}
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Home
            </Link>
          </li>
          <li>
            <Link 
              to="/text-analyzer" 
              className={isActive('/text-analyzer') ? 'active' : ''}
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Text Analyzer
            </Link>
          </li>
          <li>
            <Link 
              to="/job-detection" 
              className={isActive('/job-detection') ? 'active' : ''}
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Job Analysis
            </Link>
          </li>
          <li>
            <Link 
              to="/internship-detection" 
              className={isActive('/internship-detection') ? 'active' : ''}
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Internship Analysis
            </Link>
          </li>
        </ul>

        <div className="theme-toggle-container" ref={dropdownRef}>
          <button 
            className="theme-toggle"
            onClick={() => setShowThemeDropdown(!showThemeDropdown)}
          >
            <span className="theme-icon">{getThemeIcon()}</span>
            <span className="theme-text">{getThemeLabel()}</span>
          </button>
          
          {showThemeDropdown && (
            <div className="theme-dropdown">
              <button 
                className={`theme-option ${theme === 'dark' ? 'active' : ''}`}
                onClick={() => { toggleTheme('dark'); setShowThemeDropdown(false); }}
              >
                <Moon size={18} /> Dark
              </button>
              <button 
                className={`theme-option ${theme === 'light' ? 'active' : ''}`}
                onClick={() => { toggleTheme('light'); setShowThemeDropdown(false); }}
              >
                <Sun size={18} /> Light
              </button>
              <button 
                className={`theme-option ${theme === 'black' ? 'active' : ''}`}
                onClick={() => { toggleTheme('black'); setShowThemeDropdown(false); }}
              >
                <Circle size={18} /> Black
              </button>
            </div>
          )}
        </div>
      </div>
    </nav>
  )
}

export default Navbar
