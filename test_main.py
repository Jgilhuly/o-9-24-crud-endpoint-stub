"""Comprehensive test suite for FastAPI CRUD application."""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestRootEndpoints:
    """Test basic API endpoints."""
    
    def test_read_root(self):
        """Test root endpoint returns welcome message."""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
        assert "Welcome" in response.json()["message"]
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


class TestProductEndpoints:
    """Test Product CRUD operations."""
    
    def test_get_all_products(self):
        """Test getting all products."""
        response = client.get("/products")
        assert response.status_code == 200
        products = response.json()
        assert isinstance(products, list)
        # Should have sample products
        assert len(products) >= 3
    
    def test_get_product_success(self):
        """Test getting a specific product by ID."""
        response = client.get("/products/1")
        assert response.status_code == 200
        product = response.json()
        assert product["id"] == 1
        assert "name" in product
        assert "description" in product
        assert "price" in product
        assert "category" in product
    
    def test_get_product_not_found(self):
        """Test getting a non-existent product returns 404."""
        response = client.get("/products/999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_create_product_success(self):
        """Test creating a new product with valid data."""
        product_data = {
            "name": "Test Product",
            "description": "A test product for testing",
            "price": 29.99,
            "category": "Test",
            "tags": ["test", "example"],
            "in_stock": True
        }
        response = client.post("/products", json=product_data)
        assert response.status_code == 200
        product = response.json()
        assert product["name"] == product_data["name"]
        assert product["description"] == product_data["description"]
        assert product["price"] == product_data["price"]
        assert product["category"] == product_data["category"]
        assert product["tags"] == product_data["tags"]
        assert product["in_stock"] == product_data["in_stock"]
        assert "id" in product
        assert "created_at" in product
    
    def test_create_product_minimal_data(self):
        """Test creating a product with minimal required data."""
        product_data = {
            "name": "Minimal Product",
            "description": "Minimal description",
            "price": 19.99,
            "category": "Minimal"
        }
        response = client.post("/products", json=product_data)
        assert response.status_code == 200
        product = response.json()
        assert product["name"] == product_data["name"]
        assert product["tags"] == []  # Default empty list
        assert product["in_stock"] is True  # Default True
    
    def test_create_product_validation_error(self):
        """Test creating a product with invalid data."""
        invalid_data = {
            "name": "",  # Empty name should fail
            "description": "Test description",
            "price": -10,  # Negative price should fail
            "category": "Test"
        }
        response = client.post("/products", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    def test_update_product_success(self):
        """Test updating an existing product."""
        # First create a product
        product_data = {
            "name": "Original Product",
            "description": "Original description",
            "price": 25.00,
            "category": "Original"
        }
        create_response = client.post("/products", json=product_data)
        product_id = create_response.json()["id"]
        
        # Update the product
        update_data = {
            "name": "Updated Product",
            "price": 30.00
        }
        response = client.put(f"/products/{product_id}", json=update_data)
        assert response.status_code == 200
        updated_product = response.json()
        assert updated_product["name"] == update_data["name"]
        assert updated_product["price"] == update_data["price"]
        assert updated_product["description"] == product_data["description"]  # Unchanged
    
    def test_update_product_not_found(self):
        """Test updating a non-existent product returns 404."""
        update_data = {"name": "Updated Name"}
        response = client.put("/products/999", json=update_data)
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_update_product_partial(self):
        """Test partial update of a product."""
        # Create a product first
        product_data = {
            "name": "Partial Test Product",
            "description": "Original description",
            "price": 15.00,
            "category": "Test",
            "tags": ["original"],
            "in_stock": True
        }
        create_response = client.post("/products", json=product_data)
        product_id = create_response.json()["id"]
        
        # Update only the price
        update_data = {"price": 20.00}
        response = client.put(f"/products/{product_id}", json=update_data)
        assert response.status_code == 200
        updated_product = response.json()
        assert updated_product["price"] == 20.00
        assert updated_product["name"] == product_data["name"]  # Unchanged
        assert updated_product["tags"] == product_data["tags"]  # Unchanged
    
    def test_delete_product_success(self):
        """Test deleting an existing product."""
        # Create a product first
        product_data = {
            "name": "To Delete Product",
            "description": "This will be deleted",
            "price": 10.00,
            "category": "Temporary"
        }
        create_response = client.post("/products", json=product_data)
        product_id = create_response.json()["id"]
        
        # Delete the product
        response = client.delete(f"/products/{product_id}")
        assert response.status_code == 204
        
        # Verify it's deleted
        get_response = client.get(f"/products/{product_id}")
        assert get_response.status_code == 404
    
    def test_delete_product_not_found(self):
        """Test deleting a non-existent product returns 404."""
        response = client.delete("/products/999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestUserEndpoints:
    """Test User CRUD operations."""
    
    def test_get_all_users(self):
        """Test getting all users."""
        response = client.get("/users")
        assert response.status_code == 200
        users = response.json()
        assert isinstance(users, list)
    
    def test_get_user_success(self):
        """Test getting a specific user by ID."""
        # First create a user
        user_data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123"
        }
        create_response = client.post("/users", json=user_data)
        user_id = create_response.json()["id"]
        
        # Get the user
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200
        user = response.json()
        assert user["id"] == user_id
        assert user["name"] == user_data["name"]
        assert user["email"] == user_data["email"]
        assert "created_at" in user
    
    def test_get_user_not_found(self):
        """Test getting a non-existent user returns 404."""
        response = client.get("/users/999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_create_user_success(self):
        """Test creating a new user with valid data."""
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "securepassword123"
        }
        response = client.post("/users", json=user_data)
        assert response.status_code == 200
        user = response.json()
        assert user["name"] == user_data["name"]
        assert user["email"] == user_data["email"]
        assert user["password"] == user_data["password"]
        assert "id" in user
        assert "created_at" in user
    
    def test_create_user_validation_error(self):
        """Test creating a user with invalid data."""
        invalid_data = {
            "name": "",  # Empty name
            "email": "invalid-email",  # Invalid email format
            "password": "123"  # Too short password
        }
        response = client.post("/users", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    def test_update_user_success(self):
        """Test updating an existing user."""
        # Create a user first
        user_data = {
            "name": "Original User",
            "email": "original@example.com",
            "password": "originalpassword"
        }
        create_response = client.post("/users", json=user_data)
        user_id = create_response.json()["id"]
        
        # Update the user
        update_data = {
            "name": "Updated User",
            "email": "updated@example.com"
        }
        response = client.put(f"/users/{user_id}", json=update_data)
        assert response.status_code == 200
        updated_user = response.json()
        assert updated_user["name"] == update_data["name"]
        assert updated_user["email"] == update_data["email"]
        assert updated_user["password"] == user_data["password"]  # Unchanged
    
    def test_update_user_not_found(self):
        """Test updating a non-existent user returns 404."""
        update_data = {"name": "Updated Name"}
        response = client.put("/users/999", json=update_data)
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_delete_user_success(self):
        """Test deleting an existing user."""
        # Create a user first
        user_data = {
            "name": "User To Delete",
            "email": "delete@example.com",
            "password": "password123"
        }
        create_response = client.post("/users", json=user_data)
        user_id = create_response.json()["id"]
        
        # Delete the user
        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"]
        
        # Verify it's deleted
        get_response = client.get(f"/users/{user_id}")
        assert get_response.status_code == 404
    
    def test_delete_user_not_found(self):
        """Test deleting a non-existent user returns 404."""
        response = client.delete("/users/999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestValidationAndEdgeCases:
    """Test error handling and edge cases."""
    
    def test_invalid_json_format(self):
        """Test sending invalid JSON format."""
        response = client.post(
            "/products",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
    
    def test_missing_required_fields(self):
        """Test creating product with missing required fields."""
        incomplete_data = {
            "name": "Incomplete Product"
            # Missing description, price, category
        }
        response = client.post("/products", json=incomplete_data)
        assert response.status_code == 422
    
    def test_negative_product_id(self):
        """Test using negative product ID."""
        response = client.get("/products/-1")
        assert response.status_code == 404
    
    def test_zero_product_id(self):
        """Test using zero product ID."""
        response = client.get("/products/0")
        assert response.status_code == 404
    
    def test_large_product_id(self):
        """Test using very large product ID."""
        response = client.get("/products/999999999")
        assert response.status_code == 404
    
    def test_empty_string_values(self):
        """Test creating product with empty string values."""
        empty_data = {
            "name": "",
            "description": "",
            "price": 0,
            "category": ""
        }
        response = client.post("/products", json=empty_data)
        assert response.status_code == 422
    
    def test_boundary_price_values(self):
        """Test boundary price values."""
        # Test very small price
        small_price_data = {
            "name": "Small Price Product",
            "description": "Test product",
            "price": 0.01,
            "category": "Test"
        }
        response = client.post("/products", json=small_price_data)
        assert response.status_code == 200
        
        # Test very large price
        large_price_data = {
            "name": "Large Price Product",
            "description": "Test product",
            "price": 999999.99,
            "category": "Test"
        }
        response = client.post("/products", json=large_price_data)
        assert response.status_code == 200
    
    def test_special_characters_in_data(self):
        """Test handling special characters in product data."""
        special_data = {
            "name": "Product with Special Chars: !@#$%^&*()",
            "description": "Description with émojis 🚀 and unicode",
            "price": 25.50,
            "category": "Special & Unique",
            "tags": ["special", "unicode", "émojis"]
        }
        response = client.post("/products", json=special_data)
        assert response.status_code == 200
        product = response.json()
        assert product["name"] == special_data["name"]
        assert product["description"] == special_data["description"]
        assert product["tags"] == special_data["tags"]