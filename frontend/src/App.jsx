import React from 'react';
import Header from './components/Header';
import StatusBanner from './components/StatusBanner';
import UploadSection from './components/UploadSection';
import ActionButtons from './components/ActionButtons';
import './App.css';

function App() {
  return (
    <div className="app-layout">
      <div className="app-container">
        {/* Top Header */}
        <Header />

        {/* Backend & AI Connection Status */}
        <StatusBanner />

        {/* Section 1: Upload Study Material */}
        <UploadSection />

        {/* Horizontal Divider */}
        <div className="app-divider" />

        {/* Section 2: Action Buttons & Coming Soon Placeholders */}
        <ActionButtons />

        {/* Footer info */}
        <footer className="app-footer">
          <p>LearnLens AI • Day 1 Setup &amp; Architecture</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
