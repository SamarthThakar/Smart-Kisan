import React, { useState, useEffect, useCallback } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import {
  Sun,
  CloudSun,
  CloudRain,
  Thermometer,
  Calendar,
  Cloud,
  Store,
  MessageSquare,
  Landmark,
  Sprout,
  TrendingUp,
  ChevronRight,
  Bot,
  MapPin,
  Wind,
  Droplets,
  Zap,
  ArrowRight,
  Sparkles,
} from 'lucide-react';
import { api } from '../services/api';
import { useAuth } from '../context/AuthContext';

export default function Home() {
  const { t } = useTranslation();
  const { user } = useAuth();
  const navigate = useNavigate();

  const [weather, setWeather] = useState(null);
  const [loadingWeather, setLoadingWeather] = useState(true);
  const [locationName, setLocationName] = useState('Pune, Maharashtra');
  const [latLon, setLatLon] = useState({ lat: 18.5204, lon: 73.8567 });

  const fetchWeatherData = useCallback(async (lat, lon) => {
    setLoadingWeather(true);
    try {
      const data = await api.getWeather(lat, lon);
      setWeather(data);
    } catch (err) {
      console.warn('Using fallback weather data', err);
      setWeather({
        current: {
          temperature: 28.0,
          feels_like: 28.0,
          humidity: 72,
          wind_speed: 12.0,
          precipitation: 0.0,
          conditions: 'Partly Cloudy',
        },
        forecast: [
          { day: 'Mon', max_temp: 27, min_temp: 20, condition: 'Sunny', weather_code: 0 },
          { day: 'Tue', max_temp: 26, min_temp: 19, condition: 'Cloudy', weather_code: 2 },
          { day: 'Wed', max_temp: 27, min_temp: 20, condition: 'Rain', weather_code: 61 },
          { day: 'Thu', max_temp: 28, min_temp: 21, condition: 'Sunny', weather_code: 0 },
        ],
        farming_advice: [
          {
            title: 'Optimal Irrigation Window',
            message: 'Rain expected tomorrow. Delay fertilizer application.',
            action: 'Hold irrigation for 24-48 hours',
          },
        ],
      });
    } finally {
      setLoadingWeather(false);
    }
  }, []);

  useEffect(() => {
    if (user?.district) {
      setLocationName(`${user.district}${user.state ? ', ' + user.state : ''}`);
    }

    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        async (pos) => {
          const lat = pos.coords.latitude;
          const lon = pos.coords.longitude;
          setLatLon({ lat, lon });

          try {
            const res = await fetch(
              `https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${lat}&longitude=${lon}&localityLanguage=en`
            );
            if (res.ok) {
              const data = await res.json();
              const place = data.city || data.locality || data.principalSubdivision;
              if (place) {
                const fullPlace =
                  data.principalSubdivision && data.city !== data.principalSubdivision
                    ? `${place}, ${data.principalSubdivision}`
                    : place;
                setLocationName(fullPlace);
              }
            }
          } catch {
            // fallback
          }

          fetchWeatherData(lat, lon);
        },
        () => fetchWeatherData(latLon.lat, latLon.lon),
        { timeout: 7000 }
      );
    } else {
      fetchWeatherData(latLon.lat, latLon.lon);
    }
  }, [fetchWeatherData, user]);

  // Weather metrics
  const currentTemp = weather?.current?.temperature != null
    ? Math.round(weather.current.temperature)
    : 28;
  const currentCondition =
    weather?.current?.conditions || weather?.current?.condition || 'Partly Cloudy';
  const currentHumidity =
    weather?.current?.humidity ?? weather?.current?.relative_humidity ?? 72;
  const currentWind = weather?.current?.wind_speed != null
    ? Math.round(weather.current.wind_speed)
    : 12;
  const currentRain = weather?.current?.precipitation != null && weather.current.precipitation > 0
    ? `${weather.current.precipitation} mm`
    : 'Low';

  // 4-day forecast for the weather widget
  const miniForecast = (weather?.forecast && weather.forecast.length > 0)
    ? weather.forecast.slice(0, 4).map((f, idx) => {
        const dayLabel = f.day || (f.date ? new Date(f.date).toLocaleDateString(undefined, { weekday: 'short' }) : (idx === 0 ? 'Mon' : `+${idx}d`));
        const maxT = Math.round(f.max_temp ?? f.temp_max ?? 28);
        const minT = Math.round(f.min_temp ?? f.temp_min ?? 20);
        const cond = f.condition || (f.weather_code === 0 ? 'Sunny' : f.weather_code <= 3 ? 'Cloudy' : 'Rain');
        return { day: dayLabel, max: maxT, min: minT, cond, code: f.weather_code };
      })
    : [
        { day: 'Mon', max: 27, min: 20, cond: 'Sunny' },
        { day: 'Tue', max: 26, min: 19, cond: 'Cloudy' },
        { day: 'Wed', max: 27, min: 20, cond: 'Rain' },
        { day: 'Thu', max: 28, min: 21, cond: 'Sunny' },
      ];

  // Time-aware greeting
  const getTimeGreeting = () => {
    const hour = new Date().getHours();
    if (hour >= 4 && hour < 12) {
      return {
        text: 'Good Morning',
        icon: Sun,
        color: '#f59e0b',
        bg: '#fef3c7',
        timeDesc: 'Expected Today',
      };
    } else if (hour >= 12 && hour < 17) {
      return {
        text: 'Good Afternoon',
        icon: Sun,
        color: '#f59e0b',
        bg: '#fef3c7',
        timeDesc: 'This Afternoon',
      };
    } else if (hour >= 17 && hour < 22) {
      return {
        text: 'Good Evening',
        icon: CloudSun,
        color: '#f97316',
        bg: '#ffedd5',
        timeDesc: 'Tonight',
      };
    } else {
      return {
        text: 'Good Night',
        icon: CloudSun,
        color: '#818cf8',
        bg: '#e0e7ff',
        timeDesc: 'Tonight',
      };
    }
  };

  const greeting = getTimeGreeting();
  const GreetingIcon = greeting.icon;

  // AI Recommendation text
  const aiRecommendation = weather?.farming_advice?.[0]?.message ||
    'Rain expected tomorrow. Delay fertilizer application.';

  return (
    <div className="dashboard-page">
      {/* ── Top Panoramic Banner & Welcome ── */}
      <section className="dashboard-hero-banner">
        <div className="dashboard-hero-content">
          <h1 className="dashboard-hero-title">
            Welcome to Smart Farming Assistant
          </h1>
          <p className="dashboard-hero-subtitle">
            Smarter decisions. Healthier crops. A sustainable tomorrow.
          </p>
        </div>
      </section>

      {/* ── Two-Column Main Grid ── */}
      <div className="dashboard-grid">
        {/* ── Left Column (Main Activities) ── */}
        <div className="dashboard-main-col">
          {/* Weather Greeting Strip */}
          <div className="weather-greeting-card">
            {/* Segment 1: Greeting + Village */}
            <div className="greeting-segment">
              <div className="greeting-icon-wrap" style={{ background: greeting.bg }}>
                <GreetingIcon size={26} color={greeting.color} />
              </div>
              <div>
                <div className="greeting-title">
                  {greeting.text}, {user?.full_name?.split(' ')[0] || 'Kisan'}!
                </div>
                <div className="greeting-sub">
                  <MapPin size={12} color="#4b5563" /> Village: {locationName}
                </div>
              </div>
            </div>

            <div className="greeting-divider" />

            {/* Segment 2: Temperature + Humidity */}
            <div className="greeting-segment">
              <div className="greeting-icon-wrap temp-icon">
                <Thermometer size={26} color="#ef4444" />
              </div>
              <div>
                <div className="greeting-title">
                  {currentTemp}°C
                </div>
                <div className="greeting-sub">
                  <Droplets size={12} color="#3b82f6" /> Humidity {currentHumidity}%
                </div>
              </div>
            </div>

            <div className="greeting-divider" />

            {/* Segment 3: Condition + Expected Rain */}
            <div className="greeting-segment">
              <div className="greeting-icon-wrap rain-icon">
                <CloudRain size={26} color="#3b82f6" />
              </div>
              <div>
                <div className="greeting-title">
                  {currentCondition.includes('Rain') ? 'Light Rain' : currentCondition}
                </div>
                <div className="greeting-sub">
                  {greeting.timeDesc}
                </div>
              </div>
            </div>
          </div>

          {/* ⚡ Quick Actions */}
          <div className="dashboard-section">
            <h2 className="section-title">
              <Zap size={16} color="#15803d" /> Quick Actions
            </h2>
            <div className="quick-actions-grid">
              <Link to="/crop" className="quick-action-card card-schedule">
                <div className="qa-left">
                  <div className="qa-icon-wrap qa-icon-schedule">
                    <Calendar size={18} color="#15803d" />
                  </div>
                  <span className="qa-label">Schedule</span>
                </div>
                <ArrowRight size={15} className="qa-arrow" />
              </Link>

              <a href="#weather-card" className="quick-action-card card-weather">
                <div className="qa-left">
                  <div className="qa-icon-wrap qa-icon-weather">
                    <Cloud size={18} color="#2563eb" />
                  </div>
                  <span className="qa-label">Weather</span>
                </div>
                <ArrowRight size={15} className="qa-arrow" />
              </a>

              <Link to="/market" className="quick-action-card card-market">
                <div className="qa-left">
                  <div className="qa-icon-wrap qa-icon-market">
                    <Store size={18} color="#ea580c" />
                  </div>
                  <span className="qa-label">Market</span>
                </div>
                <ArrowRight size={15} className="qa-arrow" />
              </Link>

              <Link to="/chat" className="quick-action-card card-ai">
                <div className="qa-left">
                  <div className="qa-icon-wrap qa-icon-ai">
                    <MessageSquare size={18} color="#7c3aed" />
                  </div>
                  <span className="qa-label">Ask AI</span>
                </div>
                <ArrowRight size={15} className="qa-arrow" />
              </Link>
            </div>
          </div>

          {/* 👥 Feature Categories */}
          <div className="dashboard-section">
            <h2 className="section-title">
              <Sparkles size={16} color="#15803d" /> Feature Categories
            </h2>
            <div className="features-2x2-grid">
              {/* Government Schemes */}
              <Link to="/schemes" className="feature-category-card">
                <div className="fc-icon-wrap fc-schemes">
                  <Landmark size={22} color="#15803d" />
                </div>
                <div className="fc-text">
                  <div className="fc-title">Government Schemes</div>
                  <div className="fc-desc">Subsidies • PM-KISAN • Crop Insurance</div>
                </div>
                <ChevronRight size={16} className="fc-arrow" />
              </Link>

              {/* Expert Guidance */}
              <Link to="/crop" className="feature-category-card">
                <div className="fc-icon-wrap fc-guidance">
                  <Sprout size={22} color="#0284c7" />
                </div>
                <div className="fc-text">
                  <div className="fc-title">Expert Guidance</div>
                  <div className="fc-desc">Crop Selection • Fertilizer • Pest Control</div>
                </div>
                <ChevronRight size={16} className="fc-arrow" />
              </Link>

              {/* Weather Advisory */}
              <a href="#weather-card" className="feature-category-card">
                <div className="fc-icon-wrap fc-weather">
                  <CloudRain size={22} color="#7c3aed" />
                </div>
                <div className="fc-text">
                  <div className="fc-title">Weather Advisory</div>
                  <div className="fc-desc">Rain Forecast • Temperature • Harvest Alerts</div>
                </div>
                <ChevronRight size={16} className="fc-arrow" />
              </a>

              {/* Market Prices */}
              <Link to="/market" className="feature-category-card">
                <div className="fc-icon-wrap fc-market">
                  <TrendingUp size={22} color="#ea580c" />
                </div>
                <div className="fc-text">
                  <div className="fc-title">Market Prices</div>
                  <div className="fc-desc">Daily Mandi Rates • Nearby Markets</div>
                </div>
                <ChevronRight size={16} className="fc-arrow" />
              </Link>
            </div>
          </div>

          {/* 🌱 Crop Progress */}
          <div className="dashboard-section">
            <h2 className="section-title">
              <Sprout size={16} color="#15803d" /> Crop Progress
            </h2>
            <Link to="/crop" className="crop-progress-card">
              <div className="crop-thumb-wrap">
                <img
                  src="/assets/crop-soybean.jpg"
                  alt="Soybean Crop"
                  className="crop-thumb-img"
                />
              </div>

              <div className="crop-progress-details">
                <div className="crop-progress-header">
                  <span className="crop-stage-percent">70% Growth Stage</span>
                </div>
                <div className="crop-progress-bar-bg">
                  <div className="crop-progress-bar-fill" style={{ width: '70%' }} />
                </div>
                <div className="crop-meta-row">
                  <span className="crop-name-tag">Crop: Soybean</span>
                  <span className="crop-meta-item">
                    <Sprout size={13} color="#15803d" /> Stage: Vegetative
                  </span>
                  <span className="crop-meta-item">
                    <Calendar size={13} color="#6b7280" /> Next: Flowering
                  </span>
                </div>
              </div>

              <ChevronRight size={18} className="crop-arrow" />
            </Link>
          </div>

          {/* 💬 Bottom Prompt Bar */}
          <div className="bottom-ask-banner">
            <div className="ask-banner-left">
              <div className="ask-sprout-icon">
                <Sprout size={20} color="#15803d" />
              </div>
              <span className="ask-banner-text">
                Get smarter responses, upload files and images, and more.
              </span>
            </div>
            <Link to="/chat" className="btn-ask-anything">
              <MessageSquare size={14} /> Ask Anything
            </Link>
          </div>
        </div>

        {/* ── Right Column (Sidebar Widgets) ── */}
        <div className="dashboard-sidebar-col" id="weather-card">
          {/* Today's Weather Card */}
          <div className="sidebar-card weather-widget-card">
            <h3 className="widget-card-title">Today's Weather</h3>

            <div className="weather-main-row">
              <div className="weather-illustration">
                <CloudSun size={46} color="#3b82f6" />
              </div>
              <div>
                <div className="weather-big-temp">
                  {loadingWeather ? '—' : `${currentTemp}°C`}
                </div>
                <div className="weather-big-cond">{currentCondition}</div>
              </div>
            </div>

            {/* Metrics Chips */}
            <div className="weather-metrics-chips">
              <div className="metric-chip">
                <div className="metric-chip-icon">
                  <Droplets size={14} color="#3b82f6" />
                </div>
                <div className="metric-chip-info">
                  <span className="metric-chip-label">Humidity</span>
                  <span className="metric-chip-val">{currentHumidity}%</span>
                </div>
              </div>

              <div className="metric-chip">
                <div className="metric-chip-icon">
                  <Wind size={14} color="#059669" />
                </div>
                <div className="metric-chip-info">
                  <span className="metric-chip-label">Wind</span>
                  <span className="metric-chip-val">{currentWind} km/h</span>
                </div>
              </div>

              <div className="metric-chip">
                <div className="metric-chip-icon">
                  <CloudRain size={14} color="#6366f1" />
                </div>
                <div className="metric-chip-info">
                  <span className="metric-chip-label">Rain</span>
                  <span className="metric-chip-val">{currentRain}</span>
                </div>
              </div>
            </div>

            {/* 4-Day Mini Forecast */}
            <div className="mini-forecast-grid">
              {miniForecast.map((d, i) => (
                <div key={i} className="mini-forecast-item">
                  <div className="mini-day-label">{d.day}</div>
                  <div className="mini-day-temp">{d.max}° / {d.min}°</div>
                  <div className="mini-day-icon">
                    {d.cond.includes('Rain') ? (
                      <CloudRain size={18} color="#3b82f6" />
                    ) : d.cond.includes('Cloud') ? (
                      <CloudSun size={18} color="#64748b" />
                    ) : (
                      <Sun size={18} color="#f59e0b" />
                    )}
                  </div>
                  <div className="mini-day-cond">{d.cond}</div>
                </div>
              ))}
            </div>
          </div>

          {/* 🤖 AI Recommendation Card */}
          <Link to="/chat" className="sidebar-card ai-recommendation-card">
            <div className="ai-rec-header">
              <div className="ai-bot-circle">
                <Bot size={20} color="#7c3aed" />
              </div>
              <span className="ai-rec-title">AI Recommendation</span>
              <ArrowRight size={16} className="ai-rec-arrow" />
            </div>

            <div className="ai-rec-body">
              <Sprout size={18} color="#7c3aed" className="ai-rec-leaf" />
              <p className="ai-rec-text">{aiRecommendation}</p>
            </div>
          </Link>

          {/* 👤 Farmer Profile Card */}
          <div className="sidebar-card farmer-profile-card">
            <div className="farmer-profile-top">
              <img
                src="/assets/farmer-avatar.jpg"
                alt="Farmer avatar"
                className="farmer-card-avatar"
              />
              <div className="farmer-card-details">
                <div className="farmer-card-name">
                  {user?.full_name || 'Farmer'}
                </div>
                <div className="farmer-card-location">
                  <MapPin size={13} color="#15803d" /> {locationName}
                </div>
              </div>
            </div>

            <Link to="/profile" className="btn-view-profile">
              View Profile <ArrowRight size={14} />
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
