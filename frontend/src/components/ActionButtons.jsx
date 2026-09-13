import React, { useState } from 'react';
import { FileText, MessageSquareQuote, Lightbulb, BrainCircuit, Layers, Info, X, Sparkles } from 'lucide-react';

export default function ActionButtons({ activeFeature, onSelectFeature, hasDocument }) {
  const [activeNotification, setActiveNotification] = useState(null);

  const actions = [
    {
      id: 'summarize',
      label: 'AI Summary',
      icon: FileText,
      description: 'Condense documents & key exam points',
      isLive: true,
    },
    {
      id: 'ask',
      label: 'Ask AI',
      icon: MessageSquareQuote,
      description: 'Ask deep questions grounded in your notes',
      isLive: true,
    },
    {
      id: 'explain',
      label: 'Explain Simply',
      icon: Lightbulb,
      description: 'Beginner-friendly breakdown with analogies',
      isLive: true,
    },
    {
      id: 'quiz',
      label: 'Generate Quiz',
      icon: BrainCircuit,
      description: 'Test your understanding with AI quizzes',
      isLive: false,
      message: 'Feature coming in Day 4: AI Knowledge Checks & Quizzes',
    },
    {
      id: 'flashcards',
      label: 'Flashcards',
      icon: Layers,
      description: 'Spaced repetition flashcards',
      isLive: false,
      message: 'Feature coming in Day 5: Interactive Study Flashcards',
    },
  ];

  const handleActionClick = (action) => {
    if (action.isLive) {
      if (onSelectFeature) {
        onSelectFeature(action.id);
      }
      if (!hasDocument) {
        setActiveNotification({
          title: action.label,
          message: 'Upload a study PDF above to extract content and run this AI tool.',
          id: action.id,
        });
      } else {
        setActiveNotification(null);
      }
    } else {
      setActiveNotification({
        title: action.label,
        message: action.message,
        id: action.id,
      });
    }
  };


  return (
    <section className="section-card actions-section">
      <div className="section-header">
        <h2 className="section-title">⚡ AI Learning Workspace</h2>
        <p className="section-description">
          Select an AI learning tool below to process your study material.
        </p>
      </div>

      <div className="action-buttons-grid">
        {actions.map((action) => {
          const Icon = action.icon;
          const isActive = activeFeature === action.id;

          return (
            <button
              key={action.id}
              className={`action-btn action-${action.id} ${isActive ? 'active-feature-tab' : ''}`}
              onClick={() => handleActionClick(action)}
            >
              <div className="action-icon-wrapper">
                <Icon size={24} />
              </div>
              <div className="action-btn-text">
                <div className="action-title-row">
                  <span className="action-title">{action.label}</span>
                  {action.isLive ? (
                    <span className="badge-live-pill">
                      <Sparkles size={10} /> Live
                    </span>
                  ) : (
                    <span className="badge-soon-pill">Soon</span>
                  )}
                </div>
                <span className="action-desc">{action.description}</span>
              </div>
            </button>
          );
        })}
      </div>

      {activeNotification && (
        <div className="notification-box">
          <div className="notification-content">
            <Info size={20} className="info-icon" />
            <div className="notification-text">
              <strong>{activeNotification.title}:</strong> {activeNotification.message}
            </div>
          </div>
          <button
            className="notification-close"
            onClick={() => setActiveNotification(null)}
            aria-label="Close notification"
          >
            <X size={16} />
          </button>
        </div>
      )}
    </section>
  );
}

