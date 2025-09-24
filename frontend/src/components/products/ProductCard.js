import React from 'react';

const ProductCard = ({ product, onEdit, onDelete }) => {
  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(price);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  return (
    <div className="item-card">
      <div className="item-card-header">
        <h3 className="item-card-title">{product.name}</h3>
        <div className="item-card-price">{formatPrice(product.price)}</div>
      </div>
      
      <div className="item-card-meta">
        <span className={`status-indicator ${product.in_stock ? 'status-in-stock' : 'status-out-of-stock'}`}></span>
        {product.in_stock ? 'In Stock' : 'Out of Stock'}
        <span style={{ margin: '0 10px' }}>•</span>
        {product.category}
        <span style={{ margin: '0 10px' }}>•</span>
        Added {formatDate(product.created_at)}
      </div>

      <p className="item-card-description">{product.description}</p>

      {product.tags && product.tags.length > 0 && (
        <div className="item-card-tags">
          {product.tags.map((tag, index) => (
            <span key={index} className="item-card-tag">{tag}</span>
          ))}
        </div>
      )}

      <div className="item-card-actions">
        <button 
          className="btn btn-secondary btn-small"
          onClick={() => onEdit(product)}
        >
          Edit
        </button>
        <button 
          className="btn btn-danger btn-small"
          onClick={() => onDelete(product.id)}
        >
          Delete
        </button>
      </div>
    </div>
  );
};

export default ProductCard;
