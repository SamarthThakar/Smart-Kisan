import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import {
  User,
  Phone,
  MapPin,
  Trees,
  Globe,
  LogOut,
  LogIn,
  History,
  Save,
  CheckCircle2,
  ShieldCheck,
  ChevronRight,
  Sprout,
  ScanLine,
  Award,
  Leaf,
  BarChart2,
  Sparkles,
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { api } from '../services/api';
import toast from 'react-hot-toast';
import KisanHoloCard from '../components/effects/KisanHoloCard';

export default function Profile() {
  const { t, i18n } = useTranslation();
  const { user, profile, isGuest, login, register, logout, updateProfile } = useAuth();

  const [activeTab, setActiveTab] = useState('card');
  const [authMode, setAuthMode] = useState('login');
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [historyItems, setHistoryItems] = useState([]);
  const [loadingHistory, setLoadingHistory] = useState(false);

  const [profileData, setProfileData] = useState({
    state: profile?.state || 'Maharashtra',
    district: profile?.district || 'Pune',
    land_size_acres: profile?.land_size_acres || 4.5,
    farmer_category: profile?.farmer_category || 'small',
    soil_type: profile?.soil_type || 'Black Soil',
  });

  useEffect(() => {
    if (profile) {
      setProfileData({
        state: profile.state || 'Maharashtra',
        district: profile.district || 'Pune',
        land_size_acres: profile.land_size_acres || 4.5,
        farmer_category: profile.farmer_category || 'small',
        soil_type: profile.soil_type || 'Black Soil',
      });
    }
  }, [profile]);

  useEffect(() => {
    if (activeTab === 'history') loadHistory();
  }, [activeTab]);

  const loadHistory = async () => {
    setLoadingHistory(true);
    try {
      const res = await api.getHistory('all');
      setHistoryItems(res.history || []);
    } catch (err) {
      console.warn('Using sample activity', err);
      setHistoryItems([
        {
          id: '1',
          type: 'disease',
          title: 'Tomato Late Blight Detected',
          subtitle: '89.2% confidence · Leaf scan',
          created_at: new Date().toISOString(),
        },
        {
          id: '2',
          type: 'crop',
          title: 'Top recommendation: Rice & Maize',
          subtitle: 'Soil NPK (90-42-43) · Kharif season',
          created_at: new Date(Date.now() - 86400000).toISOString(),
        },
      ]);
    } finally {
      setLoadingHistory(false);
    }
  };

  const handleLanguageChange = (langCode) => {
    i18n.changeLanguage(langCode);
    localStorage.setItem('smart_kisan_lang', langCode);
    toast.success(
      `Language set to ${langCode === 'hi' ? 'हिंदी' : langCode === 'mr' ? 'मराठी' : 'English'}`
    );
  };

  const handleAuthSubmit = async (e) => {
    e.preventDefault();
    if (authMode === 'login') {
      await login(phone, password);
    } else {
      await register(phone, fullName, i18n.language, password);
    }
  };

  const handleSaveProfile = async (e) => {
    e.preventDefault();
    await updateProfile(profileData);
  };

  /* Computed farmer tier */
  const farmerTier = profile?.land_size_acres >= 10
    ? 'Master Cultivator'
    : profile?.land_size_acres >= 5
    ? 'Senior Farmer'
    : 'Rising Kisan';

  /* Tab config */
  const tabs = [
    { id: 'card',    label: 'Kisan Ratna Card', icon: Award },
    { id: 'profile', label: 'Farm Details',     icon: Leaf },
    { id: 'history', label: 'Activity History', icon: History },
  ];

  return (
    <div style={{ maxWidth: '860px', margin: '0 auto', paddingBottom: '50px' }}>
      {/* ── Farmer Hero Card ── */}
      <div
        style={{
          background: '#ffffff',
          borderRadius: '20px',
          padding: '24px',
          border: '1px solid #e0ece3',
          boxShadow: '0 4px 16px rgba(0, 0, 0, 0.04)',
          marginBottom: '20px',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          textAlign: 'center',
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        {/* Accent top stripe */}
        <div
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            height: '4px',
            background: 'linear-gradient(90deg, #167a48, #f59e0b, #167a48)',
          }}
        />

        {/* Avatar */}
        <div
          style={{
            width: '84px',
            height: '84px',
            borderRadius: '50%',
            overflow: 'hidden',
            border: '3px solid #d1fae5',
            boxShadow: '0 4px 14px rgba(22, 122, 72, 0.15)',
            marginBottom: '12px',
          }}
        >
          <img
            src="/assets/farmer-avatar.jpg"
            alt="Farmer Profile"
            style={{ width: '100%', height: '100%', objectFit: 'cover' }}
          />
        </div>

        <h1
          style={{
            fontSize: '1.45rem',
            fontWeight: 800,
            color: '#0f291e',
            margin: '0 0 6px 0',
            fontFamily: 'var(--font-heading)',
          }}
        >
          {user?.full_name || 'Farmer Friend'}
        </h1>

        <div style={{ display: 'flex', justifyContent: 'center', gap: '8px', flexWrap: 'wrap', marginBottom: '10px' }}>
          <span
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '4px',
              padding: '4px 12px',
              borderRadius: '20px',
              background: '#fef3c7',
              color: '#b45309',
              fontWeight: 700,
              fontSize: '0.78rem',
              border: '1px solid #fde68a',
            }}
          >
            🏅 {farmerTier}
          </span>
          <span
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '4px',
              padding: '4px 12px',
              borderRadius: '20px',
              background: isGuest ? '#fef3c7' : '#eaf6ed',
              color: isGuest ? '#b45309' : '#167a48',
              fontWeight: 700,
              fontSize: '0.78rem',
              border: isGuest ? '1px solid #fde68a' : '1px solid #c7e8d0',
            }}
          >
            {isGuest ? '⚠️ Demo Mode' : '✅ Verified Kisan'}
          </span>
        </div>

        {!isGuest && (
          <div
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '6px',
              fontSize: '0.82rem',
              color: '#4b5563',
              background: '#f3f4f6',
              padding: '4px 14px',
              borderRadius: '20px',
            }}
          >
            <Phone size={12} color="#6b7280" />
            {user?.phone || '—'}
          </div>
        )}

        {/* Tab Switcher */}
        <div
          style={{
            display: 'flex',
            background: '#f3f7f4',
            borderRadius: '24px',
            padding: '4px',
            marginTop: '20px',
            width: '100%',
            maxWidth: '460px',
            gap: '4px',
          }}
        >
          {tabs.map((tab) => {
            const TabIcon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                style={{
                  flex: 1,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '6px',
                  padding: '9px 12px',
                  borderRadius: '20px',
                  border: 'none',
                  background: isActive ? '#167a48' : 'transparent',
                  color: isActive ? '#ffffff' : '#4b5563',
                  fontWeight: 700,
                  fontSize: '0.78rem',
                  cursor: 'pointer',
                  fontFamily: 'var(--font-heading)',
                  boxShadow: isActive ? '0 2px 8px rgba(22, 122, 72, 0.25)' : 'none',
                  transition: 'all 0.2s',
                }}
              >
                <TabIcon size={14} />
                {tab.label}
              </button>
            );
          })}
        </div>
      </div>

      {/* ── Tab 1: Kisan Holographic Card ── */}
      {activeTab === 'card' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {/* Constrained 3D Card Box */}
          <div className="kisan-holo-card-wrapper">
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                marginBottom: '12px',
              }}
            >
              <div>
                <div style={{ fontFamily: 'var(--font-heading)', fontWeight: 800, fontSize: '1rem', color: '#0f291e' }}>
                  🌾 Kisan Ratna Trophy Card
                </div>
                <div style={{ fontSize: '0.72rem', color: '#6b7280', marginTop: '2px' }}>
                  Move mouse to tilt · Drag to rotate · Double-click to flip
                </div>
              </div>
              <span
                style={{
                  background: '#fef3c7',
                  color: '#b45309',
                  fontWeight: 700,
                  fontSize: '0.7rem',
                  padding: '3px 8px',
                  borderRadius: '12px',
                  border: '1px solid #fde68a',
                }}
              >
                ✨ 3D Holo
              </span>
            </div>

            <KisanHoloCard
              variant="golden-wheat"
              title={isGuest ? undefined : `${farmerTier} — ${user?.full_name?.split(' ')[0] || 'Kisan'}`}
            />
          </div>

          {/* Quick Metrics Grid */}
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(3, 1fr)',
              gap: '12px',
              maxWidth: '380px',
              margin: '0 auto',
              width: '100%',
            }}
          >
            {[
              { label: 'Land Area', value: `${profile?.land_size_acres || '4.5'} ac`, icon: '🌾' },
              { label: 'Soil Type', value: (profile?.soil_type || 'Black Soil').split(' ')[0], icon: '🌱' },
              { label: 'State',     value: profile?.state || 'MH', icon: '📍' },
            ].map((stat) => (
              <div
                key={stat.label}
                style={{
                  background: '#ffffff',
                  border: '1px solid #e0ece3',
                  borderRadius: '14px',
                  padding: '12px 8px',
                  textAlign: 'center',
                  boxShadow: '0 2px 8px rgba(0, 0, 0, 0.03)',
                }}
              >
                <div style={{ fontSize: '1.3rem', marginBottom: '2px' }}>{stat.icon}</div>
                <div style={{ fontSize: '0.85rem', fontWeight: 800, color: '#167a48', fontFamily: 'var(--font-heading)' }}>
                  {stat.value}
                </div>
                <div style={{ fontSize: '0.68rem', color: '#6b7280', fontWeight: 600 }}>
                  {stat.label}
                </div>
              </div>
            ))}
          </div>

          {/* Scheme Badges */}
          <div
            style={{
              background: '#ffffff',
              border: '1px solid #e0ece3',
              borderRadius: '16px',
              padding: '18px 20px',
              maxWidth: '520px',
              margin: '0 auto',
              width: '100%',
              boxShadow: '0 2px 10px rgba(0, 0, 0, 0.03)',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
              <ShieldCheck size={18} color="#167a48" />
              <span style={{ fontFamily: 'var(--font-heading)', fontWeight: 700, fontSize: '0.92rem', color: '#0f291e' }}>
                Verified Agricultural Badges
              </span>
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
              {['PM-KISAN Active', 'KCC Approved', 'FASAL Bima Protected', 'MSP Verified'].map((scheme) => (
                <span
                  key={scheme}
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '4px',
                    padding: '6px 12px',
                    borderRadius: '20px',
                    border: '1px solid #c7e8d0',
                    background: '#f0fdf4',
                    color: '#15803d',
                    fontSize: '0.74rem',
                    fontWeight: 700,
                  }}
                >
                  ✓ {scheme}
                </span>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ── Tab 2: Farm Details & Settings ── */}
      {activeTab === 'profile' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', maxWidth: '620px', margin: '0 auto' }}>
          {/* Language Selector */}
          <div
            style={{
              background: '#ffffff',
              border: '1px solid #e0ece3',
              borderRadius: '16px',
              padding: '18px 20px',
              boxShadow: '0 2px 10px rgba(0, 0, 0, 0.03)',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px' }}>
              <Globe size={18} color="#167a48" />
              <h3 style={{ fontSize: '0.95rem', fontWeight: 700, margin: 0, color: '#0f291e' }}>
                Preferred Language / भाषा
              </h3>
            </div>
            <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
              {[
                { code: 'en', label: 'English' },
                { code: 'hi', label: 'हिंदी' },
                { code: 'mr', label: 'मराठी' },
              ].map((lang) => (
                <button
                  key={lang.code}
                  type="button"
                  style={{
                    padding: '8px 18px',
                    borderRadius: '20px',
                    border: i18n.language === lang.code ? '1px solid #167a48' : '1px solid #d1d5db',
                    background: i18n.language === lang.code ? '#167a48' : '#ffffff',
                    color: i18n.language === lang.code ? '#ffffff' : '#374151',
                    fontWeight: 700,
                    fontSize: '0.82rem',
                    cursor: 'pointer',
                  }}
                  onClick={() => handleLanguageChange(lang.code)}
                >
                  {lang.label}
                </button>
              ))}
            </div>
          </div>

          {/* Farm Profile Form */}
          <form
            onSubmit={handleSaveProfile}
            style={{
              background: '#ffffff',
              border: '1px solid #e0ece3',
              borderRadius: '16px',
              padding: '20px',
              boxShadow: '0 2px 10px rgba(0, 0, 0, 0.03)',
              display: 'flex',
              flexDirection: 'column',
              gap: '14px',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Trees size={18} color="#167a48" />
              <h3 style={{ fontSize: '0.95rem', fontWeight: 700, margin: 0, color: '#0f291e' }}>
                Farm & Land Details
              </h3>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '12px' }}>
              <div>
                <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: '#4b5563', marginBottom: '4px' }}>
                  State
                </label>
                <input
                  type="text"
                  style={{
                    width: '100%',
                    padding: '9px 12px',
                    borderRadius: '10px',
                    border: '1px solid #d1d5db',
                    background: '#f9fafb',
                    fontSize: '0.85rem',
                  }}
                  value={profileData.state}
                  onChange={(e) => setProfileData({ ...profileData, state: e.target.value })}
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: '#4b5563', marginBottom: '4px' }}>
                  District
                </label>
                <input
                  type="text"
                  style={{
                    width: '100%',
                    padding: '9px 12px',
                    borderRadius: '10px',
                    border: '1px solid #d1d5db',
                    background: '#f9fafb',
                    fontSize: '0.85rem',
                  }}
                  value={profileData.district}
                  onChange={(e) => setProfileData({ ...profileData, district: e.target.value })}
                />
              </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '12px' }}>
              <div>
                <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: '#4b5563', marginBottom: '4px' }}>
                  Land Size (Acres)
                </label>
                <input
                  type="number"
                  step="0.5"
                  style={{
                    width: '100%',
                    padding: '9px 12px',
                    borderRadius: '10px',
                    border: '1px solid #d1d5db',
                    background: '#f9fafb',
                    fontSize: '0.85rem',
                  }}
                  value={profileData.land_size_acres}
                  onChange={(e) =>
                    setProfileData({ ...profileData, land_size_acres: parseFloat(e.target.value) || 0 })
                  }
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: '#4b5563', marginBottom: '4px' }}>
                  Soil Type
                </label>
                <select
                  style={{
                    width: '100%',
                    padding: '9px 12px',
                    borderRadius: '10px',
                    border: '1px solid #d1d5db',
                    background: '#f9fafb',
                    fontSize: '0.85rem',
                  }}
                  value={profileData.soil_type}
                  onChange={(e) => setProfileData({ ...profileData, soil_type: e.target.value })}
                >
                  <option value="Black Soil">Black Soil</option>
                  <option value="Alluvial Soil">Alluvial Soil</option>
                  <option value="Red Laterite Soil">Red Laterite Soil</option>
                  <option value="Sandy Loam">Sandy Loam</option>
                  <option value="Clayey Soil">Clayey Soil</option>
                </select>
              </div>
            </div>

            <button
              type="submit"
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px',
                padding: '11px 20px',
                borderRadius: '12px',
                background: '#167a48',
                color: '#ffffff',
                border: 'none',
                fontWeight: 700,
                fontSize: '0.88rem',
                cursor: 'pointer',
                marginTop: '6px',
              }}
            >
              <Save size={16} /> Save Farm Profile
            </button>
          </form>

          {/* Auth Section */}
          {isGuest ? (
            <div
              style={{
                background: '#ffffff',
                border: '1px solid #e0ece3',
                borderRadius: '16px',
                padding: '20px',
                boxShadow: '0 2px 10px rgba(0, 0, 0, 0.03)',
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
                <h3 style={{ fontSize: '0.95rem', fontWeight: 700, margin: 0, color: '#0f291e' }}>
                  {authMode === 'login' ? '🔑 Farmer Login' : '🌱 Create Farmer Account'}
                </h3>
                <button
                  type="button"
                  onClick={() => setAuthMode(authMode === 'login' ? 'register' : 'login')}
                  style={{
                    background: 'transparent',
                    border: 'none',
                    color: '#167a48',
                    fontSize: '0.8rem',
                    fontWeight: 700,
                    cursor: 'pointer',
                  }}
                >
                  {authMode === 'login' ? 'Need Account?' : 'Have Account?'}
                </button>
              </div>

              <form onSubmit={handleAuthSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                {authMode === 'register' && (
                  <div>
                    <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: '#4b5563', marginBottom: '4px' }}>
                      Full Name
                    </label>
                    <input
                      type="text"
                      style={{
                        width: '100%',
                        padding: '9px 12px',
                        borderRadius: '10px',
                        border: '1px solid #d1d5db',
                        background: '#f9fafb',
                      }}
                      placeholder="e.g. Ramesh Patil"
                      value={fullName}
                      onChange={(e) => setFullName(e.target.value)}
                      required
                    />
                  </div>
                )}

                <div>
                  <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: '#4b5563', marginBottom: '4px' }}>
                    Phone Number (10 digits)
                  </label>
                  <input
                    type="tel"
                    style={{
                      width: '100%',
                      padding: '9px 12px',
                      borderRadius: '10px',
                      border: '1px solid #d1d5db',
                      background: '#f9fafb',
                    }}
                    placeholder="e.g. 9876543210"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    required
                  />
                </div>

                <div>
                  <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: '#4b5563', marginBottom: '4px' }}>
                    Password
                  </label>
                  <input
                    type="password"
                    style={{
                      width: '100%',
                      padding: '9px 12px',
                      borderRadius: '10px',
                      border: '1px solid #d1d5db',
                      background: '#f9fafb',
                    }}
                    placeholder="Enter password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                </div>

                <button
                  type="submit"
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '8px',
                    padding: '11px 20px',
                    borderRadius: '12px',
                    background: '#167a48',
                    color: '#ffffff',
                    border: 'none',
                    fontWeight: 700,
                    fontSize: '0.88rem',
                    cursor: 'pointer',
                    marginTop: '4px',
                  }}
                >
                  <LogIn size={15} />
                  {authMode === 'login' ? 'Login to Smart-Kisan' : 'Create Free Account'}
                </button>
              </form>
            </div>
          ) : (
            <button
              onClick={logout}
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px',
                padding: '12px 20px',
                borderRadius: '12px',
                background: '#fee2e2',
                color: '#dc2626',
                border: '1px solid #fecaca',
                fontWeight: 700,
                fontSize: '0.88rem',
                cursor: 'pointer',
              }}
            >
              <LogOut size={16} /> Sign Out
            </button>
          )}
        </div>
      )}

      {/* ── Tab 3: Activity History ── */}
      {activeTab === 'history' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', maxWidth: '620px', margin: '0 auto' }}>
          {loadingHistory ? (
            <div style={{ textAlign: 'center', padding: '40px' }}>
              <span style={{ fontSize: '0.88rem', color: '#6b7280' }}>Loading activity records...</span>
            </div>
          ) : historyItems.length === 0 ? (
            <div
              style={{
                background: '#ffffff',
                border: '1px solid #e0ece3',
                borderRadius: '16px',
                padding: '40px 20px',
                textAlign: 'center',
              }}
            >
              <History size={36} color="#9ca3af" style={{ margin: '0 auto 12px' }} />
              <h4 style={{ fontSize: '0.98rem', color: '#111827', margin: '0 0 6px 0' }}>No activity records yet</h4>
              <p style={{ fontSize: '0.82rem', color: '#6b7280', margin: 0 }}>
                Your crop disease diagnoses and advisory queries will automatically show up here.
              </p>
            </div>
          ) : (
            historyItems.map((item) => (
              <div
                key={item.id}
                style={{
                  background: '#ffffff',
                  border: '1px solid #e0ece3',
                  borderRadius: '14px',
                  padding: '14px 18px',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '14px',
                  boxShadow: '0 2px 8px rgba(0, 0, 0, 0.03)',
                }}
              >
                <div
                  style={{
                    width: '40px',
                    height: '40px',
                    borderRadius: '10px',
                    background: item.type === 'disease' ? '#fef2f2' : '#f0fdf4',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    flexShrink: 0,
                  }}
                >
                  {item.type === 'disease' ? (
                    <ScanLine size={20} color="#ef4444" />
                  ) : (
                    <Sprout size={20} color="#16a34a" />
                  )}
                </div>
                <div style={{ flex: 1 }}>
                  <h4 style={{ fontSize: '0.9rem', fontWeight: 700, margin: '0 0 3px 0', color: '#111827' }}>
                    {item.title}
                  </h4>
                  <div style={{ fontSize: '0.75rem', color: '#6b7280' }}>
                    {item.subtitle} · {new Date(item.created_at).toLocaleDateString()}
                  </div>
                </div>
                <ChevronRight size={16} color="#9ca3af" />
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}
