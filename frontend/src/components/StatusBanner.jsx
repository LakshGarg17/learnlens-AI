import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Activity, CheckCircle2, XCircle, RefreshCw, Cpu } from 'lucide-react';

const API_BASE = 'http://localhost:8000';

export default function StatusBanner() {
  const [backendStatus, setBackendStatus] = useState('checking'); // 'checking' | 'connected' | 'offline'
  const [aiStatus, setAiStatus] = useState(null); // null | { success: bool, message: string, model?: string }
  const [testingAi, setTestingAi] = useState(false);

  const checkBackendHealth = async () => {
    try {
      setBackendStatus('checking');
      const response = await axios.get(`${API_BASE}/api/health`, { timeout: 3000 });
      if (response.data && response.data.status === 'ok') {
        setBackendStatus('connected');
      } else {
        setBackendStatus('offline');
      }
    } catch {
      setBackendStatus('offline');
    }
  };

  const runAiTest = async () => {
    setTestingAi(true);
    setAiStatus(null);
    try {
      const response = await axios.get(`${API_BASE}/api/test-ai-connection`, { timeout: 8000 });
      setAiStatus(response.data);
    } catch (err) {
      setAiStatus({
        success: false,
        message: err.response?.data?.message || 'Could not reach backend API endpoint',
      });
    } finally {
      setTestingAi(false);
    }
  };

  useEffect(() => {
    checkBackendHealth();
  }, []);

  return (
    <div className="status-banner">
      <div className="status-item">
        <span className="status-label">FastAPI Backend:</span>
        <div className={`status-pill ${backendStatus}`}>
          {backendStatus === 'connected' && <CheckCircle2 size={15} />}
          {backendStatus === 'offline' && <XCircle size={15} />}
          {backendStatus === 'checking' && <RefreshCw size={15} className="spin" />}
          <span>
            {backendStatus === 'connected' && 'Online (Port 8000)'}
            {backendStatus === 'offline' && 'Offline (Check backend server)'}
            {backendStatus === 'checking' && 'Connecting...'}
          </span>
        </div>
        <button
          className="btn-icon"
          onClick={checkBackendHealth}
          title="Refresh backend status"
        >
          <RefreshCw size={14} />
        </button>
      </div>

      <div className="status-item ai-test-section">
        <button
          className="btn-ai-test"
          onClick={runAiTest}
          disabled={testingAi || backendStatus !== 'connected'}
        >
          <Cpu size={15} />
          <span>{testingAi ? 'Testing Anthropic API...' : 'Test AI Connection'}</span>
        </button>

        {aiStatus && (
          <div className={`ai-result-pill ${aiStatus.success ? 'success' : 'warning'}`}>
            <span>
              {aiStatus.success
                ? `AI Connected (${aiStatus.model || 'Claude'}): "${aiStatus.message}"`
                : `AI Key Check: ${aiStatus.message}`}
            </span>
          </div>
        )}
      </div>
    </div>
  );
}
