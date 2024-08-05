import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const FormComponent = () => {
    const [parameters, setParameters] = useState([]);
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (!token) {
            navigate('/login');
        }
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

        const data = {
            parameters: parameters,
            start_date: startDate,
            end_date: endDate,
        };

        try {
            const token = localStorage.getItem('token');
            const response = await axios.post('http://127.0.0.1:5000/analysis', data, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
            });
            console.log(response.data.message);
        } catch (error) {
            console.error('There was an error submitting the form!', error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>Select Parameters for Analysis</h2>
            <label>
                <input type="checkbox" name="parameters" value="param1" onChange={handleCheckboxChange} /> Parameter 1
            </label><br />
            <label>
                <input type="checkbox" name="parameters" value="param2" onChange={handleCheckboxChange} /> Parameter 2
            </label><br />
            <label>
                <input type="checkbox" name="parameters" value="param3" onChange={handleCheckboxChange} /> Parameter 3
            </label><br />

            <h2>Select Date Range</h2>
            <label htmlFor="start_date">Start Date:</label>
            <input type="date" id="start_date" name="start_date" value={startDate} onChange={(e) => setStartDate(e.target.value)} /><br />
            <label htmlFor="end_date">End Date:</label>
            <input type="date" id="end_date" name="end_date" value={endDate} onChange={(e) => setEndDate(e.target.value)} /><br />

            <input type="submit" value="Submit" />
        </form>
    );
};

export default FormComponent;
