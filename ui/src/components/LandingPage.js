import React from 'react';
import { MDBContainer, MDBRow, MDBCol, MDBBtn } from 'mdb-react-ui-kit';

export default function LandingPage() {
  return (
    <MDBContainer fluid className="px-4 py-5 my-5 text-center">
      <MDBRow className="align-items-center g-lg-5 py-5">
        <MDBCol lg="7" className="text-lg-start">
          <h1 className="display-4 fw-bold lh-1 mb-3">A New Way to Invest in Agriculture</h1>
          <p className="col-lg-10 fs-4">
            Zou provides farmers, ranchers, private foresters, and agricultural producers 
            with online self service applications and educational materials.
          </p>
          <MDBBtn color="success" size="lg">Invest Now</MDBBtn>
        </MDBCol>
        <MDBCol md="10" lg="5">
          <img src="/path-to-your-image.jpg" className="img-fluid" alt="Agriculture Image" />
        </MDBCol>
      </MDBRow>
      <MDBRow className="mt-5">
        <h2>New Opportunities</h2>
        <p>We are the first and the only crowdfunding platform enabling you to help finance our farmers.</p>
      </MDBRow>
    </MDBContainer>
  );
}
