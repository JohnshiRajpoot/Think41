import React from 'react';
import './App.css';
import CustomerList from './components/CustomerList';

function App() {
  return (
    <div className="container mt-5">
      <h2 className="text-center mb-4">Customer Dashboard</h2>
      <CustomerList />
    </div>
  );
}

export default App;
