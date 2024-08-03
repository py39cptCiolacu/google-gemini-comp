import React, { useState } from 'react';
import axios from 'axios';

const FormComponent = () => {
    const [parameters, setParameters] = useState([]);
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');

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
            const response = await axios.post('http://127.0.0.1:5000/analysis', data, {
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            console.log(response.data.message);
            // Handle the response data as needed
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
