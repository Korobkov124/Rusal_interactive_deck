import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import AuthPage from './AuthPage';
import Page1 from './Page1';

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<AuthPage />} />
                <Route path="/page1" element={<Page1 />} />
                {}
            </Routes>
        </Router>
    );
};

export default App;
