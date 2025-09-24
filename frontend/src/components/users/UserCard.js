import React from 'react';

const UserCard = ({ user, onEdit, onDelete }) => {
  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  return (
    <div className="item-card">
      <div className="item-card-header">
        <h3 className="item-card-title">{user.name}</h3>
      </div>
      
      <div className="item-card-meta">
        <strong>Email:</strong> {user.email}
        <br />
        <strong>Member since:</strong> {formatDate(user.created_at)}
      </div>

      <div className="item-card-actions">
        <button 
          className="btn btn-secondary btn-small"
          onClick={() => onEdit(user)}
        >
          Edit
        </button>
        <button 
          className="btn btn-danger btn-small"
          onClick={() => onDelete(user.id)}
        >
          Delete
        </button>
      </div>
    </div>
  );
};

export default UserCard;
