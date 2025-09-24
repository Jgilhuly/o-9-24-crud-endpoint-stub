import React, { useState } from 'react';
import Header from './components/common/Header';
import ProductList from './components/products/ProductList';
import UserList from './components/users/UserList';
import './styles/global.css';
import './styles/forms.css';
import './styles/components.css';

function App() {
  const [currentView, setCurrentView] = useState('products');

  const renderCurrentView = () => {
    switch (currentView) {
      case 'users':
        return <UserList />;
      case 'products':
      default:
        return <ProductList />;
    }
  };

  return (
    <div className="App">
      <Header title="CRUD App" />
      <main>
        <div className="container">
          <nav className="nav" style={{ marginBottom: '2rem', justifyContent: 'center' }}>
            <button 
              className={`nav-link ${currentView === 'products' ? 'active' : ''}`}
              onClick={() => setCurrentView('products')}
              style={{ background: 'none', border: 'none', cursor: 'pointer' }}
            >
              Products
            </button>
            <button 
              className={`nav-link ${currentView === 'users' ? 'active' : ''}`}
              onClick={() => setCurrentView('users')}
              style={{ background: 'none', border: 'none', cursor: 'pointer' }}
            >
              Users
            </button>
          </nav>
        </div>
        {renderCurrentView()}
      </main>
    </div>
  );
}

export default App;
