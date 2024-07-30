import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './UserProfile.css';

function UserProfile() {
  const [userInfo, setUserInfo] = useState(null);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUserInfo = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/user_profile', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include', // Include credentials for cross-origin requests
        });

        if (response.status === 401) {
          navigate('/login'); // Redirect to login if not authenticated
          return;
        }

        // Log the raw response text
        const responseText = await response.text();
        console.log('Response Text:', responseText);

        // Try to parse the response as JSON
        const data = JSON.parse(responseText);

        if (!response.ok) {
          throw new Error(data.message || 'Something went wrong');
        }

        setUserInfo(data);
      } catch (error) {
        console.error('Fetch error:', error); // Log the error
        setError(error.message);
      }
    };

    fetchUserInfo();
  }, [navigate]);

  if (error) {
    return <div className="user-profile-container"><p>{error}</p></div>;
  }

  return (
    <div className="user-profile-container">
      {userInfo ? (
        <div>
          <h1>User Profile</h1>
          <p><strong>Username:</strong> {userInfo.username}</p>
          <p><strong>Email:</strong> {userInfo.email}</p>
          <button onClick={() => navigate('/map')} className="map-button">
            Go to Map
          </button>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}

export default UserProfile;
