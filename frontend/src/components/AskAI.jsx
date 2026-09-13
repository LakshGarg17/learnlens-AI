import React, { useState } from 'react';
import axios from 'axios';
import { MessageSquareQuote, Send, Loader2, AlertCircle, Copy, Check, Sparkles, HelpCircle, ShieldCheck } from 'lucide-react';

const API_BASE = 'http://localhost:8000';

const SUGGESTIONS = [
  'What are the core concepts covered in this document?',
  'Explain the main definitions with examples.',
  'What key questions might appear on an exam about this topic?',
];

export default function AskAI({ fullText, filename }) {
  const [question, setQuestion] = useState('');
  const [qaHistory, setQaHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [copiedIndex, setCopiedIndex] = useState(null);

  const handleAsk = async (queryToAsk) => {
    const activeQuestion = (queryToAsk !== undefined ? queryToAsk : question).trim();

    if (!fullText || !fullText.trim()) {
      setError('Please upload a study material PDF before asking questions.');
      return;
    }
    if (!activeQuestion) {
      setError('Please enter a question to ask.');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await axios.post(
        `${API_BASE}/api/ask`,
        { text: fullText, question: activeQuestion },
        { headers: { 'Content-Type': 'application/json' }, timeout: 60000 }
      );

      const answer = response.data?.answer || "No response received.";
      const isGroundedNotice = answer.includes("couldn't find this information in the uploaded study material");

      setQaHistory((prev) => [
        {
          question: activeQuestion,
          answer,
          isGroundedNotice,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        },
        ...prev,
      ]);
      setQuestion('');
    } catch (err) {
      const backendError =
        err.response?.data?.detail ||
        err.response?.data?.message ||
        'Unable to answer your question. Please check backend and try again.';
      setError(backendError);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (!isLoading) {
        handleAsk();
      }
    }
  };

  const handleCopy = (text, index) => {
    if (navigator.clipboard) {
      navigator.clipboard.writeText(text);
      setCopiedIndex(index);
      setTimeout(() => setCopiedIndex(null), 2000);
    }
  };

  return (
    <section className="section-card ai-feature-card" id="ask-ai-section">
      <div className="section-header">
        <div className="feature-tag ask-tag">
          <MessageSquareQuote size={14} /> Ask AI • Question &amp; Answer
        </div>
        <h2 className="section-title">Contextual Study Q&amp;A</h2>
        <p className="section-description">
          Ask questions answered strictly from <strong>{filename || 'your uploaded notes'}</strong> with zero hallucinations.
        </p>
      </div>

      {/* Input Box */}
      <div className="ask-input-box-wrapper">
        <div className="ask-input-container">
          <input
            type="text"
            className="ask-text-input"
            placeholder={
              fullText
                ? 'Ask anything about your notes (e.g., "What is supervised learning?")...'
                : 'Upload a PDF above to enable AI questions...'
            }
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={isLoading || !fullText}
          />
          <button
            className="btn-send-question"
            onClick={() => handleAsk()}
            disabled={isLoading || !question.trim() || !fullText}
            title="Ask AI"
          >
            {isLoading ? (
              <Loader2 size={18} className="spin" />
            ) : (
              <>
                <Send size={16} />
                <span>Ask</span>
              </>
            )}
          </button>
        </div>

        {/* Suggestion pills */}
        {fullText && (
          <div className="suggestions-bar">
            <span className="suggestions-label">
              <Sparkles size={12} /> Suggested:
            </span>
            <div className="suggestions-list">
              {SUGGESTIONS.map((item, idx) => (
                <button
                  key={idx}
                  className="suggestion-pill"
                  onClick={() => {
                    setQuestion(item);
                    handleAsk(item);
                  }}
                  disabled={isLoading}
                >
                  {item}
                </button>
              ))}
            </div>
          </div>
        )}
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
          <p className="loading-title">Thinking...</p>
          <p className="loading-subtitle">
            Scanning study material for relevant concepts and facts...
          </p>
        </div>
      )}

      {/* Grounded QA History Feed */}
      <div className="qa-history-feed">
        {qaHistory.length === 0 && !isLoading && (
          <div className="feature-placeholder-box">
            <HelpCircle size={36} className="placeholder-icon" />
            <p className="placeholder-title">No questions asked yet</p>
            <p className="placeholder-subtitle">
              Type a question above or click a suggestion to test your knowledge against the study guide.
            </p>
          </div>
        )}

        {qaHistory.map((item, idx) => (
          <div key={idx} className="qa-item-card">
            <div className="qa-question-header">
              <span className="qa-role-badge student-badge">You</span>
              <p className="qa-question-text">{item.question}</p>
              <span className="qa-time">{item.timestamp}</span>
            </div>

            <div className={`qa-answer-container ${item.isGroundedNotice ? 'unfound-notice' : ''}`}>
              <div className="qa-answer-header">
                <div className="qa-role-wrapper">
                  <span className="qa-role-badge ai-badge">LearnLens AI</span>
                  {item.isGroundedNotice ? (
                    <span className="grounding-pill warning">Not In Material</span>
                  ) : (
                    <span className="grounding-pill verified">
                      <ShieldCheck size={12} /> Grounded in Notes
                    </span>
                  )}
                </div>
                <button
                  className="btn-copy-small"
                  onClick={() => handleCopy(item.answer, idx)}
                  title="Copy answer"
                >
                  {copiedIndex === idx ? <Check size={14} /> : <Copy size={14} />}
                  <span>{copiedIndex === idx ? 'Copied' : 'Copy'}</span>
                </button>
              </div>

              <div className="qa-answer-body">
                {item.answer.split('\n').map((line, pIdx) => (
                  <p key={pIdx} className="qa-p">
                    {line}
                  </p>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
