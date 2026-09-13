import React, { useState } from 'react';
import Header from './components/Header';
import StatusBanner from './components/StatusBanner';
import UploadSection from './components/UploadSection';
import TextPreview from './components/TextPreview';
import ActionButtons from './components/ActionButtons';
import Summary from './components/Summary';
import AskAI from './components/AskAI';
import ExplainTopic from './components/ExplainTopic';
import './App.css';

function App() {
  const [documentData, setDocumentData] = useState(null);
  const [activeFeature, setActiveFeature] = useState('summary');

  const handleUploadSuccess = (data) => {
    setDocumentData(data);
    // Keep active feature on summary when new PDF is uploaded
    if (!activeFeature) {
      setActiveFeature('summary');
    }
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

        {/* Section 3: AI Learning Tools Hub */}
        <ActionButtons
          activeFeature={activeFeature}
          onSelectFeature={setActiveFeature}
          hasDocument={Boolean(documentData?.full_text)}
        />

        {/* Section 4: Active AI Tool Component */}
        <div className="active-ai-container">
          {activeFeature === 'summary' && (
            <Summary
              fullText={documentData?.full_text}
              filename={documentData?.filename}
            />
          )}

          {activeFeature === 'ask' && (
            <AskAI
              fullText={documentData?.full_text}
              filename={documentData?.filename}
            />
          )}

          {activeFeature === 'explain' && (
            <ExplainTopic
              fullText={documentData?.full_text}
              filename={documentData?.filename}
            />
          )}
        </div>

        {/* Footer info */}
        <footer className="app-footer">
          <p>LearnLens AI • Day 3: Intelligent AI Study Assistant (Summary, Q&amp;A, Simplifier)</p>
        </footer>
      </div>
    </div>
  );
}

export default App;

