import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import './i18n';

import { AuthProvider } from './context/AuthContext';
import Sidebar from './components/Sidebar';
import TopHeader from './components/TopHeader';
import BottomNav from './components/BottomNav';
import SplashScreen from './components/SplashScreen';

import Home from './pages/Home';
import DiseaseDetector from './pages/DiseaseDetector';
import CropAdvisor from './pages/CropAdvisor';
import MarketPrices from './pages/MarketPrices';
import Schemes from './pages/Schemes';
import Chat from './pages/Chat';
import Profile from './pages/Profile';

export default function App() {
  const [showSplash, setShowSplash] = useState(true);
  const [splashFading, setSplashFading] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const fadeTimer = setTimeout(() => {
      setSplashFading(true);
    }, 1400);

    const hideTimer = setTimeout(() => {
      setShowSplash(false);
    }, 1900);

    return () => {
      clearTimeout(fadeTimer);
      clearTimeout(hideTimer);
    };
  }, []);

  return (
    <AuthProvider>
      <BrowserRouter>
        {showSplash && <SplashScreen isFading={splashFading} />}
        
        <div className={`app-layout ${mobileMenuOpen ? 'mobile-menu-active' : ''}`}>
          {/* Left Sidebar */}
          <div className="sidebar-container">
            <Sidebar />
          </div>

          {/* Backdrop for mobile drawer */}
          {mobileMenuOpen && (
            <div
              className="sidebar-backdrop"
              onClick={() => setMobileMenuOpen(false)}
            />
          )}

          {/* Main Dashboard Canvas */}
          <div className="main-canvas">
            <TopHeader onToggleMobileMenu={() => setMobileMenuOpen(!mobileMenuOpen)} />
            
            <main className="content-container">
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/disease" element={<DiseaseDetector />} />
                <Route path="/crop" element={<CropAdvisor />} />
                <Route path="/market" element={<MarketPrices />} />
                <Route path="/schemes" element={<Schemes />} />
                <Route path="/chat" element={<Chat />} />
                <Route path="/profile" element={<Profile />} />
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </main>
          </div>

          {/* Mobile Bottom Navigation */}
          <BottomNav />
        </div>

        <Toaster
          position="top-center"
          toastOptions={{
            duration: 3500,
            style: {
              background: '#14532d',
              color: '#ffffff',
              borderRadius: '12px',
              fontSize: '0.875rem',
              boxShadow: '0 4px 20px rgba(0, 0, 0, 0.15)',
            },
          }}
        />
      </BrowserRouter>
    </AuthProvider>
  );
}
