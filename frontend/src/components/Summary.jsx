import React, { useState } from 'react';
import axios from 'axios';
import { Sparkles, Copy, Check, RefreshCw, AlertCircle, FileText, ChevronRight } from 'lucide-react';

const API_BASE = 'http://localhost:8000';

export default function Summary({ fullText, filename }) {
  const [summary, setSummary] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [copied, setCopied] = useState(false);

  const handleGenerateSummary = async () => {
    if (!fullText || !fullText.trim()) {
      setError('Please upload a study material PDF before generating a summary.');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await axios.post(
        `${API_BASE}/api/summarize`,
        { text: fullText },
        { headers: { 'Content-Type': 'application/json' }, timeout: 60000 }
      );

      if (response.data && response.data.summary) {
        setSummary(response.data.summary);
      } else {
        setError('Received an empty summary response. Please try again.');
      }
    } catch (err) {
      const backendError =
        err.response?.data?.detail ||
        err.response?.data?.message ||
        'Unable to generate the summary. Please check backend and try again.';
      setError(backendError);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCopy = () => {
    if (!summary) return;
    if (navigator.clipboard) {
      navigator.clipboard.writeText(summary);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  // Helper to format markdown headings and bullet lines cleanly
  const renderFormattedSummary = (raw) => {
    const lines = raw.split('\n');
    return lines.map((line, index) => {
      const trimmed = line.trim();
      if (!trimmed) {
        return <div key={index} className="summary-spacer" />;
      }
      if (trimmed.startsWith('### ')) {
        return <h4 key={index} className="summary-h4">{trimmed.replace('### ', '')}</h4>;
      }
      if (trimmed.startsWith('## ')) {
        return <h3 key={index} className="summary-h3">{trimmed.replace('## ', '')}</h3>;
      }
      if (trimmed.startsWith('# ')) {
        return <h2 key={index} className="summary-h2">{trimmed.replace('# ', '')}</h2>;
      }
      if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
        const content = trimmed.slice(2);
        return (
          <li key={index} className="summary-bullet">
            <ChevronRight size={14} className="bullet-icon" />
            <span>{renderBoldSpans(content)}</span>
          </li>
        );
      }
      return <p key={index} className="summary-paragraph">{renderBoldSpans(trimmed)}</p>;
    });
  };

  const renderBoldSpans = (text) => {
    const parts = text.split(/(\*\*.*?\*\*)/g);
    return parts.map((part, i) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return <strong key={i} className="summary-highlight">{part.slice(2, -2)}</strong>;
      }
      return part;
    });
  };

  return (
    <section className="section-card ai-feature-card" id="summary-section">
      <div className="section-header ai-header-row">
        <div>
          <div className="feature-tag summary-tag">
            <Sparkles size={14} /> AI Study Summary
          </div>
          <h2 className="section-title">Comprehensive Key Point Summary</h2>
          <p className="section-description">
            Exam-focused, grounded breakdown of essential concepts from{' '}
            <strong>{filename || 'your uploaded notes'}</strong>.
          </p>
        </div>

        <div className="ai-actions-row">
          {summary && (
            <button
              className="btn-secondary-action"
              onClick={handleCopy}
              title="Copy summary to clipboard"
            >
              {copied ? <Check size={16} /> : <Copy size={16} />}
              <span>{copied ? 'Copied!' : 'Copy'}</span>
            </button>
          )}

          <button
            className="btn-primary-action"
            onClick={handleGenerateSummary}
            disabled={isLoading || !fullText}
          >
            {isLoading ? (
              <>
                <RefreshCw size={16} className="spin" />
                <span>Generating summary...</span>
              </>
            ) : summary ? (
              <>
                <RefreshCw size={16} />
                <span>Regenerate</span>
              </>
            ) : (
              <>
                <Sparkles size={16} />
                <span>Generate Summary</span>
              </>
            )}
          </button>
        </div>
      </div>

      {error && (
        <div className="feature-error-alert" role="alert">
          <AlertCircle size={18} className="error-icon" />
          <div className="error-text">
            <strong>Error:</strong> {error}
          </div>
        </div>
      )}

      {isLoading && (
        <div className="ai-loading-container">
          <div className="ai-pulse-orb" />
          <p className="loading-title">Generating summary...</p>
          <p className="loading-subtitle">
            Analyzing document structure and extracting high-yield exam takeaways...
          </p>
        </div>
      )}

      {!isLoading && !summary && !error && (
        <div className="feature-placeholder-box">
          <FileText size={36} className="placeholder-icon" />
          <p className="placeholder-title">Ready to summarize</p>
          <p className="placeholder-subtitle">
            {fullText
              ? 'Click "Generate Summary" above to create an exam-ready breakdown of this document.'
              : 'Upload a study PDF above to unlock instant AI summarization.'}
          </p>
        </div>
      )}

      {!isLoading && summary && (
        <div className="summary-content-display">
          <ul className="summary-list">
            {renderFormattedSummary(summary)}
          </ul>
        </div>
      )}
    </section>
  );
}
