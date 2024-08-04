import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Link, Navigate } from 'react-router-dom';
import './App.css';
import Login from './pages/Login/Login';
import Register from './pages/Register/Register';
import Map from './pages/Map/Map';
import UserProfile from './pages/UserProfile/UserProfile';
import Analysis from './pages/Analysis/Analysis'


import 'mdb-react-ui-kit/dist/css/mdb.min.css';
function App() {
  const [username, setUsername] = useState('');

  // Verificăm dacă există un token în localStorage și actualizăm starea
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      // Poti decoda token-ul JWT pentru a obține informațiile despre utilizator
      // În acest exemplu simplu, presupunem că utilizatorul este autentificat dacă există un token
      setUsername('Authenticated User'); // Într-un caz real, ar trebui să obții username-ul din token
    }
  }, []);

  return (
    <Router>
      <div className="App">
        <nav>
          <Link to="/">Home</Link> | <Link to="/login">Login</Link> | <Link to="/register">Register</Link>
        </nav>
        <Routes>
          <Route path="/login" element={<Login setUsername={setUsername} />} />
          <Route path="/register" element={<Register />} />
          <Route path="/user_profile" element={
            <PrivateRoute>
              <UserProfile />
            </PrivateRoute>
          } />
          <Route path="/map" element={
            <PrivateRoute>
              <Map />
            </PrivateRoute>
          } />
          <Route path="/Analysis" element={
            <PrivateRoute>
              <Analysis />
            </PrivateRoute>
          } />
          <Route path="/" element={<Home />} />
        </Routes>
      </div>
    </Router>
  );
}

// Componentă pentru rutele protejate
function PrivateRoute({ children }) {
  const token = localStorage.getItem('token');
  return token ? children : <Navigate to="/login" />;
}

function Home() {
  return (
    <div>
      <h2>Home Page</h2>
      <Link to="/login">Go to Login</Link><br />
      <Link to="/register">Go to Register</Link>
    </div>
  );
}

export default App;
