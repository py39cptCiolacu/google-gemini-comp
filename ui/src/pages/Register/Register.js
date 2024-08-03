import React, { useState } from 'react';
import './Register.css';
import {
  MDBBtn,
  MDBContainer,
  MDBRow,
  MDBCol,
  MDBCard,
  MDBCardBody,
  MDBInput,
  MDBCheckbox,
  MDBIcon
}
from 'mdb-react-ui-kit';

function Register() {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirm, setPasswordConfirm] = useState('');
  const [message, setMessage] = useState('');

  const handleRegister = async (e) => {
    e.preventDefault();
    
    const response = await fetch('http://127.0.0.1:5000/api/v1/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, username, password, password_confirm: passwordConfirm }),
    });

    const data = await response.json();

    if (response.status === 201) {
      setMessage(data.message);
    } else {
      setMessage(data.message);
    }
  };

//   return (
//     <div className="register-container">
//       <h3>Register</h2>
//       <form onSubmit={handleRegister}>
//         <div>
//           <label>Email:</label>
//           <input
//             type="email"
//             value={email}
//             onChange={(e) => setEmail(e.target.value)}
//             required
//           />
//         </div>
//         <div>
//           <label>Username:</label>
//           <input
//             type="text"
//             value={username}
//             onChange={(e) => setUsername(e.target.value)}
//             required
//           />
//         </div>
//         <div>
//           <label>Password:</label>
//           <input
//             type="password"
//             value={password}
//             onChange={(e) => setPassword(e.target.value)}
//             required
//           />
//         </div>
//         <div>
//           <label>Confirm Password:</label>
//           <input
//             type="password"
//             value={passwordConfirm}
//             onChange={(e) => setPasswordConfirm(e.target.value)}
//             required
//           />
//         </div>
//         <button type="submit">Register</button>
//       </form>
//       {message && <p>{message}</p>}
//     </div>
//   );
// }


    return (
      <MDBContainer fluid className='p-4'>
      
        <MDBRow>
    
          <MDBCol md='6' className='text-center text-md-start d-flex flex-column justify-content-center'>
    
            <h1 className="my-5 display-3 fw-bold ls-tight px-3">
              The best offer <br />
              <span className="text-primary">for your business</span>
            </h1>
    
            <p className='px-3' style={{color: 'hsl(217, 10%, 50.8%)'}}>
              Lorem ipsum dolor sit amet consectetur adipisicing elit.
              Eveniet, itaque accusantium odio, soluta, corrupti aliquam
              quibusdam tempora at cupiditate quis eum maiores libero
              veritatis? Dicta facilis sint aliquid ipsum atque?
            </p>
    
          </MDBCol>
    
          <MDBCol md='6'>
    
            <MDBCard className='my-5'>
              <MDBCardBody className='p-5'>
    
                <MDBRow>
                  <MDBCol col='6'>
                    <MDBInput wrapperClass='mb-4' label='Username' id='form1' type='text'/>
                  </MDBCol>
    
                  <MDBCol col='6'>
                    <MDBInput wrapperClass='mb-4' label='Email' id='form1' type='email'/>
                  </MDBCol>
                </MDBRow>
    
                <MDBInput wrapperClass='mb-4' label='Password' id='form1' type='password'/>
                <MDBInput wrapperClass='mb-4' label='Password' id='form1' type='password'/>
    
                {/* <div className='d-flex justify-content-center mb-4'>
                  <MDBCheckbox name='flexCheck' value='' id='flexCheckDefault' label='Subscribe to our newsletter' />
                </div>
     */}
                <MDBBtn className='w-100 mb-4' size='md'>sign up</MDBBtn>
                
                <div className="text-center">
                
                  <p>or sign up</p>
                
                </div>
                
              </MDBCardBody>
            </MDBCard>
                
          </MDBCol>
                
        </MDBRow>
                
      </MDBContainer>
    );
}

export default Register;
