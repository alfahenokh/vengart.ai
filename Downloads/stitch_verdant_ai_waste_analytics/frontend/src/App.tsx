import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from './components/theme';
import Navigation from './components/layout/Navigation';
import Dashboard from './pages/Dashboard';
import Analytics from './pages/Analytics';
import Simulator from './pages/Simulator';
import Resources from './pages/Resources';

/**
 * Main Application Component
 *
 * Sets up the SPA with React Router, wraps everything in the Obsidian Moss
 * ThemeProvider, and renders the shared Navigation bar above all routes.
 */
const App: React.FC = () => {
  return (
    <ThemeProvider initialDarkMode={true}>
      <Router>
        <div className="min-h-screen bg-background flex flex-col">
          <Navigation />
          <main className="flex-1">
            <Routes>
              {/* Default route → Dashboard */}
              <Route path="/" element={<Navigate to="/dashboard" replace />} />

              {/* Module routes */}
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/analytics" element={<Analytics />} />
              <Route path="/simulator" element={<Simulator />} />
              <Route path="/resources" element={<Resources />} />

              {/* Catch-all → Dashboard */}
              <Route path="*" element={<Navigate to="/dashboard" replace />} />
            </Routes>
          </main>
        </div>
      </Router>
    </ThemeProvider>
  );
};

export default App;
