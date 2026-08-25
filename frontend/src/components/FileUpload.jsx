import React, { useState, useRef } from 'react';
import axios from 'axios';
import { UploadCloud, FileText, Loader2, AlertCircle, CheckCircle2, X } from 'lucide-react';

const API_BASE = 'http://localhost:8000';

export default function FileUpload({ onUploadSuccess }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [uploadedInfo, setUploadedInfo] = useState(null);
  const fileInputRef = useRef(null);

  const handleFile = async (file) => {
    if (!file) return;

    // Validate file type
    const isPdf = file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf');
    if (!isPdf) {
      setErrorMessage('Please select a valid PDF file (.pdf format only).');
      setSelectedFile(null);
      return;
    }

    // Clear previous errors & previous uploaded info
    setErrorMessage(null);
    setSelectedFile(file);
    setIsUploading(true);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_BASE}/api/upload-pdf`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const data = response.data;
      setUploadedInfo({
        name: data.filename || file.name,
        size: file.size,
        pages: data.page_count,
      });

      if (onUploadSuccess) {
        onUploadSuccess(data);
      }
    } catch (err) {
      const backendError =
        err.response?.data?.detail ||
        err.response?.data?.message ||
        err.message ||
        'Failed to upload and extract text from the PDF.';
      setErrorMessage(backendError);
      setUploadedInfo(null);
    } finally {
      setIsUploading(false);
    }
  };

  const handleInputChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFile(file);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    const file = e.dataTransfer.files?.[0];
    if (file) {
      handleFile(file);
    }
  };

  const handleClear = (e) => {
    e.stopPropagation();
    e.preventDefault();
    setSelectedFile(null);
    setUploadedInfo(null);
    setErrorMessage(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="file-upload-wrapper">
      <div
        className={`file-drop-area ${isDragging ? 'drag-over' : ''} ${isUploading ? 'uploading' : ''} ${uploadedInfo ? 'has-file' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => !isUploading && fileInputRef.current?.click()}
        role="button"
        tabIndex={0}
        aria-label="Upload PDF Document"
      >
        <input
          ref={fileInputRef}
          id="pdf-upload-input"
          type="file"
          accept=".pdf"
          onChange={handleInputChange}
          className="file-input-hidden"
          disabled={isUploading}
        />

        {isUploading ? (
          <div className="upload-state-container">
            <Loader2 size={32} className="spin text-accent" />
            <div className="upload-state-text">
              <span className="primary-prompt">Extracting text with LearnLens AI...</span>
              <span className="secondary-prompt">Parsing pages from {selectedFile?.name}</span>
            </div>
          </div>
        ) : uploadedInfo ? (
          <div className="file-info-preview">
            <FileText size={32} className="text-accent" />
            <div className="file-details">
              <span className="file-name" title={uploadedInfo.name}>{uploadedInfo.name}</span>
              <span className="file-meta">
                {(uploadedInfo.size / 1024).toFixed(1)} KB • {uploadedInfo.pages} {uploadedInfo.pages === 1 ? 'page' : 'pages'} extracted
              </span>
            </div>
            <div className="file-action-badges">
              <span className="badge-ready">
                <CheckCircle2 size={13} /> Parsed
              </span>
              <button
                type="button"
                className="btn-clear-file"
                onClick={handleClear}
                title="Remove and upload another PDF"
                aria-label="Remove uploaded file"
              >
                <X size={14} />
              </button>
            </div>
          </div>
        ) : (
          <div className="upload-placeholder">
            <UploadCloud size={34} className="placeholder-icon" />
            <span className="primary-prompt">
              {isDragging ? 'Drop your PDF here' : 'Click to browse or drop PDF here'}
            </span>
            <span className="secondary-prompt">Supports .pdf files with extractable text</span>
          </div>
        )}
      </div>

      {errorMessage && (
        <div className="upload-error-alert" role="alert">
          <AlertCircle size={18} className="error-icon" />
          <div className="error-text">
            <strong>Upload Error:</strong> {errorMessage}
          </div>
          <button
            type="button"
            className="error-dismiss-btn"
            onClick={() => setErrorMessage(null)}
            aria-label="Dismiss error"
          >
            <X size={14} />
          </button>
        </div>
      )}
    </div>
  );
}
