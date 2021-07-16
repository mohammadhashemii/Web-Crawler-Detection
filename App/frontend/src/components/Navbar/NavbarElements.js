import styled from 'styled-components';
import { NavLink as Link } from 'react-router-dom';

export const Nav = styled.nav`
  background: #f2a000;
  height: 80px;
  display: flex;
  justify-content: center;
  font-weight: 700;
`;

export const NavLink = styled(Link)`
  color: #fff;
  font-size: 2rem;
  display: flex;
  align-items: center;
  text-decoration: none;
  cursor: pointer;
  
`;

export const NavIcon = styled.div`
      display: block;
      position: absolute;
      top: 0;
      right: 0;
      cursor: pointer;
      color: #fff;
    
      p {
        transform: translate(-175%, 100%);
        font-weight: bold;
      }
`;


