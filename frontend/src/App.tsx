import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import MinerDetail from './components/MinerDetail';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>矿机管理系统</h1>
        </header>
        <main className="App-main">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/miner/:id" element={<MinerDetail />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
