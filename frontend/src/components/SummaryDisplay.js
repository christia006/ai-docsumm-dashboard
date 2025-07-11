import React from 'react';
import { Bar } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
);

function SummaryDisplay({ document }) {
    if (!document) {
        return <div className="summary-display-card">Select a document to see details.</div>;
    }

    // Data untuk chart keywords
    const keywordLabels = document.keywords.map(k => k.keyword_text);
    const keywordScores = document.keywords.map(k => k.score);

    const keywordChartData = {
        labels: keywordLabels,
        datasets: [
            {
                label: 'Keyword Score',
                data: keywordScores,
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
            },
        ],
    };

    const chartOptions = {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Top Keywords by Score',
            },
        },
    };

    return (
        <div className="summary-display-card">
            <h2>Document Details: {document.filename}</h2>
            <p><strong>Upload Date:</strong> {new Date(document.uploaded_at).toLocaleDateString()}</p>

            <h3>Summary:</h3>
            <p className="summary-text">{document.summary}</p>

            <h3>Named Entities:</h3>
            <ul className="entity-list">
                {document.entities.length > 0 ? (
                    document.entities.map((entity, index) => (
                        <li key={index}>
                            <strong>{entity.entity_type}:</strong> {entity.entity_text}
                        </li>
                    ))
                ) : (
                    <li>No entities found.</li>
                )}
            </ul>

            <h3>Keywords:</h3>
            {document.keywords.length > 0 ? (
                <div className="keyword-chart-container">
                    <Bar data={keywordChartData} options={chartOptions} />
                </div>
            ) : (
                <p>No keywords found.</p>
            )}
            {/* Anda bisa menambahkan bagian untuk menampilkan original_text juga jika diperlukan */}
        </div>
    );
}

export default SummaryDisplay;