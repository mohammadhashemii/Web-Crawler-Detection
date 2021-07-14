import React from 'react';
import { Nav, NavLink} from './NavbarElements';

const Navbar = () => {
  return (
    <>
      <Nav>
        <NavLink to='/'>Web Crawler Detection</NavLink>
      </Nav>
    </>
  );
};

export default Navbar;
