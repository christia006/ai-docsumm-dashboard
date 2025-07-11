import React, { useState } from 'react';
import { uploadDocument } from '../api';

function DocumentUpload({ onDocumentSummarized }) {
    const [selectedFile, setSelectedFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
        setError(null);
    };

    const handleUpload = async () => {
        if (!selectedFile) {
            setError("Please select a file first.");
            return;
        }
        setLoading(true);
        try {
            const response = await uploadDocument(selectedFile);
            alert('Document summarized successfully!');
            onDocumentSummarized(response.data);
            setSelectedFile(null);
        } catch (err) {
            console.error("Error:", err);
            setError(err.response?.data?.detail || "Failed to summarize document.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="document-upload-card">
            <h2>Upload Document for Summary</h2>
            <input type="file" accept=".txt,.pdf" onChange={handleFileChange} />
            {selectedFile && <p>Selected file: {selectedFile.name}</p>}
            <button onClick={handleUpload} disabled={loading}>
                {loading ? 'Summarizing...' : 'Summarize Document'}
            </button>
            {error && <p className="error-message">{error}</p>}
        </div>
    );
}

export default DocumentUpload;
