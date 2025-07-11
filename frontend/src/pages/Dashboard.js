import React, { useState, useEffect } from 'react';
import DocumentUpload from '../components/DocumentUpload';
import SummaryDisplay from '../components/SummaryDisplay';
import { getDocuments, getDocumentById } from '../api';
import './Dashboard.css'; // Untuk styling dashboard

function Dashboard() {
    const [documents, setDocuments] = useState([]);
    const [selectedDocument, setSelectedDocument] = useState(null);
    const [loadingDocuments, setLoadingDocuments] = useState(true);
    const [error, setError] = useState(null);

    const fetchDocuments = async () => {
        setLoadingDocuments(true);
        try {
            const response = await getDocuments();
            setDocuments(response.data);
        } catch (err) {
            console.error("Error fetching documents:", err);
            setError("Failed to load documents.");
        } finally {
            setLoadingDocuments(false);
        }
    };

    useEffect(() => {
        fetchDocuments();
    }, []);

    const handleDocumentSummarized = (newDocument) => {
        // Tambahkan dokumen baru ke daftar
        setDocuments((prevDocs) => [newDocument, ...prevDocs]);
        setSelectedDocument(newDocument); // Otomatis tampilkan ringkasan dokumen baru
    };

    const handleDocumentSelect = async (docId) => {
        try {
            const response = await getDocumentById(docId);
            setSelectedDocument(response.data);
        } catch (err) {
            console.error("Error fetching document details:", err);
            setError("Failed to load document details.");
        }
    };

    return (
        <div className="dashboard-container">
            <header className="dashboard-header">
                <h1>AI Document Summarizer Dashboard</h1>
            </header>

            <div className="dashboard-content">
                <div className="upload-section">
                    <DocumentUpload onDocumentSummarized={handleDocumentSummarized} />
                </div>

                <div className="documents-list-section">
                    <h2>Summarized Documents</h2>
                    {loadingDocuments ? (
                        <p>Loading documents...</p>
                    ) : error ? (
                        <p className="error-message">{error}</p>
                    ) : documents.length === 0 ? (
                        <p>No documents summarized yet. Upload one!</p>
                    ) : (
                        <ul className="document-list">
                            {documents.map((doc) => (
                                <li
                                    key={doc.id}
                                    onClick={() => handleDocumentSelect(doc.id)}
                                    className={selectedDocument?.id === doc.id ? 'active' : ''}
                                >
                                    {doc.filename} ({new Date(doc.uploaded_at).toLocaleDateString()})
                                </li>
                            ))}
                        </ul>
                    )}
                </div>

                <div className="summary-details-section">
                    <SummaryDisplay document={selectedDocument} />
                </div>
            </div>
        </div>
    );
}

export default Dashboard;