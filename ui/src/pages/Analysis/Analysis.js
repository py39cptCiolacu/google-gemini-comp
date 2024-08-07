import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { 
    MDBCheckbox, 
    MDBInput, 
    MDBDropdown, 
    MDBDropdownItem, 
    MDBDropdownMenu, 
    MDBDropdownToggle, 
    MDBBtn, 
    MDBContainer, 
    MDBRow, 
    MDBCol, 
    MDBCard, 
    MDBCardBody, 
    MDBCardHeader 
} from 'mdb-react-ui-kit';

const FormComponent = () => {
    const [parameters, setParameters] = useState([]);
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');
    const [fields, setFields] = useState([]);
    const [crops, setCrops] = useState([]);
    const [selectedField, setSelectedField] = useState('');
    const [selectedCrop, setSelectedCrop] = useState('');
    const navigate = useNavigate();

    // Datele simulate pentru loturi și culturi
    const fieldsOptions = ['Field 1', 'Field 2', 'Field 3'];
    const cropsOptions = ['Wheat', 'Corn', 'Barley', 'Oats', 'Soybean', 'Rice', 'Canola', 'Cotton'];

    // Parametrii actualizați
    const parameterOptions = [
        'Temperature at 2 meters',
        'Total Precipitation',
        'Soil Moisture (top layer)',
        'Solar Radiation at the surface',
        'Relative Humidity',
        'Wind Speed (u component)',
        'Wind Speed (v component)',
        'Soil Temperature at level 1',
    ];

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (!token) {
            navigate('/login');
        }

        setFields(fieldsOptions);
        setCrops(cropsOptions);
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
            field: selectedField,
            crop: selectedCrop,
        };

        try {
            const token = localStorage.getItem('token');
            const response = await axios.post('http://localhost:5000/api/v1/analysis', data, {
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
        <MDBContainer style={{ padding: '50px' }} className="my-4">
            <MDBRow className="justify-content-center">
                <MDBCol md="8">
                    <MDBCard>
                        <MDBCardHeader>
                            <h4>Select Parameters for Analysis</h4>
                        </MDBCardHeader>
                        <MDBCardBody>
                            <form onSubmit={handleSubmit}>
                                <h5>Select Parameters</h5>
                                <MDBRow>
                                    {parameterOptions.map((param, index) => (
                                        <MDBCol md="6" key={index}>
                                            <MDBCheckbox
                                                id={`checkbox${index}`}
                                                label={param}
                                                value={param}
                                                onChange={handleCheckboxChange}
                                            />
                                        </MDBCol>
                                    ))}
                                </MDBRow>

                                <h5 className="mt-4">Select Date Range</h5>
                                <MDBInput
                                    type="date"
                                    label="Start Date"
                                    value={startDate}
                                    onChange={(e) => setStartDate(e.target.value)}
                                />
                                <MDBInput
                                    type="date"
                                    label="End Date"
                                    value={endDate}
                                    onChange={(e) => setEndDate(e.target.value)}
                                />

                                <h5 className="mt-4">Select Field</h5>
                                <MDBDropdown className="mb-4">
                                    <MDBDropdownToggle color="secondary">
                                        {selectedField || 'Select Field'}
                                    </MDBDropdownToggle>
                                    <MDBDropdownMenu>
                                        {fields.map((field, index) => (
                                            <MDBDropdownItem key={index} onClick={() => setSelectedField(field)}>
                                                {field}
                                            </MDBDropdownItem>
                                        ))}
                                    </MDBDropdownMenu>
                                </MDBDropdown>

                                <h5 className="mt-4">Select Crop</h5>
                                <MDBDropdown className="mb-4">
                                    <MDBDropdownToggle color="secondary">
                                        {selectedCrop || 'Select Crop'}
                                    </MDBDropdownToggle>
                                    <MDBDropdownMenu>
                                        {crops.map((crop, index) => (
                                            <MDBDropdownItem key={index} onClick={() => setSelectedCrop(crop)}>
                                                {crop}
                                            </MDBDropdownItem>
                                        ))}
                                    </MDBDropdownMenu>
                                </MDBDropdown>

                                <MDBBtn type="submit" color="primary" className="mt-4">Submit</MDBBtn>
                            </form>
                        </MDBCardBody>
                    </MDBCard>
                </MDBCol>
            </MDBRow>
        </MDBContainer>
    );
};

export default FormComponent;
