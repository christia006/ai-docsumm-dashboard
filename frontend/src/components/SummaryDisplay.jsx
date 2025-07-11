import React from 'react';

function SummaryDisplay({ document }) {
    if (!document) {
        return <p>Select a document to see the summary.</p>;
    }

    return (
        <div>
            <h2>Summary of: {document.filename}</h2>
            <div className="summary-paragraph">
                {document.summary}
            </div>
        </div>
    );
}

export default SummaryDisplay;
