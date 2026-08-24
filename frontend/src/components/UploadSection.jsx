import React, { useState } from 'react';
import { UploadCloud, FileText, Search, Check, AlertCircle } from 'lucide-react';

export default function UploadSection() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [topic, setTopic] = useState('');

  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      if (file.type === 'application/pdf' || file.name.endsWith('.pdf')) {
        setSelectedFile(file);
        // TODO: Day 2 - handle PDF upload and extraction via FastAPI backend
      } else {
        alert('Please select a valid PDF file.');
      }
    }
  };

  const handleTopicChange = (e) => {
    setTopic(e.target.value);
    // TODO: Day 2 - prepare prompt context for manual topic input
  };

  return (
    <section className="section-card upload-section">
      <div className="section-header">
        <h2 className="section-title">📚 Upload Study Material</h2>
        <p className="section-description">
          Choose between uploading a PDF document or entering a specific topic to study.
        </p>
      </div>

      <div className="upload-grid">
        {/* Option 1: PDF File Uploader */}
        <div className={`upload-box ${selectedFile ? 'has-file' : ''}`}>
          <div className="upload-box-header">
            <UploadCloud size={24} className="box-icon" />
            <h3 className="box-title">Upload PDF Document</h3>
          </div>
          
          <label className="file-drop-area" htmlFor="pdf-upload">
            <input
              id="pdf-upload"
              type="file"
              accept=".pdf"
              onChange={handleFileChange}
              className="file-input-hidden"
            />
            {selectedFile ? (
              <div className="file-info-preview">
                <FileText size={28} className="text-accent" />
                <div className="file-details">
                  <span className="file-name">{selectedFile.name}</span>
                  <span className="file-size">{(selectedFile.size / 1024).toFixed(1)} KB</span>
                </div>
                <span className="badge-ready">Ready</span>
              </div>
            ) : (
              <div className="upload-placeholder">
                <FileText size={32} className="placeholder-icon" />
                <span className="primary-prompt">Click to browse or drop PDF here</span>
                <span className="secondary-prompt">Supports .pdf files up to 25MB</span>
              </div>
            )}
          </label>
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
