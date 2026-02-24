# React Frontend Documentation

## Overview
The frontend is a modern React single-page application (SPA) built with Vite for fast development and optimized builds.

## Technology Stack
- **React** 18.2 - UI library
- **React Router** 6 - Client-side routing
- **Axios** - HTTP client for API requests
- **Vite** - Build tool and dev server
- **Lucide React** - Icon library
- **Framer Motion** - Animation library (optional)

## Project Structure

```
frontend/
├── src/
│   ├── components/           # Reusable components
│   │   ├── Navbar.jsx       # Navigation bar with routing
│   │   ├── Footer.jsx       # Footer component
│   │   └── FloatingOrbs.jsx # Animated background
│   ├── pages/               # Page components
│   │   ├── Home.jsx         # Landing page
│   │   ├── TextAnalyzer.jsx # NLP text analysis
│   │   ├── JobDetection.jsx # Job ML prediction
│   │   └── InternshipDetection.jsx # Internship ML
│   ├── services/
│   │   └── api.js           # API service layer
│   ├── contexts/
│   │   └── ThemeContext.jsx # Theme management
│   ├── App.jsx              # Main app component
│   ├── App.css              # App styles
│   ├── index.css            # Global styles
│   └── main.jsx             # Entry point
├── index.html               # HTML template
├── package.json             # Dependencies
└── vite.config.js           # Vite configuration
```

## Components

### Navbar
- Responsive navigation with mobile menu
- Active route highlighting
- Theme switcher (Dark/Light/Black)
- Uses React Router for navigation

### Pages

#### Home
- Hero section with call-to-action
- Statistics display
- Feature cards
- Detection pipeline visualization
- What we detect section

#### TextAnalyzer
- Text input form with character counter
- Tab switching (Job/Internship)
- Real-time NLP analysis
- Risk score visualization
- Scam indicators list
- Recommendations based on risk level

#### JobDetection
- Form with 8 input fields
- Calls 5 ML models (XGBoost, CatBoost, Random Forest, Gradient Boost, Decision Tree)
- Ensemble voting display
- Individual model predictions
- Confidence scores

#### InternshipDetection
- Form with 10 input fields
- Calls 3 ML models (SVM, Random Forest, XGBoost)
- Ensemble results
- Warning alerts for suspicious inputs

## API Integration

The `api.js` service provides:
- `predictJob(data)` - Job prediction
- `predictInternship(data)` - Internship prediction
- `analyzeText(data)` - NLP text analysis
- `comprehensiveAnalysis(data)` - Combined analysis
- `checkHealth()` - API health check

### Example Usage
```javascript
import { analyzeText } from '../services/api'

const result = await analyzeText({
  text: "Job description here...",
  type: "job"
})
```

## Theming

The app supports three themes managed by ThemeContext:
- **Dark** (default) - Dark background with cyan/purple accents
- **Light** - White background with reduced opacity effects
- **Black** - Pure black background with enhanced contrast

Theme is persisted in localStorage.

## Styling Approach

- CSS Variables for theming
- Component-scoped CSS files
- Utility classes in index.css
- Responsive design with media queries
- Mobile-first approach

## Development

```bash
# Install dependencies
npm install

# Start dev server (http://localhost:3000)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Environment Variables

Create `.env` file in frontend directory:
```
VITE_API_URL=http://localhost:5000/api
```

## API Proxy

Vite dev server proxies `/api` requests to Flask backend (port 5000) to avoid CORS issues during development.

## Build & Deployment

### Production Build
```bash
npm run build
```
Output: `dist/` folder

### Deployment Options
1. **Static Hosting** (Netlify, Vercel, GitHub Pages)
   - Deploy `dist/` folder
   - Add redirects for SPA routing

2. **Serve with Flask**
   - Build React app
   - Move `dist/` contents to Flask `static/` folder
   - Update Flask to serve React build

## Best Practices

1. **Component Organization**
   - One component per file
   - Co-locate CSS with components
   - Use descriptive names

2. **State Management**
   - Local state for component-specific data
   - Context for shared state (theme)
   - No prop drilling

3. **API Calls**
   - All API calls in `services/api.js`
   - Error handling in components
   - Loading states for better UX

4. **Performance**
   - Lazy load routes if needed
   - Optimize images
   - Use production build for deployment

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 3000 (Windows)
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### API Connection Issues
- Ensure Flask backend is running on port 5000
- Check CORS configuration in Flask
- Verify proxy settings in vite.config.js

### Build Errors
```bash
# Clear node_modules and reinstall
rm -rf node_modules
npm install
```
