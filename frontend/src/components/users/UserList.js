import React, { useState, useEffect } from 'react';
import { userService } from '../../services/userService';
import UserCard from './UserCard';
import UserForm from './UserForm';
import LoadingSpinner from '../common/LoadingSpinner';

const UserList = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [editingUser, setEditingUser] = useState(null);

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    try {
      setLoading(true);
      const data = await userService.getAllUsers();
      setUsers(data);
      setError(null);
    } catch (err) {
      setError('Failed to load users');
      console.error('Error loading users:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateUser = async (userData) => {
    try {
      const newUser = await userService.createUser(userData);
      setUsers([...users, newUser]);
      setShowForm(false);
    } catch (err) {
      setError('Failed to create user');
      console.error('Error creating user:', err);
    }
  };

  const handleUpdateUser = async (id, userData) => {
    try {
      const updatedUser = await userService.updateUser(id, userData);
      setUsers(users.map(u => u.id === id ? updatedUser : u));
      setEditingUser(null);
    } catch (err) {
      setError('Failed to update user');
      console.error('Error updating user:', err);
    }
  };

  const handleDeleteUser = async (id) => {
    if (window.confirm('Are you sure you want to delete this user?')) {
      try {
        await userService.deleteUser(id);
        setUsers(users.filter(u => u.id !== id));
      } catch (err) {
        setError('Failed to delete user');
        console.error('Error deleting user:', err);
      }
    }
  };

  const handleEditClick = (user) => {
    setEditingUser(user);
    setShowForm(true);
  };

  const handleFormClose = () => {
    setShowForm(false);
    setEditingUser(null);
  };

  if (loading) {
    return <LoadingSpinner text="Loading users..." />;
  }

  if (error) {
    return (
      <div className="container">
        <div className="alert alert-error">
          {error}
          <button onClick={loadUsers} className="btn btn-secondary mt-2">
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="list-header">
        <h2 className="list-title">Users</h2>
        <div className="list-actions">
          <button 
            className="btn btn-primary"
            onClick={() => setShowForm(true)}
          >
            Add User
          </button>
        </div>
      </div>

      {users.length === 0 ? (
        <div className="empty-state">
          <div className="empty-state-icon">👥</div>
          <h3 className="empty-state-title">No Users Found</h3>
          <p className="empty-state-description">
            Get started by adding your first user.
          </p>
          <button 
            className="btn btn-primary"
            onClick={() => setShowForm(true)}
          >
            Add User
          </button>
        </div>
      ) : (
        <div className="grid grid-3">
          {users.map(user => (
            <UserCard
              key={user.id}
              user={user}
              onEdit={handleEditClick}
              onDelete={handleDeleteUser}
            />
          ))}
        </div>
      )}

      {showForm && (
        <UserForm
          user={editingUser}
          onSubmit={editingUser ? 
            (data) => handleUpdateUser(editingUser.id, data) :
            handleCreateUser
          }
          onClose={handleFormClose}
        />
      )}
    </div>
  );
};

export default UserList;
