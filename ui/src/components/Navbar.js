import React from 'react';
import { MDBNavbar, MDBContainer, MDBNavbarBrand, MDBNavbarNav, MDBNavbarItem, MDBNavbarLink, MDBNavbarToggler, MDBIcon, MDBCollapse } from 'mdb-react-ui-kit';

export default function Navbar({ isAuthenticated, username, setIsAuthenticated, setUsername }) {
  const [showNav, setShowNav] = React.useState(false);

  return (
    <MDBNavbar expand='lg' light bgColor='light'>
      <MDBContainer fluid>
        <MDBNavbarBrand href='#'>FieldMaster</MDBNavbarBrand>
        <MDBNavbarToggler
          type='button'
          data-target='#navbarToggleExternalContent'
          aria-controls='navbarToggleExternalContent'
          aria-expanded='false'
          aria-label='Toggle navigation'
          onClick={() => setShowNav(!showNav)}
        >
          <MDBIcon icon='bars' fas />
        </MDBNavbarToggler>
        <MDBCollapse navbar show={showNav}>
          <MDBNavbarNav right fullWidth={false} className='mb-2 mb-lg-0'>
            <MDBNavbarItem>
              <MDBNavbarLink href='/'>Home</MDBNavbarLink>
            </MDBNavbarItem>
            {isAuthenticated ? (
              <>
                <MDBNavbarItem>
                  <MDBNavbarLink href='/user_profile'>User Profile</MDBNavbarLink>
                </MDBNavbarItem>
                <MDBNavbarItem>
                  <MDBNavbarLink href='/map'>Add Land</MDBNavbarLink>
                </MDBNavbarItem>
                <MDBNavbarItem>
                  <MDBNavbarLink href='/analysis'>Get Suggestion</MDBNavbarLink>
                </MDBNavbarItem>
                <MDBNavbarItem>
                  <MDBNavbarLink href='/logout'>Log Out</MDBNavbarLink>
                </MDBNavbarItem>
              </>
            ) : (
              <>
                <MDBNavbarItem>
                  <MDBNavbarLink href='/login'>Login</MDBNavbarLink>
                </MDBNavbarItem>
                <MDBNavbarItem>
                  <MDBNavbarLink href='/register'>Register</MDBNavbarLink>
                </MDBNavbarItem>
              </>
            )}
            <MDBNavbarItem className='ms-auto'>
              <span className='navbar-text'>{isAuthenticated ? 'User' : 'None'}</span>
            </MDBNavbarItem>
          </MDBNavbarNav>
        </MDBCollapse>
      </MDBContainer>
    </MDBNavbar>
  );
}
