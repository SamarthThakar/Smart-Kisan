import React from 'react';
import { NavLink, Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import {
  Home,
  Store,
  Brain,
  Bell,
  User,
  Sprout,
} from 'lucide-react';

export default function Sidebar() {
  const { t } = useTranslation();

  const navItems = [
    { to: '/', label: 'Home', icon: Home, end: true },
    { to: '/market', label: 'Market', icon: Store },
    { to: '/crop', label: 'AI', icon: Brain },
    { to: '/schemes', label: 'Alerts', icon: Bell, badge: 3 },
    { to: '/profile', label: 'Profile', icon: User },
  ];

  return (
    <aside className="app-sidebar">
      {/* Brand Header */}
      <Link to="/" className="sidebar-brand">
        <div className="sidebar-brand-icon">
          <Sprout size={24} color="#15803d" />
        </div>
        <div className="sidebar-brand-text">
          <span className="sidebar-brand-title">Smart Farming</span>
          <span className="sidebar-brand-subtitle">Assistant</span>
        </div>
      </Link>

      {/* Nav Menu */}
      <nav className="sidebar-nav">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) =>
                `sidebar-nav-item ${isActive ? 'active' : ''}`
              }
            >
              <div className="sidebar-nav-icon">
                <Icon size={19} />
              </div>
              <span className="sidebar-nav-label">{item.label}</span>
              {item.badge && (
                <span className="sidebar-badge">{item.badge}</span>
              )}
            </NavLink>
          );
        })}
      </nav>

      {/* Illustrated Field Footer */}
      <div className="sidebar-footer">
        <div className="sidebar-field-art">
          <img
            src="/assets/tractor-field.jpg"
            alt="Field with tractor"
            className="sidebar-art-img"
          />
        </div>
      </div>
    </aside>
  );
}
