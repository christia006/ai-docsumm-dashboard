import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const uploadDocument = (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/summarize-document/', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
};

export const getDocuments = () => api.get('/documents/');

export const getDocumentById = (id) => api.get(`/documents/${id}`);

export const deleteDocument = (id) => api.delete(`/documents/${id}`);

export default api;
