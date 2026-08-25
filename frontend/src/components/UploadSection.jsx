import React, { useState } from 'react';
import { UploadCloud, Search, Check } from 'lucide-react';
import FileUpload from './FileUpload';

export default function UploadSection({ onUploadSuccess }) {
  const [topic, setTopic] = useState('');

  const handleTopicChange = (e) => {
    setTopic(e.target.value);
    // TODO: Day 3 - prepare prompt context for manual topic input
  };

  return (
    <section className="section-card upload-section">
      <div className="section-header">
        <h2 className="section-title">📚 Upload Study Material</h2>
        <p className="section-description">
          Upload a PDF document to extract its text, or enter a specific topic to study.
        </p>
      </div>

      <div className="upload-grid">
        {/* Option 1: PDF File Uploader */}
        <div className="upload-box">
          <div className="upload-box-header">
            <UploadCloud size={24} className="box-icon" />
            <h3 className="box-title">Upload PDF Document</h3>
          </div>

          <FileUpload onUploadSuccess={onUploadSuccess} />
        </div>

        {/* Option 2: Topic Input */}
        <div className="upload-box">
          <div className="upload-box-header">
            <Search size={24} className="box-icon" />
            <h3 className="box-title">Or Enter Topic Manually</h3>
          </div>

          <div className="topic-input-container">
            <input
              type="text"
              className="topic-text-input"
              placeholder="e.g. Quantum Computing, Photosynthesis, Neural Networks..."
              value={topic}
              onChange={handleTopicChange}
            />
            {topic && (
              <div className="topic-active-badge">
                <Check size={14} />
                <span>Target topic: <strong>{topic}</strong></span>
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
