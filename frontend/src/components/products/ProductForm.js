import React, { useState, useEffect } from 'react';

const ProductForm = ({ product, onSubmit, onClose }) => {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    price: '',
    category: '',
    tags: '',
    in_stock: true
  });
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (product) {
      setFormData({
        name: product.name || '',
        description: product.description || '',
        price: product.price || '',
        category: product.category || '',
        tags: product.tags ? product.tags.join(', ') : '',
        in_stock: product.in_stock !== undefined ? product.in_stock : true
      });
    }
  }, [product]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Name is required';
    }

    if (!formData.description.trim()) {
      newErrors.description = 'Description is required';
    }

    if (!formData.price || isNaN(formData.price) || parseFloat(formData.price) <= 0) {
      newErrors.price = 'Price must be a positive number';
    }

    if (!formData.category.trim()) {
      newErrors.category = 'Category is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);

    try {
      const submitData = {
        ...formData,
        price: parseFloat(formData.price),
        tags: formData.tags ? formData.tags.split(',').map(tag => tag.trim()).filter(tag => tag) : []
      };

      await onSubmit(submitData);
    } catch (error) {
      console.error('Form submission error:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3 className="modal-title">
            {product ? 'Edit Product' : 'Add New Product'}
          </h3>
          <button className="modal-close" onClick={onClose}>
            ×
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label" htmlFor="name">Name *</label>
            <input
              type="text"
              id="name"
              name="name"
              className={`form-input ${errors.name ? 'is-invalid' : ''}`}
              value={formData.name}
              onChange={handleChange}
              placeholder="Enter product name"
            />
            {errors.name && <div className="form-error">{errors.name}</div>}
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="description">Description *</label>
            <textarea
              id="description"
              name="description"
              className={`form-textarea ${errors.description ? 'is-invalid' : ''}`}
              value={formData.description}
              onChange={handleChange}
              placeholder="Enter product description"
            />
            {errors.description && <div className="form-error">{errors.description}</div>}
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="price">Price *</label>
            <input
              type="number"
              id="price"
              name="price"
              step="0.01"
              min="0"
              className={`form-input ${errors.price ? 'is-invalid' : ''}`}
              value={formData.price}
              onChange={handleChange}
              placeholder="0.00"
            />
            {errors.price && <div className="form-error">{errors.price}</div>}
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="category">Category *</label>
            <input
              type="text"
              id="category"
              name="category"
              className={`form-input ${errors.category ? 'is-invalid' : ''}`}
              value={formData.category}
              onChange={handleChange}
              placeholder="Enter product category"
            />
            {errors.category && <div className="form-error">{errors.category}</div>}
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="tags">Tags</label>
            <input
              type="text"
              id="tags"
              name="tags"
              className="form-input"
              value={formData.tags}
              onChange={handleChange}
              placeholder="Enter tags separated by commas"
            />
            <div className="form-help">Separate multiple tags with commas</div>
          </div>

          <div className="form-group">
            <div className="form-checkbox">
              <input
                type="checkbox"
                id="in_stock"
                name="in_stock"
                checked={formData.in_stock}
                onChange={handleChange}
              />
              <label className="form-label" htmlFor="in_stock">In Stock</label>
            </div>
          </div>

          <div className="form-actions">
            <button 
              type="button" 
              className="btn btn-secondary"
              onClick={onClose}
              disabled={isSubmitting}
            >
              Cancel
            </button>
            <button 
              type="submit" 
              className="btn btn-primary"
              disabled={isSubmitting}
            >
              {isSubmitting ? (
                <>
                  <span className="loading-spinner" style={{ marginRight: '8px' }}></span>
                  {product ? 'Updating...' : 'Creating...'}
                </>
              ) : (
                product ? 'Update Product' : 'Create Product'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ProductForm;
