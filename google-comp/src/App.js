import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link} from 'react-router-dom';
import './App.css';
import Login from './Login';
import Register from './Register';
import Map from './Map';
import UserProfile from './UserProfile';

function App() {
  const [username, setUsername] = useState('');

  return (
    <Router>
      <div className="App">
        <nav>
          <Link to="/">Home</Link> | <Link to="/login">Login</Link> | <Link to="/register">Register</Link>
        </nav>
        <Routes>
          <Route path="/login" element={<Login setUsername={setUsername} />} />
          <Route path="/register" element={<Register />} />
          <Route path="/user_profile" element={<UserProfile />} />
          <Route path="/map" element={<Map />} />
          <Route path="/" element={<Home />} />
        </Routes>
      </div>
    </Router>
  );
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
