import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import {
  Landmark,
  Search,
  ExternalLink,
  CheckCircle,
  FileText,
  Filter,
  Sparkles,
  ChevronRight,
  Shield,
  CreditCard,
  Percent,
  Droplets,
  Sprout,
  TrendingUp,
  X,
} from 'lucide-react';
import { api } from '../services/api';
import toast from 'react-hot-toast';

export default function Schemes() {
  const { t } = useTranslation();

  const [schemes, setSchemes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedType, setSelectedType] = useState('all');
  const [selectedScheme, setSelectedScheme] = useState(null);

  const categories = [
    { id: 'all', label: 'All Schemes', icon: Landmark },
    { id: 'subsidy', label: 'Subsidy & Grants', icon: Percent },
    { id: 'insurance', label: 'Crop Insurance', icon: Shield },
    { id: 'credit', label: 'Kisan Credit & Loans', icon: CreditCard },
    { id: 'irrigation', label: 'Irrigation', icon: Droplets },
    { id: 'organic', label: 'Organic Farming', icon: Sprout },
    { id: 'market', label: 'Market Linkage', icon: TrendingUp },
  ];

  useEffect(() => {
    fetchSchemes();
  }, [selectedType]);

  const fetchSchemes = async () => {
    setLoading(true);
    try {
      const params = {};
      if (selectedType !== 'all') params.scheme_type = selectedType;
      if (searchQuery.trim()) params.q = searchQuery.trim();

      const res = await api.getSchemes(params);
      if (res?.schemes && res.schemes.length > 0) {
        setSchemes(res.schemes);
      } else if (res?.schemes && selectedType !== 'all') {
        setSchemes([]);
      } else {
        throw new Error('No schemes found from backend');
      }
    } catch (err) {
      console.warn('Backend schemes call returned empty or failed, using built-in fallback list', err);
      // Fallback seeded list
      console.warn('Backend schemes call failed, using default seeded schemes list', err);
      // Fallback seeded list
      setSchemes([
        {
          id: 'pm-kisan',
          scheme_name: 'Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)',
          short_name: 'PM-KISAN',
          ministry: 'Ministry of Agriculture & Farmers Welfare',
          scheme_type: 'subsidy',
          description: 'Direct income support of ₹6,000/year to all eligible land-holding farmer families in 3 equal installments of ₹2,000.',
          benefits: [
            '₹6,000 per year directly to bank account via DBT',
            'No intermediaries or commission',
            'Covers small, marginal and large landholders',
          ],
          eligibility_criteria: {
            land_holding: 'Must possess cultivable landholding',
            exclusions: 'Institutional landholders, income tax payers excluded',
          },
          required_documents: ['Aadhaar Card', 'Bank Passbook', 'Land Khatauni / 7/12 Extract'],
          official_url: 'https://pmkisan.gov.in',
        },
        {
          id: 'pmfby',
          scheme_name: 'Pradhan Mantri Fasal Bima Yojana (PMFBY)',
          short_name: 'PMFBY',
          ministry: 'Ministry of Agriculture & Farmers Welfare',
          scheme_type: 'insurance',
          description: 'Comprehensive financial support for crop loss or damage arising out of natural calamities, pests and diseases.',
          benefits: [
            'Premium as low as 2% for Kharif and 1.5% for Rabi crops',
            'Post-harvest loss coverage up to 14 days',
            'Fast digital claim processing via Crop Insurance App',
          ],
          eligibility_criteria: {
            farmers: 'All farmers cultivating notified crops in notified areas',
          },
          required_documents: ['Aadhaar Card', 'Land Records', 'Sowing Certificate'],
          official_url: 'https://pmfby.gov.in',
        },
        {
          id: 'kcc',
          scheme_name: 'Kisan Credit Card Scheme (KCC)',
          short_name: 'KCC',
          ministry: 'Ministry of Agriculture & Farmers Welfare',
          scheme_type: 'credit',
          description: 'Affordable credit up to ₹3 Lakh at an effective interest rate of 4% for timely repayments for agriculture & animal husbandry.',
          benefits: [
            'Credit limit up to ₹3 lakh at 4% concessional rate',
            'No collateral needed for loans up to ₹1.6 lakh',
            'Covers crop cultivation, seed, and fertilizer purchase',
          ],
          eligibility_criteria: {
            farmers: 'Individual/joint farmers, tenant farmers, SHGs',
          },
          required_documents: ['Aadhaar/PAN', 'Land Records', 'Passport Size Photos'],
          official_url: 'https://www.nabard.org',
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    fetchSchemes();
  };

  const filteredSchemes = schemes.filter((s) => {
    if (!searchQuery) return true;
    const q = searchQuery.toLowerCase();
    return (
      (s.scheme_name || '').toLowerCase().includes(q) ||
      (s.short_name || '').toLowerCase().includes(q) ||
      (s.description || '').toLowerCase().includes(q) ||
      (s.benefit_summary || '').toLowerCase().includes(q)
    );
  });

  return (
    <div className="page">
      <div className="page-content" style={{ gap: '20px' }}>
        {/* Header */}
        <div>
          <span className="badge badge-primary">{t('schemes')}</span>
          <h1 style={{ fontSize: '1.45rem', marginTop: '6px' }}>Government Agricultural Schemes</h1>
          <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
            Find Central & State subsidies, crop insurance, and concessional loans.
          </p>
        </div>

        {/* Search Bar */}
        <form onSubmit={handleSearch} className="input-icon-wrapper">
          <Search size={18} className="input-icon" />
          <input
            type="text"
            className="input"
            placeholder={t('searchSchemesPlaceholder')}
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </form>

        {/* Category Chips */}
        <div style={{ display: 'flex', gap: '8px', overflowX: 'auto', paddingBottom: '4px' }}>
          {categories.map((c) => {
            const Icon = c.icon;
            const active = selectedType === c.id;
            return (
              <button
                key={c.id}
                onClick={() => setSelectedType(c.id)}
                className={`chip ${active ? 'active' : ''}`}
                style={{
                  background: active ? 'var(--primary)' : 'var(--bg-card-elevated)',
                  color: active ? '#FFF' : 'var(--text-secondary)',
                  borderColor: active ? 'var(--primary-light)' : 'var(--border-subtle)',
                }}
              >
                <Icon size={14} /> {c.label}
              </button>
            );
          })}
        </div>

        {/* Schemes List */}
        {loading ? (
          <div style={{ textAlign: 'center', padding: '32px' }}>
            <div className="spinner" style={{ margin: '0 auto 12px' }} />
            <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Loading government schemes...</span>
          </div>
        ) : filteredSchemes.length === 0 ? (
          <div
            style={{
              textAlign: 'center',
              padding: '36px 20px',
              background: 'var(--bg-card)',
              borderRadius: 'var(--radius-lg)',
              border: '1px solid var(--border-subtle)',
            }}
          >
            <Landmark size={36} color="var(--text-muted)" style={{ margin: '0 auto 10px' }} />
            <h3 style={{ fontSize: '1.05rem', marginBottom: '6px' }}>No schemes found</h3>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '14px' }}>
              No schemes match this category or search filter.
            </p>
            <button
              onClick={() => { setSelectedType('all'); setSearchQuery(''); }}
              className="btn btn-outline"
              style={{ fontSize: '0.8rem', padding: '6px 16px', margin: '0 auto' }}
            >
              Reset Filters
            </button>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            {filteredSchemes.map((scheme) => (
              <div
                key={scheme.id}
                className="scheme-card"
                onClick={() => setSelectedScheme(scheme)}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '8px' }}>
                  <div>
                    <span className="badge badge-gold" style={{ textTransform: 'uppercase', marginBottom: '6px' }}>
                      {scheme.scheme_type || 'Subsidy'}
                    </span>
                    <h3 style={{ fontSize: '1.05rem', margin: '4px 0 2px' }}>
                      {scheme.short_name || scheme.scheme_name}
                    </h3>
                    <div style={{ fontSize: '0.72rem', color: 'var(--text-secondary)' }}>
                      {scheme.ministry || 'Ministry of Agriculture & Farmers Welfare'}
                    </div>
                  </div>
                  <ChevronRight size={18} color="var(--text-muted)" style={{ flexShrink: 0 }} />
                </div>

                <p style={{ fontSize: '0.82rem', color: 'var(--text-primary)', marginTop: '10px', lineHeight: 1.5 }}>
                  {scheme.description || scheme.benefit_summary}
                </p>

                {/* Key Benefits Preview */}
                {scheme.benefits && scheme.benefits.length > 0 && (
                  <div style={{ marginTop: '10px', display: 'flex', flexDirection: 'column', gap: '4px' }}>
                    {scheme.benefits.slice(0, 2).map((b, idx) => (
                      <div key={idx} style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.78rem', color: '#86EFAC' }}>
                        <CheckCircle size={13} color="var(--success)" style={{ flexShrink: 0 }} />
                        <span>{b}</span>
                      </div>
                    ))}
                  </div>
                )}

                <div
                  style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    marginTop: '14px',
                    paddingTop: '10px',
                    borderTop: '1px solid var(--border-subtle)',
                  }}
                >
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                    📄 {scheme.required_documents?.length || 3} documents needed
                  </span>
                  <a
                    href={scheme.official_url || '#'}
                    target="_blank"
                    rel="noreferrer"
                    onClick={(e) => e.stopPropagation()}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '4px',
                      fontSize: '0.78rem',
                      fontWeight: 600,
                      color: 'var(--secondary)',
                    }}
                  >
                    Official Portal <ExternalLink size={13} />
                  </a>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Scheme Details Bottom Sheet Modal */}
        {selectedScheme && (
          <div className="modal-overlay" onClick={() => setSelectedScheme(null)}>
            <div className="bottom-sheet" onClick={(e) => e.stopPropagation()}>
              <div className="sheet-handle" />
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div>
                  <span className="badge badge-gold">{selectedScheme.scheme_type?.toUpperCase()}</span>
                  <h2 style={{ fontSize: '1.25rem', marginTop: '6px' }}>{selectedScheme.scheme_name}</h2>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                    {selectedScheme.ministry}
                  </div>
                </div>
                <button
                  onClick={() => setSelectedScheme(null)}
                  style={{
                    background: 'var(--bg-input)',
                    border: '1px solid var(--border-subtle)',
                    borderRadius: '50%',
                    width: '32px',
                    height: '32px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'var(--text-muted)',
                    cursor: 'pointer',
                  }}
                >
                  <X size={16} />
                </button>
              </div>

              {selectedScheme.description && (
                <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', marginTop: '12px', lineHeight: 1.5 }}>
                  {selectedScheme.description}
                </p>
              )}

              <div style={{ marginTop: '16px' }}>
                <h4 style={{ fontSize: '0.9rem', color: '#86EFAC', marginBottom: '8px' }}>Benefits & Assistance</h4>
                <ul style={{ paddingLeft: '20px', fontSize: '0.82rem', color: 'var(--text-primary)', lineHeight: 1.6 }}>
                  {(selectedScheme.benefits || []).map((b, idx) => (
                    <li key={idx}>{b}</li>
                  ))}
                </ul>
              </div>

              <div style={{ marginTop: '16px' }}>
                <h4 style={{ fontSize: '0.9rem', color: '#FCD34D', marginBottom: '8px' }}>Required Documents</h4>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                  {(selectedScheme.required_documents || ['Aadhaar Card', 'Bank Passbook', 'Land Records']).map((d, idx) => (
                    <span key={idx} className="badge badge-primary">
                      {d}
                    </span>
                  ))}
                </div>
              </div>

              <div style={{ marginTop: '24px' }}>
                <a
                  href={selectedScheme.official_url || '#'}
                  target="_blank"
                  rel="noreferrer"
                  className="btn btn-primary btn-full"
                >
                  <ExternalLink size={18} /> Visit Official Application Portal
                </a>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
