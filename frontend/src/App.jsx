import React, { useState } from 'react';
import Header from './components/Header';
import StatusBanner from './components/StatusBanner';
import UploadSection from './components/UploadSection';
import TextPreview from './components/TextPreview';
import ActionButtons from './components/ActionButtons';
import './App.css';

function App() {
  const [documentData, setDocumentData] = useState(null);

  const handleUploadSuccess = (data) => {
    setDocumentData(data);
  };

  return (
    <div className="app-layout">
      <div className="app-container">
        {/* Top Header */}
        <Header />

        {/* Backend & AI Connection Status */}
        <StatusBanner />

        {/* Section 1: Upload Study Material (PDF & Topic) */}
        <UploadSection onUploadSuccess={handleUploadSuccess} />

        {/* Section 2: Extracted Text Preview */}
        <TextPreview documentData={documentData} />

        {/* Horizontal Divider */}
        <div className="app-divider" />

        {/* Section 3: Action Buttons & Coming Soon Placeholders */}
        {/* TODO: Day 3 - enable action buttons once full_text is available */}
        <ActionButtons />

        {/* Footer info */}
        <footer className="app-footer">
          <p>LearnLens AI • Day 2: PDF Upload &amp; Text Extraction</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
