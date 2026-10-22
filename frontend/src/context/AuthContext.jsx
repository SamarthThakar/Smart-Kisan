import React, { createContext, useContext, useState, useEffect } from 'react';
import { api } from '../services/api';
import toast from 'react-hot-toast';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [profile, setProfile] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('smart_kisan_token'));
  const [loading, setLoading] = useState(true);
  const [isGuest, setIsGuest] = useState(false);

  useEffect(() => {
    const initializeAuth = async () => {
      if (token) {
        try {
          const res = await api.getMe();
          setUser(res.user);
          setProfile(res.profile);
          setIsGuest(false);
        } catch (err) {
          console.warn('Session expired or invalid, continuing as guest/demo', err);
          localStorage.removeItem('smart_kisan_token');
          setToken(null);
          // Default guest demo farmer
          setUser({
            id: 'guest-farmer-01',
            full_name: 'Kisan Mitra (Demo)',
            phone: '9876543210',
            preferred_language: 'en',
          });
          setIsGuest(true);
        }
      } else {
        // Default to guest mode so farmers can immediately explore without hard roadblocks
        setUser({
          id: 'guest-farmer-01',
          full_name: 'Kisan Mitra (Demo)',
          phone: '9876543210',
          preferred_language: 'en',
        });
        setIsGuest(true);
      }
      setLoading(false);
    };

    initializeAuth();
  }, [token]);

  const login = async (phone, password) => {
    try {
      const res = await api.login(phone, password);
      localStorage.setItem('smart_kisan_token', res.access_token);
      setToken(res.access_token);
      setUser(res.user);
      setIsGuest(false);
      toast.success(`Welcome back, ${res.user.full_name}!`);
      return true;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Invalid phone or password';
      toast.error(errorMsg);
      return false;
    }
  };

  const register = async (phone, fullName, preferredLanguage, password) => {
    try {
      const res = await api.register(phone, fullName, preferredLanguage, password);
      localStorage.setItem('smart_kisan_token', res.access_token);
      setToken(res.access_token);
      setUser(res.user);
      setIsGuest(false);
      toast.success(`Welcome to Smart Kisan, ${res.user.full_name}!`);
      return true;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Registration failed. Please check phone number.';
      toast.error(errorMsg);
      return false;
    }
  };

  const logout = () => {
    localStorage.removeItem('smart_kisan_token');
    setToken(null);
    setUser({
      id: 'guest-farmer-01',
      full_name: 'Kisan Mitra (Demo)',
      phone: '9876543210',
      preferred_language: 'en',
    });
    setIsGuest(true);
    toast.success('Logged out successfully');
  };

  const updateProfile = async (profileData) => {
    try {
      await api.updateProfile(profileData);
      setProfile((prev) => ({ ...prev, ...profileData }));
      toast.success('Farmer profile updated!');
      return true;
    } catch (err) {
      toast.error('Failed to update profile');
      return false;
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        profile,
        token,
        loading,
        isGuest,
        login,
        register,
        logout,
        updateProfile,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
