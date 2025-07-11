import React, { useState, useEffect } from 'react';
import DocumentUpload from '../components/DocumentUpload';
import SummaryDisplay from '../components/SummaryDisplay';
import { getDocuments, getDocumentById, deleteDocument } from '../api';
import './Dashboard.css';

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
        setDocuments((prevDocs) => [newDocument, ...prevDocs]);
        setSelectedDocument(newDocument);
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

    const handleDeleteDocument = async (docId) => {
        if (!window.confirm("Are you sure you want to delete this document?")) return;
        try {
            await deleteDocument(docId);
            setDocuments((prevDocs) => prevDocs.filter((doc) => doc.id !== docId));
            if (selectedDocument?.id === docId) {
                setSelectedDocument(null);
            }
        } catch (err) {
            console.error("Error deleting document:", err);
            setError("Failed to delete document.");
        }
    };

    return (
        <div className="dashboard">
            <header className="dashboard-header">
                <h1>📄 AI Document Summarizer</h1>
            </header>

            <main className="dashboard-main">
                <section className="left-panel">
                    <DocumentUpload onDocumentSummarized={handleDocumentSummarized} />
                    <h2>📚 Summarized Documents</h2>
                    {loadingDocuments ? (
                        <p>Loading documents...</p>
                    ) : error ? (
                        <p className="error">{error}</p>
                    ) : documents.length === 0 ? (
                        <p>No documents summarized yet.</p>
                    ) : (
                        <ul className="documents-list">
                            {documents.map((doc) => (
                                <li key={doc.id} className={selectedDocument?.id === doc.id ? 'active' : ''}>
                                    <div onClick={() => handleDocumentSelect(doc.id)}>
                                        <strong>{doc.filename}</strong><br />
                                        <small>{new Date(doc.uploaded_at).toLocaleDateString()}</small>
                                    </div>
                                    <button
                                        className="delete-btn"
                                        onClick={() => handleDeleteDocument(doc.id)}
                                        title="Delete document"
                                    >
                                        🗑️
                                    </button>
                                </li>
                            ))}
                        </ul>
                    )}
                </section>

                <section className="right-panel">
                    <SummaryDisplay document={selectedDocument} />
                </section>
            </main>
        </div>
    );
}

export default Dashboard;
