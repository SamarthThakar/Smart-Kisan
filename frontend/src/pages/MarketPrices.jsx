import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import {
  TrendingUp,
  TrendingDown,
  Minus,
  Sparkles,
  MapPin,
  Calendar,
  Search,
  Award,
  Filter,
} from 'lucide-react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';
import { api } from '../services/api';
import toast from 'react-hot-toast';

export default function MarketPrices() {
  const { t } = useTranslation();

  const [commodities, setCommodities] = useState([]);
  const [selectedCommodity, setSelectedCommodity] = useState('Tomato');
  const [selectedState, setSelectedState] = useState('');
  const [marketData, setMarketData] = useState(null);
  const [loading, setLoading] = useState(false);

  const states = [
    'All States',
    'Maharashtra',
    'Uttar Pradesh',
    'Madhya Pradesh',
    'Punjab',
    'Gujarat',
    'Karnataka',
    'Rajasthan',
    'Haryana',
    'Andhra Pradesh',
  ];

  useEffect(() => {
    loadCommodities();
    fetchPrices('Tomato', '');
  }, []);

  const loadCommodities = async () => {
    try {
      const res = await api.getCommodities();
      if (res?.commodities) {
        setCommodities(res.commodities);
      }
    } catch (err) {
      setCommodities([
        'Rice', 'Wheat', 'Maize', 'Cotton', 'Sugarcane', 'Soybean',
        'Groundnut', 'Onion', 'Potato', 'Tomato', 'Chilli', 'Turmeric',
        'Cumin', 'Mustard', 'Bajra', 'Jowar', 'Chickpea', 'Banana'
      ]);
    }
  };

  const fetchPrices = async (commodity, state) => {
    setLoading(true);
    try {
      const data = await api.getMarketPrices(commodity, state);
      setMarketData(data);
    } catch (err) {
      console.warn('Backend call failed, using mock market prices', err);
      // Mock fallback
      setMarketData({
        commodity,
        state: state || 'All States',
        data_date: new Date().toISOString().split('T')[0],
        source: 'Sample Data (data.gov.in format)',
        is_live: false,
        trend: { direction: 'rising', pct_change: 4.8 },
        markets: [
          { market: 'Lasalgaon Mandi', district: 'Nashik', state: 'Maharashtra', min_price: 1350, max_price: 1850, modal_price: 1650, variety: 'Desi', is_best_market: false },
          { market: 'Vashi APMC', district: 'Navi Mumbai', state: 'Maharashtra', min_price: 1500, max_price: 2100, modal_price: 1950, variety: 'Hybrid', is_best_market: true },
          { market: 'Pune Market Yard', district: 'Pune', state: 'Maharashtra', min_price: 1400, max_price: 1900, modal_price: 1720, variety: 'Desi', is_best_market: false },
          { market: 'Azadpur Mandi', district: 'North Delhi', state: 'Delhi', min_price: 1450, max_price: 2000, modal_price: 1800, variety: 'Local', is_best_market: false },
          { market: 'Ahmedabad APMC', district: 'Ahmedabad', state: 'Gujarat', min_price: 1300, max_price: 1750, modal_price: 1580, variety: 'Hybrid', is_best_market: false },
        ],
      });
    } finally {
      setLoading(false);
    }
  };

  const handleCommodityChange = (e) => {
    const val = e.target.value;
    setSelectedCommodity(val);
    fetchPrices(val, selectedState);
  };

  const handleStateChange = (e) => {
    const val = e.target.value;
    setSelectedState(val);
    fetchPrices(selectedCommodity, val);
  };

  const bestMarket = marketData?.markets?.find((m) => m.is_best_market) || marketData?.markets?.[0];

  const chartData = (marketData?.markets || []).slice(0, 6).map((m) => ({
    name: m.market.replace(' APMC', '').replace(' Mandi', ''),
    modal: m.modal_price,
    min: m.min_price,
    max: m.max_price,
  }));

  return (
    <div className="page">
      <div className="page-content" style={{ gap: '20px' }}>
        {/* Title */}
        <div>
          <span className="badge badge-primary">{t('marketPrices')}</span>
          <h1 style={{ fontSize: '1.45rem', marginTop: '6px' }}>{t('checkPrices')}</h1>
          <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
            Real-time mandi prices across India to help you sell at peak rates.
          </p>
        </div>

        {/* Filter Selection Bar */}
        <div className="card card-elevated" style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '10px' }}>
            <div className="input-group">
              <label className="input-label">{t('selectCommodity')}</label>
              <select
                className="input"
                value={selectedCommodity}
                onChange={handleCommodityChange}
              >
                {commodities.map((c) => (
                  <option key={c} value={c}>
                    {c}
                  </option>
                ))}
              </select>
            </div>
            <div className="input-group">
              <label className="input-label">{t('selectState')}</label>
              <select
                className="input"
                value={selectedState}
                onChange={handleStateChange}
              >
                {states.map((s) => (
                  <option key={s} value={s === 'All States' ? '' : s}>
                    {s}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Best Price Alert Banner */}
        {bestMarket && (
          <div
            className="card"
            style={{
              background: 'linear-gradient(135deg, rgba(245, 158, 11, 0.15), rgba(45, 122, 58, 0.2))',
              border: '1px solid rgba(245, 158, 11, 0.4)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <div
                style={{
                  width: '42px',
                  height: '42px',
                  borderRadius: '12px',
                  background: 'var(--gradient-gold)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}
              >
                <Award size={22} color="#1A0A00" />
              </div>
              <div>
                <div style={{ fontSize: '0.72rem', color: 'var(--secondary-light)', fontWeight: 700 }}>
                  🌟 {t('bestMandiAlert')}
                </div>
                <div style={{ fontSize: '1.05rem', fontWeight: 800, color: 'var(--text-primary)' }}>
                  {bestMarket.market}
                </div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                  {bestMarket.district}, {bestMarket.state}
                </div>
              </div>
            </div>
            <div style={{ textAlign: 'right' }}>
              <div style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--secondary)' }}>
                ₹{bestMarket.modal_price}
              </div>
              <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)' }}>/ quintal</div>
            </div>
          </div>
        )}

        {/* Price Trend Chart with Recharts */}
        {chartData.length > 0 && (
          <div className="card" style={{ padding: '16px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
              <h3 style={{ fontSize: '0.95rem' }}>Mandi Price Comparison (₹/Qtl)</h3>
              <span className="badge badge-success">Modal Rate</span>
            </div>
            <div style={{ width: '100%', height: 180 }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData} margin={{ top: 5, right: 10, left: -20, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.08)" />
                  <XAxis dataKey="name" stroke="#86EFAC" fontSize={10} tickLine={false} />
                  <YAxis stroke="#86EFAC" fontSize={10} tickLine={false} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#162B1A',
                      borderColor: '#2D7A3A',
                      borderRadius: '8px',
                      color: '#F0FDF4',
                    }}
                  />
                  <Bar dataKey="modal" fill="#22C55E" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

        {/* Full Mandi Rates Table */}
        <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
          <div style={{ padding: '14px 16px', borderBottom: '1px solid var(--border-subtle)' }}>
            <h3 style={{ fontSize: '0.95rem', margin: 0 }}>All Market Mandi Rates</h3>
          </div>

          {loading ? (
            <div style={{ padding: '32px', textAlign: 'center' }}>
              <div className="spinner" style={{ margin: '0 auto 12px' }} />
              <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Loading live mandi data...</span>
            </div>
          ) : (
            <div style={{ overflowX: 'auto' }}>
              <table className="price-table">
                <thead>
                  <tr>
                    <th>{t('mandiName')}</th>
                    <th>Variety</th>
                    <th>{t('modalPrice')}</th>
                    <th>{t('minMax')}</th>
                  </tr>
                </thead>
                <tbody>
                  {marketData?.markets?.map((m, idx) => (
                    <tr key={idx} className={m.is_best_market ? 'best-market-row' : ''}>
                      <td>
                        <div style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{m.market}</div>
                        <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                          {m.district}, {m.state}
                        </div>
                      </td>
                      <td>
                        <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                          {m.variety || 'Standard'}
                        </span>
                      </td>
                      <td>
                        <div style={{ fontWeight: 700, color: m.is_best_market ? 'var(--secondary)' : 'var(--text-primary)' }}>
                          ₹{m.modal_price}
                        </div>
                        <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)' }}>per qtl</div>
                      </td>
                      <td>
                        <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                          ₹{m.min_price} - ₹{m.max_price}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
