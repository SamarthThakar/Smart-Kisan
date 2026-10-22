import React from 'react';
import { NavLink } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import {
  Home,
  Store,
  Sparkles,
  Bell,
  User,
} from 'lucide-react';

export default function BottomNav() {
  const { t } = useTranslation();

  const navItems = [
    { to: '/', label: 'Home', icon: Home },
    { to: '/market', label: 'Market', icon: Store },
    { to: '/crop', label: 'AI', icon: Sparkles },
    { to: '/schemes', label: 'Alerts', icon: Bell, badge: 3 },
    { to: '/profile', label: 'Profile', icon: User },
  ];

  return (
    <nav className="mobile-bottom-nav" aria-label="Mobile Navigation">
      {navItems.map((item) => {
        const IconComponent = item.icon;
        return (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.to === '/'}
            className={({ isActive }) => `m-nav-item ${isActive ? 'active' : ''}`}
          >
            <div className="m-nav-icon-wrap">
              <IconComponent size={20} />
              {item.badge && <span className="m-nav-badge">{item.badge}</span>}
            </div>
            <span className="m-nav-label">{item.label}</span>
          </NavLink>
        );
      })}
    </nav>
  );
}
