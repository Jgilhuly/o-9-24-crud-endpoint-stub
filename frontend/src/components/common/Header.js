import React from 'react';

const Header = ({ title = "CRUD App" }) => {
  return (
    <header className="header">
      <div className="container">
        <div className="header-content">
          <h1 className="header-title">{title}</h1>
          <nav className="nav">
            <a href="/" className="nav-link">Products</a>
            <a href="/users" className="nav-link">Users</a>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;
