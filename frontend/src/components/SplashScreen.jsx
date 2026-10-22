import React, { useState, useEffect } from 'react';

const PARTICLES = Array.from({ length: 16 }, (_, i) => ({
  id: i,
  x: `${Math.random() * 100}%`,
  duration: `${5 + Math.random() * 7}s`,
  delay: `${-Math.random() * 8}s`,
  sway: `${(Math.random() - 0.5) * 50}px`,
  size: `${2 + Math.random() * 3}px`,
}));

export default function SplashScreen({ isFading = false }) {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setProgress((p) => Math.min(p + 3, 100));
    }, 36);
    return () => clearInterval(interval);
  }, []);

  return (
    <div
      className={`splash-screen ${isFading ? 'fading' : ''}`}
      role="status"
      aria-label="Loading Smart Kisan"
      style={{
        background: 'radial-gradient(circle at 50% 38%, #0f3822 0%, #082114 55%, #030d07 100%)',
      }}
    >
      {/* Ambient particles */}
      <div
        aria-hidden="true"
        style={{ position: 'absolute', inset: 0, overflow: 'hidden', pointerEvents: 'none' }}
      >
        {PARTICLES.map((p) => (
          <div
            key={p.id}
            style={{
              position: 'absolute',
              left: p.x,
              top: '110%',
              width: p.size,
              height: p.size,
              borderRadius: '50%',
              background: 'rgba(245,158,11,0.5)',
              animation: `particleDrift ${p.duration} linear infinite`,
              animationDelay: p.delay,
              '--sway': p.sway,
            }}
          />
        ))}
      </div>

      {/* Radial glow behind logo */}
      <div
        aria-hidden="true"
        style={{
          position: 'absolute',
          width: '320px',
          height: '320px',
          borderRadius: '50%',
          background: 'radial-gradient(circle, rgba(34,197,94,0.22), transparent 70%)',
          pointerEvents: 'none',
        }}
      />

      {/* Logo */}
      <div className="splash-logo" style={{ fontSize: '4.8rem', zIndex: 1 }}>🌾</div>

      {/* Title */}
      <h1 className="splash-title" style={{ zIndex: 1 }}>Smart Kisan</h1>

      {/* Tagline */}
      <p className="splash-tagline" style={{ color: '#ecfdf5', opacity: 0.95, zIndex: 1 }}>
        AI-Powered Farming Assistant
        <br />
        <span style={{ fontSize: '0.85rem', color: '#fcd34d', opacity: 0.9 }}>स्मार्ट किसान · स्मार्ट हार्वेस्ट</span>
      </p>

      {/* Progress bar */}
      <div className="splash-loader" style={{ width: '90px', marginTop: '36px', zIndex: 1 }}>
        <div
          className="splash-loader-fill"
          style={{ width: `${progress}%`, transition: 'width 36ms linear' }}
        />
      </div>
    </div>
  );
}
