import React, { useState } from 'react';
import axios from 'axios';
import { Lightbulb, Loader2, AlertCircle, Copy, Check, Compass, GraduationCap } from 'lucide-react';


const API_BASE = 'http://localhost:8000';

export default function ExplainTopic({ fullText, filename }) {
  const [topic, setTopic] = useState('');
  const [explanation, setExplanation] = useState('');
  const [explainedTopic, setExplainedTopic] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [copied, setCopied] = useState(false);

  const handleExplain = async () => {
    const activeTopic = topic.trim();

    if (!fullText || !fullText.trim()) {
      setError('Please upload a study material PDF before asking for topic explanations.');
      return;
    }
    if (!activeTopic) {
      setError('Please enter a topic or concept to explain.');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await axios.post(
        `${API_BASE}/api/explain`,
        { text: fullText, topic: activeTopic },
        { headers: { 'Content-Type': 'application/json' }, timeout: 60000 }
      );

      if (response.data && response.data.explanation) {
        setExplanation(response.data.explanation);
        setExplainedTopic(activeTopic);
      } else {
        setError('Received empty explanation. Please try again.');
      }
    } catch (err) {
      const backendError =
        err.response?.data?.detail ||
        err.response?.data?.message ||
        'Unable to generate explanation. Please check backend and try again.';
      setError(backendError);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      if (!isLoading) {
        handleExplain();
      }
    }
  };

  const handleCopy = () => {
    if (!explanation) return;
    if (navigator.clipboard) {
      navigator.clipboard.writeText(explanation);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <section className="section-card ai-feature-card" id="explain-section">
      <div className="section-header">
        <div className="feature-tag explain-tag">
          <Lightbulb size={14} /> Explain Simply
        </div>
        <h2 className="section-title">Concept Simplifier &amp; Exam Breakdown</h2>
        <p className="section-description">
          Translate complex concepts from <strong>{filename || 'your uploaded notes'}</strong> into intuitive, beginner-friendly explanations with real-world analogies.
        </p>
      </div>

      {/* Input Box */}
      <div className="explain-input-container">
        <input
          type="text"
          className="explain-text-input"
          placeholder={
            fullText
              ? 'Enter a concept to simplify (e.g. "Deadlock", "Backpropagation", "Pointers")...'
              : 'Upload a PDF above to explain concepts...'
          }
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={isLoading || !fullText}
        />
        <button
          className="btn-primary-action btn-explain"
          onClick={handleExplain}
          disabled={isLoading || !topic.trim() || !fullText}
        >
          {isLoading ? (
            <>
              <Loader2 size={16} className="spin" />
              <span>Generating explanation...</span>
            </>
          ) : (
            <>
              <Compass size={16} />
              <span>Explain Simply</span>
            </>
          )}
        </button>
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
          <p className="loading-title">Generating explanation...</p>
          <p className="loading-subtitle">
            Formulating beginner-friendly analogies and key takeaways for "{topic}"...
          </p>
        </div>
      )}

      {!isLoading && !explanation && (
        <div className="feature-placeholder-box">
          <GraduationCap size={36} className="placeholder-icon" />
          <p className="placeholder-title">No topic selected yet</p>
          <p className="placeholder-subtitle">
            Type any tricky term or theory from your notes above to get a clear, intuitive explanation.
          </p>
        </div>
      )}

      {!isLoading && explanation && (
        <div className="explanation-result-card">
          <div className="explanation-result-header">
            <div>
              <span className="concept-badge">Explained Concept</span>
              <h3 className="concept-title">{explainedTopic}</h3>
            </div>
            <button
              className="btn-copy-small"
              onClick={handleCopy}
              title="Copy explanation"
            >
              {copied ? <Check size={14} /> : <Copy size={14} />}
              <span>{copied ? 'Copied' : 'Copy'}</span>
            </button>
          </div>

          <div className="explanation-body">
            {explanation.split('\n').map((line, idx) => {
              const trimmed = line.trim();
              if (!trimmed) return <div key={idx} className="summary-spacer" />;
              if (trimmed.startsWith('#') || trimmed.match(/^[1-4]\.\s/)) {
                return <h4 key={idx} className="explanation-subhead">{trimmed}</h4>;
              }
              if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
                return (
                  <div key={idx} className="explanation-bullet">
                    <span className="bullet-dot">•</span>
                    <span>{trimmed.slice(2)}</span>
                  </div>
                );
              }
              return <p key={idx} className="explanation-p">{trimmed}</p>;
            })}
          </div>
        </div>
      )}
    </section>
  );
}
