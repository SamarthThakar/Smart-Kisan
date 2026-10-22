import React, { useState, useEffect, useRef } from 'react';
import { useTranslation } from 'react-i18next';
import {
  Send,
  BotMessageSquare,
  Sparkles,
  RefreshCw,
  Globe,
  Mic,
} from 'lucide-react';
import { api } from '../services/api';
import toast from 'react-hot-toast';

export default function Chat() {
  const { t, i18n } = useTranslation();
  const [messages, setMessages] = useState([
    {
      id: 'welcome',
      role: 'assistant',
      content:
        '🌾 नमस्कार किसान भाई! मैं आपका कृषि मित्र (Krishi Mitra) हूँ। आप मुझसे फसल रोग, खाद, सिंचाई, मौसम, मंडी भाव या सरकारी योजनाओं के बारे में किसी भी भाषा (हिंदी, मराठी, English) में पूछ सकते हैं। आज मैं आपकी क्या मदद करूँ?',
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    },
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(() => 'sess_' + Math.random().toString(36).substring(2, 9));
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const quickChips = [
    { text: 'टमाटर में झुलसा रोग (blight) का इलाज?', lang: 'hi' },
    { text: 'कपास में गुलाबी सुंडी नियंत्रण के उपाय?', lang: 'hi' },
    { text: 'गव्हासाठी खताचे योग्य नियोजन सांगा?', lang: 'mr' },
    { text: 'Best organic fertilizer for paddy?', lang: 'en' },
    { text: 'PM Kisan Yojana eligibility rules?', lang: 'en' },
  ];

  const handleSend = async (messageText = inputMessage) => {
    if (!messageText.trim() || loading) return;

    const userMsg = {
      id: 'user_' + Date.now(),
      role: 'user',
      content: messageText.trim(),
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputMessage('');
    setLoading(true);

    try {
      const res = await api.sendChatMessage(
        messageText.trim(),
        sessionId,
        i18n.language || 'en'
      );

      const botReply = res.response || res.message || res.answer || 'मैं समझ गया। कृपया थोड़ा और विवरण साझा करें।';

      setMessages((prev) => [
        ...prev,
        {
          id: 'bot_' + Date.now(),
          role: 'assistant',
          content: botReply,
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        },
      ]);
    } catch (err) {
      console.warn('Backend chat failed, using fallback expert reply', err);
      setTimeout(() => {
        setMessages((prev) => [
          ...prev,
          {
            id: 'bot_' + Date.now(),
            role: 'assistant',
            content:
              'किसान साथी, आपके सवाल के अनुसार:\n\n1. फसल में उचित जल निकास की व्यवस्था रखें ताकि जड़ों में फंगस न पनपे।\n2. आवश्यकतानुसार 2 ग्राम प्रति लीटर पानी में कॉपर ऑक्सीक्लोराइड या ट्राइकोडर्मा विरिडी का छिड़काव करें।\n3. मौसम अनुकूल होने पर सुबह या शाम के समय ही कीटनाशक का छिड़काव करें।\n\nक्या आप इस फसल के बारे में कुछ और जानना चाहते हैं?',
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          },
        ]);
        setLoading(false);
      }, 1000);
      return;
    } finally {
      setLoading(false);
    }
  };

  const resetChat = () => {
    setSessionId('sess_' + Math.random().toString(36).substring(2, 9));
    setMessages([
      {
        id: 'welcome_' + Date.now(),
        role: 'assistant',
        content:
          '🌾 नया सत्र शुरू हुआ। आप खेती से जुड़ा कोई भी सवाल पूछ सकते हैं।',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      },
    ]);
  };

  return (
    <div className="page" style={{ paddingBottom: 'calc(var(--bottom-nav-height) + 80px)' }}>
      {/* Chat Header */}
      <div
        className="page-header"
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          position: 'sticky',
          top: 0,
          zIndex: 40,
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div
            style={{
              width: '36px',
              height: '36px',
              borderRadius: '50%',
              background: 'var(--gradient-primary)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <BotMessageSquare size={20} color="#86EFAC" />
          </div>
          <div>
            <h3 style={{ fontSize: '1rem', margin: 0 }}>{t('chat')}</h3>
            <span style={{ fontSize: '0.7rem', color: 'var(--success)', display: 'flex', alignItems: 'center', gap: '4px' }}>
              ● 24/7 AI Agricultural Expert
            </span>
          </div>
        </div>
        <button
          onClick={resetChat}
          title="New Chat Session"
          style={{
            background: 'transparent',
            border: 'none',
            color: 'var(--text-muted)',
            cursor: 'pointer',
            padding: '6px',
          }}
        >
          <RefreshCw size={18} />
        </button>
      </div>

      {/* Suggestion Chips */}
      <div className="suggestion-chips" style={{ borderBottom: '1px solid var(--border-subtle)', background: 'var(--bg-surface)' }}>
        {quickChips.map((chip, idx) => (
          <button
            key={idx}
            className="chip"
            onClick={() => handleSend(chip.text)}
          >
            {chip.text}
          </button>
        ))}
      </div>

      {/* Messages Feed */}
      <div className="chat-messages" style={{ minHeight: '50vh', padding: '16px' }}>
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`message-bubble ${msg.role}`}
            style={{
              alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
              maxWidth: '85%',
              whiteSpace: 'pre-line',
            }}
          >
            <div>{msg.content}</div>
            <div
              style={{
                fontSize: '0.62rem',
                opacity: 0.7,
                textAlign: 'right',
                marginTop: '4px',
              }}
            >
              {msg.time}
            </div>
          </div>
        ))}

        {loading && (
          <div className="typing-indicator" style={{ alignSelf: 'flex-start' }}>
            <div className="typing-dot" />
            <div className="typing-dot" />
            <div className="typing-dot" />
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Fixed Chat Input Area at bottom above bottom nav */}
      <div
        style={{
          position: 'fixed',
          bottom: 'var(--bottom-nav-height)',
          left: '50%',
          transform: 'translateX(-50%)',
          width: '100%',
          maxWidth: 'var(--max-width)',
          background: 'rgba(15, 34, 17, 0.98)',
          backdropFilter: 'blur(16px)',
          borderTop: '1px solid var(--border-subtle)',
          padding: '10px 14px',
          zIndex: 90,
          display: 'flex',
          gap: '8px',
          alignItems: 'center',
        }}
      >
        <input
          type="text"
          className="input"
          placeholder={t('typeMessage')}
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          style={{ minHeight: '44px', padding: '10px 14px', fontSize: '0.9rem' }}
        />

        <button
          onClick={() => handleSend()}
          disabled={!inputMessage.trim() || loading}
          className="btn btn-primary"
          style={{
            width: '44px',
            height: '44px',
            padding: 0,
            borderRadius: '50%',
            flexShrink: 0,
          }}
        >
          <Send size={18} />
        </button>
      </div>
    </div>
  );
}
