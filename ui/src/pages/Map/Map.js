import React, { useState } from 'react';
import { MapContainer, TileLayer, Marker, Polygon, useMapEvents } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import axios from 'axios';
import { MDBBtn } from 'mdb-react-ui-kit';
import 'mdb-react-ui-kit/dist/css/mdb.min.css'; // Import MDB CSS

// Fix the marker icon issue by using the default Leaflet icon
delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const MapComponent = () => {
  const [points, setPoints] = useState([]);
  const [polygon, setPolygon] = useState(null);

  const MapClickHandler = () => {
    useMapEvents({
      click: (e) => {
        const newPoint = [e.latlng.lat, e.latlng.lng];
        let newPoints = [...points, newPoint];

        if (newPoints.length === 5) {
          newPoints = [newPoint];  // Reset to the new point only
        }

        setPoints(newPoints);

        if (newPoints.length === 4) {
          setPolygon(newPoints);
        } else {
          setPolygon(null);
        }

        axios.post('/get_coordinates', { lat: e.latlng.lat, lng: e.latlng.lng })
          .then(response => {
            console.log('Server response:', response.data);
          })
          .catch(error => console.error('Error posting coordinates:', error));
      }
    });
    return null;
  };

  const handleDeletePoints = () => {
    setPoints([]);
    setPolygon(null);
  };

  return (
    <div style={{ display: 'flex', alignItems: 'center', paddingTop: '70px'}}>
      <div style={{ 
        flex: 1, 
        position: 'relative',
        borderRadius: '10px',
        overflow: 'hidden',
        marginRight: '10px'
      }}>
        <MapContainer 
          center={[0, 0]} 
          zoom={2} 
          style={{ 
            height: '500px',  // Increased height
            width: 'calc(100% - 20px)'  // Adjusted width to be a bit narrower
          }}
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <MapClickHandler />
          {points.map((point, index) => (
            <Marker key={index} position={point}></Marker>
          ))}
          {polygon && <Polygon positions={polygon} color="red" />}
        </MapContainer>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', alignItems: 'center' }}>
        <MDBBtn style={{ backgroundColor: '#00b300', width: '120px' }}>Add Land</MDBBtn>
        <MDBBtn 
          style={{ backgroundColor: '#00b300', width: '120px' }} 
          onClick={handleDeletePoints}
        >
          Delete
        </MDBBtn>
        {/* <MDBBtn style={{ backgroundColor: '#00b300', width: '120px' }}>B`</MDBBtn> */}
      </div>
    </div>
  );
};

export default MapComponent;
