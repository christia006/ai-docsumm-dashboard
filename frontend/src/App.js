import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import './styles/App.css'; // Optional: Global styles if needed

function App() {
    return (
        <Router>
            <div className="App">
                <Routes>
                    <Route path="/" element={<Dashboard />} />
                    {/* Anda bisa menambahkan route lain di sini jika diperlukan */}
                </Routes>
            </div>
        </Router>
    );
}

export default App;