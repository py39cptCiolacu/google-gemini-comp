import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Helmet } from 'react-helmet';

const Analysis = () => {
    const [parameters, setParameters] = useState([]);
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');
    const [selectedLand, setSelectedLand] = useState('');
    const [lands, setLands] = useState([]);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (!token) {
            navigate('/login');
            return;
        }

        const fetchLands = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:5000/api/v1/user_lands', {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    },
                });
                setLands(response.data);
            } catch (error) {
                console.error('There was an error fetching the lands!', error);
            }
        };

        fetchLands();
    }, [navigate]);

    const handleCheckboxChange = (event) => {
        const { value, checked } = event.target;
        if (checked) {
            setParameters([...parameters, value]);
        } else {
            setParameters(parameters.filter(param => param !== value));
        }
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        setError('');

        const start = new Date(startDate);
        const end = new Date(endDate);
        const timeDiff = end - start;
        const dayDiff = timeDiff / (1000 * 3600 * 24);

        if (dayDiff > 7) {
            setError('The date range cannot exceed 7 days.');
            return;
        }

        const formatDate = (date) => {
            const year = date.getFullYear();
            const month = ('0' + (date.getMonth() + 1)).slice(-2);
            const day = ('0' + date.getDate()).slice(-2);
            return { year, month, day };
        };

        const startFormatted = formatDate(start);
        const endFormatted = formatDate(end);

        const data = {
            parameters: parameters,
            start_date: `${startFormatted.year}-${startFormatted.month}-${startFormatted.day}`,
            end_date: `${endFormatted.year}-${endFormatted.month}-${endFormatted.day}`,
            land_id: selectedLand
        };

        try {
            const token = localStorage.getItem('token');
            const response = await axios.post('http://127.0.0.1:5000/api/v1/analysis', data, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
            });
            console.log(response.data);
        } catch (error) {
            console.error('There was an error submitting the form!', error);
        }
    };

    return (
        <>
            <Helmet>
                <title>Analysis Form - FieldMaster</title>
            </Helmet>
            <div style={{ paddingTop: '60px' }}>
                <form onSubmit={handleSubmit}>
                    <h2>Select Land</h2>
                    <select value={selectedLand} onChange={(e) => setSelectedLand(e.target.value)} required>
                        <option value="">Select a land</option>
                        {lands.map(land => (
                            <option key={land.id} value={land.id}>{land.name}</option>
                        ))}
                    </select><br />

                    <h2>Select Parameters for Analysis</h2>
                    <label>
                        <input type="checkbox" name="parameters" value="2m_temperature" onChange={handleCheckboxChange} /> 2m Temperature
                    </label><br />
                    <label>
                        <input type="checkbox" name="parameters" value="total_precipitation" onChange={handleCheckboxChange} /> Total Precipitation
                    </label><br />
                    <label>
                        <input type="checkbox" name="parameters" value="volumetric_soil_water_layer_1" onChange={handleCheckboxChange} /> Volumetric Soil Water Layer 1
                    </label><br />
                    <label>
                        <input type="checkbox" name="parameters" value="surface_solar_radiation_downwards" onChange={handleCheckboxChange} /> Surface Solar Radiation Downwards
                    </label><br />
                    <label>
                        <input type="checkbox" name="parameters" value="2m_dewpoint_temperature" onChange={handleCheckboxChange} /> 2m Dewpoint Temperature
                    </label><br />
                    <label>
                        <input type="checkbox" name="parameters" value="10m_u_component_of_wind" onChange={handleCheckboxChange} /> 10m U Component of Wind
                    </label><br />
                    <label>
                        <input type="checkbox" name="parameters" value="10m_v_component_of_wind" onChange={handleCheckboxChange} /> 10m V Component of Wind
                    </label><br />
                    <label>
                        <input type="checkbox" name="parameters" value="soil_temperature_level_1" onChange={handleCheckboxChange} /> Soil Temperature Level 1
                    </label><br />

                    <h2>Select Date Range</h2>
                    <label htmlFor="start_date">Start Date:</label>
                    <input type="date" id="start_date" name="start_date" value={startDate} onChange={(e) => setStartDate(e.target.value)} /><br />
                    <label htmlFor="end_date">End Date:</label>
                    <input type="date" id="end_date" name="end_date" value={endDate} onChange={(e) => setEndDate(e.target.value)} /><br />

                    {error && <p style={{ color: 'red' }}>{error}</p>}
                    <input type="submit" value="Submit" />
                </form>
            </div>
        </>
    );
};

export default Analysis;
