import React from 'react';
import { BookOpen, Sparkles } from 'lucide-react';

export default function Header() {
  return (
    <header className="app-header">
      <div className="header-badge">
        <Sparkles size={14} className="sparkle-icon" />
        <span>Day 1 • Architecture &amp; UI Shell</span>
      </div>
      
      <div className="header-title-container">
        <div className="header-icon-box">
          <BookOpen size={32} className="header-icon" />
        </div>
        <h1 className="header-title">AI Study Assistant</h1>
      </div>
      
      <p className="header-subtitle">
        Your intelligent study companion for synthesizing documents, generating quizzes, and mastering complex topics.
      </p>
    </header>
  );
}
