import React, { useState } from 'react';
import axios from 'axios';
import {
  BrainCircuit,
  Sparkles,
  ChevronRight,
  ChevronLeft,
  CheckCircle2,
  XCircle,
  RotateCcw,
  PlusCircle,
  AlertCircle,
  HelpCircle,
  Award,
  Check,
} from 'lucide-react';

const API_BASE = 'http://localhost:8000';

const QUESTION_COUNTS = [5, 10, 15];
const DIFFICULTIES = [
  { id: 'easy', label: 'Easy', desc: 'Core definitions & key facts' },
  { id: 'medium', label: 'Medium', desc: 'Comprehension & concepts' },
  { id: 'hard', label: 'Hard', desc: 'Analytical & deep reasoning' },
];

export default function Quiz({ fullText, filename }) {
  // Setup state
  const [numQuestions, setNumQuestions] = useState(5);
  const [difficulty, setDifficulty] = useState('medium');

  // Quiz progression state: 'setup' | 'loading' | 'active' | 'results'
  const [quizState, setQuizState] = useState('setup');
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [studentAnswers, setStudentAnswers] = useState({}); // { [questionIndex]: optionIndex }

  // Status & error handling
  const [error, setError] = useState(null);

  // Generate quiz from backend
  const handleGenerateQuiz = async () => {
    if (!fullText || !fullText.trim()) {
      setError('Please upload a study material PDF before generating a quiz.');
      return;
    }

    setQuizState('loading');
    setError(null);

    try {
      const response = await axios.post(
        `${API_BASE}/api/generate-quiz`,
        {
          text: fullText,
          num_questions: numQuestions,
          difficulty: difficulty,
        },
        { headers: { 'Content-Type': 'application/json' }, timeout: 90000 }
      );

      if (response.data && response.data.questions && response.data.questions.length > 0) {
        setQuestions(response.data.questions);
        setStudentAnswers({});
        setCurrentIndex(0);
        setQuizState('active');
      } else {
        setError('No questions could be generated from this document. Please try again.');
        setQuizState('setup');
      }
    } catch (err) {
      const backendError =
        err.response?.data?.detail ||
        err.response?.data?.message ||
        'Unable to generate the quiz. Please check backend and try again.';
      setError(backendError);
      setQuizState('setup');
    }
  };

  // Select answer for the current question
  const handleSelectOption = (optionIndex) => {
    setStudentAnswers((prev) => ({
      ...prev,
      [currentIndex]: optionIndex,
    }));
  };

  // Advance to next question or submit
  const handleNext = () => {
    if (studentAnswers[currentIndex] === undefined) {
      return;
    }
    if (currentIndex < questions.length - 1) {
      setCurrentIndex((prev) => prev + 1);
    } else {
      setQuizState('results');
    }
  };

  const handlePrevious = () => {
    if (currentIndex > 0) {
      setCurrentIndex((prev) => prev - 1);
    }
  };

  // Retake the same quiz
  const handleRetake = () => {
    setStudentAnswers({});
    setCurrentIndex(0);
    setQuizState('active');
  };

  // Configure a new quiz
  const handleNewQuiz = () => {
    setStudentAnswers({});
    setCurrentIndex(0);
    setQuestions([]);
    setQuizState('setup');
    setError(null);
  };

  // Calculate score results
  const correctCount = questions.reduce((acc, q, idx) => {
    return studentAnswers[idx] === q.correct_answer ? acc + 1 : acc;
  }, 0);

  const scorePercentage = questions.length > 0
    ? Math.round((correctCount / questions.length) * 100)
    : 0;

  const currentQuestion = questions[currentIndex];
  const isCurrentAnswered = studentAnswers[currentIndex] !== undefined;
  const progressPercent = questions.length > 0
    ? ((currentIndex + 1) / questions.length) * 100
    : 0;

  return (
    <section className="section-card ai-feature-card" id="quiz-section">
      {/* Header */}
      <div className="section-header">
        <div className="feature-tag quiz-tag">
          <BrainCircuit size={14} /> AI Quiz System • Knowledge Check
        </div>
        <h2 className="section-title">Multiple Choice Knowledge Check</h2>
        <p className="section-description">
          Test your exam readiness with personalized MCQs generated strictly from{' '}
          <strong>{filename || 'your uploaded notes'}</strong>.
        </p>
      </div>

      {error && (
        <div className="feature-error-alert" role="alert">
          <AlertCircle size={18} className="error-icon" />
          <div className="error-text">
            <strong>Quiz Error:</strong> {error}
          </div>
        </div>
      )}

      {/* ========================================================= */}
      {/* STAGE 1: SETUP SCREEN                                     */}
      {/* ========================================================= */}
      {quizState === 'setup' && (
        <div className="quiz-setup-container">
          <div className="quiz-setup-grid">
            {/* Question count selection */}
            <div className="setup-group">
              <label className="setup-label">Number of Questions</label>
              <div className="setup-options-row">
                {QUESTION_COUNTS.map((count) => (
                  <button
                    key={count}
                    type="button"
                    className={`setup-choice-btn ${numQuestions === count ? 'active' : ''}`}
                    onClick={() => setNumQuestions(count)}
                  >
                    <span className="choice-number">{count}</span>
                    <span className="choice-unit">Questions</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Difficulty selection */}
            <div className="setup-group">
              <label className="setup-label">Difficulty Level</label>
              <div className="setup-options-row">
                {DIFFICULTIES.map((d) => (
                  <button
                    key={d.id}
                    type="button"
                    className={`setup-choice-btn ${difficulty === d.id ? 'active' : ''}`}
                    onClick={() => setDifficulty(d.id)}
                  >
                    <span className="choice-title">{d.label}</span>
                    <span className="choice-desc">{d.desc}</span>
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div className="setup-submit-row">
            <button
              type="button"
              className="btn-primary-action btn-generate-quiz"
              onClick={handleGenerateQuiz}
              disabled={!fullText}
            >
              <Sparkles size={16} />
              <span>Generate {numQuestions} Questions ({difficulty.toUpperCase()})</span>
            </button>
          </div>

          {!fullText && (
            <div className="feature-placeholder-box">
              <HelpCircle size={36} className="placeholder-icon" />
              <p className="placeholder-title">No Study Material Loaded</p>
              <p className="placeholder-subtitle">
                Please upload a study PDF above to unlock personalized AI quiz generation.
              </p>
            </div>
          )}
        </div>
      )}

      {/* ========================================================= */}
      {/* STAGE 2: LOADING SCREEN                                   */}
      {/* ========================================================= */}
      {quizState === 'loading' && (
        <div className="ai-loading-container">
          <div className="ai-pulse-orb quiz-orb" />
          <p className="loading-title">Generating your quiz...</p>
          <p className="loading-subtitle">
            Analyzing document key concepts and authoring {numQuestions} {difficulty}-level MCQs with explanations...
          </p>
        </div>
      )}

      {/* ========================================================= */}
      {/* STAGE 3: ACTIVE QUESTION SCREEN                           */}
      {/* ========================================================= */}
      {quizState === 'active' && currentQuestion && (
        <div className="quiz-active-container">
          {/* Progress Header */}
          <div className="quiz-progress-bar-container">
            <div className="quiz-progress-info">
              <span className="quiz-progress-text">
                Question <strong>{currentIndex + 1}</strong> of {questions.length}
              </span>
              <span className={`quiz-diff-badge ${difficulty}`}>
                {difficulty.toUpperCase()}
              </span>
            </div>
            <div className="quiz-progress-track">
              <div
                className="quiz-progress-fill"
                style={{ width: `${progressPercent}%` }}
              />
            </div>
          </div>

          {/* Question Text */}
          <div className="quiz-question-card">
            <div className="question-number-badge">Q{currentIndex + 1}</div>
            <h3 className="quiz-question-prompt">{currentQuestion.question}</h3>
          </div>

          {/* Options Grid */}
          <div className="quiz-options-list">
            {currentQuestion.options.map((optionText, optIdx) => {
              const isSelected = studentAnswers[currentIndex] === optIdx;
              const letter = String.fromCharCode(65 + optIdx); // A, B, C, D

              return (
                <button
                  key={optIdx}
                  type="button"
                  className={`quiz-option-item ${isSelected ? 'selected' : ''}`}
                  onClick={() => handleSelectOption(optIdx)}
                >
                  <div className="option-indicator">
                    <span className="option-letter">{letter}</span>
                  </div>
                  <span className="option-text">{optionText}</span>
                  {isSelected && (
                    <div className="option-check-icon">
                      <Check size={16} />
                    </div>
                  )}
                </button>
              );
            })}
          </div>

          {/* Navigation Controls */}
          <div className="quiz-nav-row">
            <button
              type="button"
              className="btn-secondary-action btn-prev-q"
              onClick={handlePrevious}
              disabled={currentIndex === 0}
            >
              <ChevronLeft size={16} />
              <span>Previous</span>
            </button>

            <button
              type="button"
              className="btn-primary-action btn-next-q"
              onClick={handleNext}
              disabled={!isCurrentAnswered}
            >
              <span>{currentIndex === questions.length - 1 ? 'Submit Quiz' : 'Next Question'}</span>
              <ChevronRight size={16} />
            </button>
          </div>
        </div>
      )}

      {/* ========================================================= */}
      {/* STAGE 4: RESULTS & REVIEW SCREEN                          */}
      {/* ========================================================= */}
      {quizState === 'results' && (
        <div className="quiz-results-container">
          {/* Score Summary Banner */}
          <div className="results-summary-card">
            <div className="results-score-badge">
              <span className="score-number">{scorePercentage}%</span>
              <span className="score-subtext">{correctCount} of {questions.length} Correct</span>
            </div>

            <div className="results-feedback">
              <h3 className="results-feedback-title">
                {scorePercentage === 100 && '🎉 Perfect Score! Outstanding!'}
                {scorePercentage >= 80 && scorePercentage < 100 && '👏 Excellent Job! Great grasp of the material!'}
                {scorePercentage >= 60 && scorePercentage < 80 && '👍 Good Effort! Review the explanations below.'}
                {scorePercentage < 60 && '💪 Keep Practicing! Learn from the breakdown below.'}
              </h3>
              <p className="results-feedback-desc">
                Completed {questions.length} {difficulty} questions from <strong>{filename || 'uploaded notes'}</strong>.
              </p>
            </div>

            <div className="results-stats-row">
              <div className="stat-pill stat-correct">
                <CheckCircle2 size={16} />
                <span><strong>{correctCount}</strong> Correct</span>
              </div>
              <div className="stat-pill stat-incorrect">
                <XCircle size={16} />
                <span><strong>{questions.length - correctCount}</strong> Incorrect</span>
              </div>
            </div>
          </div>

          {/* Retake Actions */}
          <div className="results-actions-bar">
            <button
              type="button"
              className="btn-secondary-action"
              onClick={handleRetake}
              title="Retake these same questions"
            >
              <RotateCcw size={16} />
              <span>Retake This Quiz</span>
            </button>
            <button
              type="button"
              className="btn-primary-action"
              onClick={handleNewQuiz}
              title="Configure and generate a new quiz"
            >
              <PlusCircle size={16} />
              <span>Generate New Quiz</span>
            </button>
          </div>

          {/* Question Review Section */}
          <div className="results-review-section">
            <h4 className="review-section-heading">
              <Award size={18} /> Question-by-Question Review
            </h4>

            <div className="review-list">
              {questions.map((q, qIdx) => {
                const studentAns = studentAnswers[qIdx];
                const isCorrect = studentAns === q.correct_answer;
                const studentChoiceLetter = studentAns !== undefined
                  ? String.fromCharCode(65 + studentAns)
                  : 'None';
                const correctChoiceLetter = String.fromCharCode(65 + q.correct_answer);

                return (
                  <div
                    key={qIdx}
                    className={`review-card ${isCorrect ? 'card-correct' : 'card-incorrect'}`}
                  >
                    <div className="review-card-header">
                      <div className="review-status-row">
                        {isCorrect ? (
                          <span className="badge-review-status correct">
                            <CheckCircle2 size={15} /> Correct
                          </span>
                        ) : (
                          <span className="badge-review-status incorrect">
                            <XCircle size={15} /> Incorrect
                          </span>
                        )}
                        <span className="review-q-num">Question {qIdx + 1}</span>
                      </div>
                    </div>

                    <p className="review-question-text">{q.question}</p>

                    <div className="review-answers-grid">
                      <div className={`answer-box student-ans-box ${isCorrect ? 'box-correct' : 'box-incorrect'}`}>
                        <span className="ans-box-label">Your Answer:</span>
                        <p className="ans-box-val">
                          <strong>{studentChoiceLetter}.</strong> {studentAns !== undefined ? q.options[studentAns] : 'No answer selected'}
                        </p>
                      </div>

                      {!isCorrect && (
                        <div className="answer-box correct-ans-box">
                          <span className="ans-box-label">Correct Answer:</span>
                          <p className="ans-box-val">
                            <strong>{correctChoiceLetter}.</strong> {q.options[q.correct_answer]}
                          </p>
                        </div>
                      )}
                    </div>

                    <div className="review-explanation-box">
                      <span className="explanation-label">Explanation:</span>
                      <p className="explanation-text">{q.explanation}</p>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </section>
  );
}
