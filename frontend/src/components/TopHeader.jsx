import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { Bell, ChevronDown, Globe, LogOut, User, Sprout } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function TopHeader({ onToggleMobileMenu }) {
  const { t, i18n } = useTranslation();
  const { user, isGuest, logout } = useAuth();
  const navigate = useNavigate();
  const [dropdownOpen, setDropdownOpen] = useState(false);

  const handleLanguageChange = (lang) => {
    i18n.changeLanguage(lang);
    localStorage.setItem('smart_kisan_lang', lang);
  };

  return (
    <header className="top-header">
      {/* Mobile Brand Mark (Left side of header on mobile only) */}
      <Link to="/" className="top-header-mobile-brand">
        <div className="mobile-brand-icon">
          <Sprout size={18} color="#15803d" />
        </div>
        <span className="mobile-brand-name">Smart Kisan</span>
      </Link>

      {/* Header Actions (Right side) */}
      <div className="top-header-actions">
        {/* Language selector (compact) */}
        <div className="header-lang-selector">
          <Globe size={13} color="#15803d" />
          <select
            value={i18n.language}
            onChange={(e) => handleLanguageChange(e.target.value)}
            aria-label="Language selection"
            className="header-lang-select"
          >
            <option value="en">English</option>
            <option value="hi">हिंदी</option>
            <option value="mr">मराठी</option>
          </select>
        </div>

        {/* Notification Bell with Badge 3 */}
        <Link to="/schemes" className="header-notification-btn" title="Alerts & Schemes">
          <Bell size={18} color="#374151" />
          <span className="notification-badge">3</span>
        </Link>

        {/* User Profile Pill & Dropdown */}
        <div className="header-user-wrapper">
          <button
            className="header-user-btn"
            onClick={() => setDropdownOpen(!dropdownOpen)}
            aria-expanded={dropdownOpen}
          >
            <img
              src="/assets/farmer-avatar.jpg"
              alt="Farmer avatar"
              className="header-avatar-img"
            />
            <span className="header-user-name desktop-only-text">
              {isGuest ? 'Farmer' : user?.full_name?.split(' ')[0] || 'Farmer'}
            </span>
            <ChevronDown size={13} color="#4b5563" className="desktop-only-text" />
          </button>

          {dropdownOpen && (
            <div className="header-dropdown-menu">
              <Link
                to="/profile"
                className="header-dropdown-item"
                onClick={() => setDropdownOpen(false)}
              >
                <User size={15} />
                <span>Farmer Profile</span>
              </Link>
              <div className="header-dropdown-divider" />
              {isGuest ? (
                <Link
                  to="/profile"
                  className="header-dropdown-item"
                  onClick={() => setDropdownOpen(false)}
                >
                  <User size={15} />
                  <span>Log In / Sign Up</span>
                </Link>
              ) : (
                <button
                  className="header-dropdown-item text-danger"
                  onClick={() => {
                    setDropdownOpen(false);
                    logout();
                    navigate('/');
                  }}
                >
                  <LogOut size={15} />
                  <span>Sign Out</span>
                </button>
              )}
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
