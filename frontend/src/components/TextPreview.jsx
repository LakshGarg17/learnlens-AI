import React, { useState } from 'react';
import { FileText, BookOpen, Copy, Check, Hash, Sparkles } from 'lucide-react';

export default function TextPreview({ documentData }) {
  const [copied, setCopied] = useState(false);

  if (!documentData) {
    return (
      <section className="section-card preview-section empty-state">
        <div className="empty-preview-content">
          <div className="empty-icon-box">
            <BookOpen size={28} className="empty-icon" />
          </div>
          <h3 className="empty-title">Document Text Preview</h3>
          <p className="empty-subtitle">
            Upload a PDF document above to extract and inspect its contents here before generating summaries, quizzes, or flashcards.
          </p>
        </div>
      </section>
    );
  }

  const { filename, page_count, preview, full_text } = documentData;
  const charCount = full_text ? full_text.length : (preview ? preview.length : 0);
  const wordCount = full_text
    ? full_text.trim().split(/\s+/).filter(Boolean).length
    : (preview ? preview.trim().split(/\s+/).filter(Boolean).length : 0);

  const handleCopy = () => {
    const textToCopy = preview || full_text || '';
    if (navigator.clipboard) {
      navigator.clipboard.writeText(textToCopy);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <section className="section-card preview-section">
      {/* Section Header */}
      <div className="section-header preview-header-row">
        <div>
          <div className="preview-badge-row">
            <span className="live-badge">
              <Sparkles size={13} /> Extracted Document
            </span>
          </div>
          <h2 className="section-title">📄 Extracted Text Preview</h2>
          <p className="section-description">
            Content parsed from your PDF, ready for AI learning tools.
          </p>
        </div>

        <button
          className="btn-copy-preview"
          onClick={handleCopy}
          title="Copy preview text"
        >
          {copied ? <Check size={15} /> : <Copy size={15} />}
          <span>{copied ? 'Copied!' : 'Copy Preview'}</span>
        </button>
      </div>

      {/* Metadata Bar */}
      <div className="document-meta-bar">
        <div className="meta-item">
          <FileText size={16} className="meta-icon" />
          <span className="meta-label">Filename:</span>
          <span className="meta-value filename-val" title={filename}>{filename}</span>
        </div>

        <div className="meta-divider" />

        <div className="meta-item">
          <BookOpen size={16} className="meta-icon" />
          <span className="meta-label">Pages:</span>
          <span className="meta-value">{page_count} {page_count === 1 ? 'page' : 'pages'}</span>
        </div>

        <div className="meta-divider" />

        <div className="meta-item">
          <Hash size={16} className="meta-icon" />
          <span className="meta-label">Length:</span>
          <span className="meta-value">{wordCount.toLocaleString()} words ({charCount.toLocaleString()} chars)</span>
        </div>
      </div>

      {/* Preview Content Box */}
      <div className="preview-box">
        <div className="preview-box-header">
          <span className="preview-tag">Text Snippet (First ~500 chars)</span>
          <span className="preview-status-pill">Ready for Day 3 AI Processing</span>
        </div>
        <div className="preview-text-container" tabIndex={0}>
          <pre className="preview-pre">{preview || 'No preview available.'}</pre>
        </div>
      </div>
    </section>
  );
}
