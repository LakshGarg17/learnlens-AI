import React, { useState } from 'react';
import { FileText, MessageSquareQuote, BrainCircuit, Layers, Info, X } from 'lucide-react';

export default function ActionButtons() {
  const [activeNotification, setActiveNotification] = useState(null);

  const actions = [
    {
      id: 'summarize',
      label: 'Summarize',
      icon: FileText,
      description: 'Condense documents & key points',
      todo: 'Day 2 - wire up summarization logic here',
      message: 'Feature coming soon: AI Document & Topic Summarization',
    },
    {
      id: 'ask',
      label: 'Ask Question',
      icon: MessageSquareQuote,
      description: 'Ask deep questions about your notes',
      todo: 'Day 2 - wire up Q&A and interactive chat logic here',
      message: 'Feature coming soon: Interactive AI Q&A Assistant',
    },
    {
      id: 'quiz',
      label: 'Generate Quiz',
      icon: BrainCircuit,
      description: 'Test your understanding with AI quizzes',
      todo: 'Day 3 - wire up quiz generation and scoring here',
      message: 'Feature coming soon: AI Knowledge Checks & Quizzes',
    },
    {
      id: 'flashcards',
      label: 'Flashcards',
      icon: Layers,
      description: 'Spaced repetition flashcards',
      todo: 'Day 3 - wire up flashcard generator here',
      message: 'Feature coming soon: Interactive Study Flashcards',
    },
  ];

  const handleActionClick = (action) => {
    // Placeholder feedback for Day 1
    setActiveNotification({
      title: action.label,
      message: action.message,
      id: action.id,
    });
  };

  return (
    <section className="section-card actions-section">
      <div className="section-header">
        <h2 className="section-title">What would you like to do?</h2>
        <p className="section-description">
          Select an AI learning tool below to process your study material.
        </p>
      </div>

      <div className="action-buttons-grid">
        {actions.map((action) => {
          const Icon = action.icon;
          return (
            <button
              key={action.id}
              className={`action-btn action-${action.id}`}
              onClick={() => handleActionClick(action)}
            >
              <div className="action-icon-wrapper">
                <Icon size={24} />
              </div>
              <div className="action-btn-text">
                <span className="action-title">{action.label}</span>
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
