
import React, { useState } from 'react';
import { MapContainer, TileLayer, Marker, Polygon, useMapEvents } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import axios from 'axios';

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

  return (
    <MapContainer center={[0, 0]} zoom={2} style={{ height: '600px', width: '100%' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <MapClickHandler />
      {points.map((point, index) => (
        <Marker key={index} position={point}></Marker>
      ))}
      {polygon && <Polygon positions={polygon} color="red" />}
    </MapContainer>
  );
};

export default MapComponent;