import React from 'react';
import { useTranslation } from 'react-i18next';
import { Sprout, Globe, UserCheck, UserX } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { Link } from 'react-router-dom';

export default function Navbar() {
  const { t, i18n } = useTranslation();
  const { user, isGuest } = useAuth();

  const handleLanguageChange = (e) => {
    const newLang = e.target.value;
    i18n.changeLanguage(newLang);
    localStorage.setItem('smart_kisan_lang', newLang);
  };

  return (
    <header className="page-header">
      {/* Logo + Brand */}
      <Link
        to="/"
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '10px',
          textDecoration: 'none',
        }}
      >
        <div className="navbar-logo-wrap">
          <Sprout size={20} color="#86EFAC" />
        </div>
        <div>
          <div
            className="gradient-text"
            style={{
              fontFamily: 'var(--font-heading)',
              fontSize: '1.25rem',
              fontWeight: 800,
              lineHeight: 1.1,
              letterSpacing: '-0.02em',
            }}
          >
            Smart Kisan
          </div>
          <div
            style={{
              fontSize: '0.6rem',
              color: 'var(--text-muted)',
              letterSpacing: '0.08em',
              textTransform: 'uppercase',
              fontFamily: 'var(--font-heading)',
              fontWeight: 600,
            }}
          >
            {t('tagline')}
          </div>
        </div>
      </Link>

      {/* Controls */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        {/* Language selector */}
        <div style={{ position: 'relative', display: 'flex', alignItems: 'center' }}>
          <Globe
            size={13}
            style={{
              position: 'absolute',
              left: '8px',
              color: 'var(--primary-light)',
              pointerEvents: 'none',
              zIndex: 1,
            }}
          />
          <select
            value={i18n.language}
            onChange={handleLanguageChange}
            aria-label="Language selection"
            style={{
              padding: '6px 10px 6px 26px',
              borderRadius: '20px',
              border: '1px solid var(--border-default)',
              background: 'var(--bg-card-elevated)',
              color: 'var(--text-primary)',
              fontSize: '0.72rem',
              fontWeight: 700,
              fontFamily: 'var(--font-heading)',
              cursor: 'pointer',
              outline: 'none',
              appearance: 'none',
              WebkitAppearance: 'none',
              transition: 'border-color var(--transition-fast)',
            }}
          >
            <option value="en">English</option>
            <option value="hi">हिंदी</option>
            <option value="mr">मराठी</option>
          </select>
        </div>

        {/* Profile / Status pill */}
        <Link
          to="/profile"
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '5px',
            padding: '6px 11px',
            borderRadius: '20px',
            background: isGuest
              ? 'rgba(245, 158, 11, 0.12)'
              : 'rgba(34, 197, 94, 0.12)',
            border: `1px solid ${isGuest ? 'rgba(245,158,11,0.3)' : 'rgba(34,197,94,0.3)'}`,
            color: isGuest ? 'var(--secondary)' : 'var(--success)',
            fontSize: '0.72rem',
            fontWeight: 700,
            fontFamily: 'var(--font-heading)',
            textDecoration: 'none',
            transition: 'all var(--transition-fast)',
            letterSpacing: '0.02em',
          }}
        >
          {isGuest ? <UserX size={12} /> : <UserCheck size={12} />}
          <span>
            {isGuest ? 'Guest' : user?.full_name?.split(' ')[0] || 'Farmer'}
          </span>
        </Link>
      </div>
    </header>
  );
}
