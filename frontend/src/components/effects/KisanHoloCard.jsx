import React, { useRef, useEffect, useState } from 'react';

/**
 * KisanHoloCard — React host for the self-contained Three.js
 * holographic trading card effect.
 *
 * Loads the card scene in an iframe, handles lifecycle, lazy-loading,
 * WebGL fallback, and responsive sizing.
 *
 * @param {Object} props
 * @param {string} [props.variant='golden-wheat'] - Card variant
 * @param {string} [props.title] - Optional title overlay
 * @param {string} [props.className] - Additional CSS class
 */
export default function KisanHoloCard({ variant = 'golden-wheat', title, className = '' }) {
  const containerRef = useRef(null);
  const iframeRef = useRef(null);
  const [loaded, setLoaded] = useState(false);
  const [error, setError] = useState(false);

  useEffect(() => {
    // IntersectionObserver for lazy-load
    const container = containerRef.current;
    if (!container) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && iframeRef.current) {
          if (!iframeRef.current.src) {
            iframeRef.current.src = '/effects/kisan-holo-card.html';
          }
        }
      },
      { threshold: 0.1 }
    );

    observer.observe(container);
    return () => observer.disconnect();
  }, []);

  const handleLoad = () => {
    setLoaded(true);
  };

  const handleError = () => {
    setError(true);
  };

  return (
    <div
      ref={containerRef}
      className={`kisan-holo-card-container ${className}`}
      style={{
        position: 'relative',
        width: '100%',
        aspectRatio: '3 / 4',
        overflow: 'hidden',
        borderRadius: 'var(--radius-xl, 24px)',
        background: 'radial-gradient(ellipse at center, rgba(26, 74, 46, 0.3), rgba(10, 26, 13, 0.9))',
      }}
    >
      {/* Loading state */}
      {!loaded && !error && (
        <div
          style={{
            position: 'absolute',
            inset: 0,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '12px',
            zIndex: 2,
          }}
        >
          <div
            style={{
              width: '40px',
              height: '40px',
              border: '3px solid rgba(245, 158, 11, 0.2)',
              borderTopColor: '#f59e0b',
              borderRadius: '50%',
              animation: 'spin 0.8s linear infinite',
            }}
          />
          <span style={{ fontSize: '0.8rem', color: 'rgba(245, 158, 11, 0.6)', fontFamily: 'var(--font-heading, Outfit, sans-serif)' }}>
            Loading 3D Card...
          </span>
        </div>
      )}

      {/* Error fallback */}
      {error && (
        <div
          style={{
            position: 'absolute',
            inset: 0,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '8px',
            background: 'var(--bg-card, #162B1A)',
            zIndex: 2,
          }}
        >
          <span style={{ fontSize: '3rem' }}>🌾</span>
          <span style={{ fontSize: '0.85rem', color: 'var(--text-muted, #6B7B6E)' }}>
            3D Card requires WebGL
          </span>
        </div>
      )}

      {/* Three.js iframe */}
      <iframe
        ref={iframeRef}
        title="Kisan Holographic Card"
        onLoad={handleLoad}
        onError={handleError}
        allow="accelerometer; autoplay"
        sandbox="allow-scripts allow-same-origin"
        style={{
          position: 'absolute',
          inset: 0,
          width: '100%',
          height: '100%',
          border: 'none',
          opacity: loaded ? 1 : 0,
          transition: 'opacity 0.6s ease',
        }}
      />

      {/* Optional title overlay */}
      {title && loaded && (
        <div
          style={{
            position: 'absolute',
            top: '16px',
            left: '50%',
            transform: 'translateX(-50%)',
            background: 'rgba(10, 26, 13, 0.75)',
            backdropFilter: 'blur(8px)',
            padding: '6px 16px',
            borderRadius: '20px',
            border: '1px solid rgba(245, 158, 11, 0.3)',
            fontSize: '0.75rem',
            fontWeight: 700,
            color: '#f59e0b',
            fontFamily: 'var(--font-heading, Outfit, sans-serif)',
            letterSpacing: '0.04em',
            whiteSpace: 'nowrap',
            pointerEvents: 'none',
            zIndex: 3,
          }}
        >
          {title}
        </div>
      )}
    </div>
  );
}
