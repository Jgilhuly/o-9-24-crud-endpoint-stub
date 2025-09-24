"""Unit tests for the FastAPI application endpoints."""
import pytest
from fastapi.testclient import TestClient
from datetime import datetime

from main import app
from models import ProductCreate, ProductUpdate, UserCreate, UserUpdate

# Create test client
client = TestClient(app)


class TestRootEndpoints:
    """Test cases for root and health endpoints."""
    
    def test_read_root(self):
        """Test the root endpoint returns welcome message."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to the Product CRUD API"}
    
    def test_health_check(self):
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


class TestProductEndpoints:
    """Test cases for product CRUD endpoints."""
    
    def test_get_all_products(self):
        """Test getting all products."""
        response = client.get("/products")
        assert response.status_code == 200
        products = response.json()
        assert isinstance(products, list)
        assert len(products) >= 3  # Should have sample data
        
        # Check structure of first product
        if products:
            product = products[0]
            assert "id" in product
            assert "name" in product
            assert "description" in product
            assert "price" in product
            assert "category" in product
            assert "tags" in product
            assert "in_stock" in product
            assert "created_at" in product
    
    def test_get_product_success(self):
        """Test getting a specific product by ID."""
        # First get all products to find a valid ID
        response = client.get("/products")
        products = response.json()
        assert len(products) > 0
        
        product_id = products[0]["id"]
        response = client.get(f"/products/{product_id}")
        assert response.status_code == 200
        
        product = response.json()
        assert product["id"] == product_id
        assert "name" in product
        assert "description" in product
    
    def test_get_product_not_found(self):
        """Test getting a product that doesn't exist."""
        response = client.get("/products/99999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Product not found"
    
    def test_create_product(self):
        """Test creating a new product."""
        product_data = {
            "name": "Test Product",
            "description": "A test product for unit testing",
            "price": 29.99,
            "category": "Test",
            "tags": ["test", "unit-test"],
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
            "description": "Minimal test product",
            "price": 19.99,
            "category": "Minimal"
        }
        
        response = client.post("/products", json=product_data)
        assert response.status_code == 200
        
        product = response.json()
        assert product["name"] == product_data["name"]
        assert product["description"] == product_data["description"]
        assert product["price"] == product_data["price"]
        assert product["category"] == product_data["category"]
        assert product["tags"] == []  # Default empty list
        assert product["in_stock"] == True  # Default True
    
    def test_update_product_success(self):
        """Test updating an existing product."""
        # First create a product
        product_data = {
            "name": "Original Product",
            "description": "Original description",
            "price": 50.00,
            "category": "Original"
        }
        
        create_response = client.post("/products", json=product_data)
        product_id = create_response.json()["id"]
        
        # Update the product
        update_data = {
            "name": "Updated Product",
            "price": 75.00,
            "tags": ["updated", "test"]
        }
        
        response = client.put(f"/products/{product_id}", json=update_data)
        assert response.status_code == 200
        
        updated_product = response.json()
        assert updated_product["id"] == product_id
        assert updated_product["name"] == update_data["name"]
        assert updated_product["price"] == update_data["price"]
        assert updated_product["tags"] == update_data["tags"]
        assert updated_product["description"] == product_data["description"]  # Unchanged
    
    def test_update_product_not_found(self):
        """Test updating a product that doesn't exist."""
        update_data = {"name": "Updated Name"}
        
        response = client.put("/products/99999", json=update_data)
        assert response.status_code == 404
        assert response.json()["detail"] == "Product not found"
    
    def test_delete_product_success(self):
        """Test deleting an existing product."""
        # First create a product
        product_data = {
            "name": "To Delete",
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
        """Test deleting a product that doesn't exist."""
        response = client.delete("/products/99999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Product not found"


class TestUserEndpoints:
    """Test cases for user CRUD endpoints."""
    
    def test_get_all_users(self):
        """Test getting all users."""
        response = client.get("/users")
        assert response.status_code == 200
        users = response.json()
        assert isinstance(users, list)
    
    def test_create_user(self):
        """Test creating a new user."""
        user_data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpassword123"
        }
        
        response = client.post("/users", json=user_data)
        assert response.status_code == 200
        
        user = response.json()
        assert user["name"] == user_data["name"]
        assert user["email"] == user_data["email"]
        assert user["password"] == user_data["password"]
        assert "id" in user
        assert "created_at" in user
    
    def test_get_user_success(self):
        """Test getting a specific user by ID."""
        # First create a user
        user_data = {
            "name": "Get User Test",
            "email": "getuser@example.com",
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
    
    def test_get_user_not_found(self):
        """Test getting a user that doesn't exist."""
        response = client.get("/users/99999")
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"
    
    def test_update_user_success(self):
        """Test updating an existing user."""
        # First create a user
        user_data = {
            "name": "Original User",
            "email": "original@example.com",
            "password": "originalpass"
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
        assert updated_user["id"] == user_id
        assert updated_user["name"] == update_data["name"]
        assert updated_user["email"] == update_data["email"]
        assert updated_user["password"] == user_data["password"]  # Unchanged
    
    def test_update_user_not_found(self):
        """Test updating a user that doesn't exist."""
        update_data = {"name": "Updated Name"}
        
        response = client.put("/users/99999", json=update_data)
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"
    
    def test_delete_user_success(self):
        """Test deleting an existing user."""
        # First create a user
        user_data = {
            "name": "To Delete User",
            "email": "delete@example.com",
            "password": "deletepass"
        }
        
        create_response = client.post("/users", json=user_data)
        user_id = create_response.json()["id"]
        
        # Delete the user
        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["message"] == "User deleted successfully"
        
        # Verify it's deleted
        get_response = client.get(f"/users/{user_id}")
        assert get_response.status_code == 404
    
    def test_delete_user_not_found(self):
        """Test deleting a user that doesn't exist."""
        response = client.delete("/users/99999")
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"


class TestValidationAndEdgeCases:
    """Test cases for validation and edge cases."""
    
    def test_create_product_invalid_data(self):
        """Test creating a product with invalid data."""
        # Missing required fields
        invalid_data = {
            "name": "Incomplete Product"
            # Missing description, price, category
        }
        
        response = client.post("/products", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    def test_create_user_invalid_data(self):
        """Test creating a user with invalid data."""
        # Missing required fields
        invalid_data = {
            "name": "Incomplete User"
            # Missing email, password
        }
        
        response = client.post("/users", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    def test_update_product_partial_data(self):
        """Test updating a product with only some fields."""
        # First create a product
        product_data = {
            "name": "Partial Update Test",
            "description": "Original description",
            "price": 100.00,
            "category": "Original"
        }
        
        create_response = client.post("/products", json=product_data)
        product_id = create_response.json()["id"]
        
        # Update only the name
        update_data = {"name": "Only Name Updated"}
        
        response = client.put(f"/products/{product_id}", json=update_data)
        assert response.status_code == 200
        
        updated_product = response.json()
        assert updated_product["name"] == update_data["name"]
        assert updated_product["description"] == product_data["description"]  # Unchanged
        assert updated_product["price"] == product_data["price"]  # Unchanged
    
    def test_update_user_partial_data(self):
        """Test updating a user with only some fields."""
        # First create a user
        user_data = {
            "name": "Partial Update User",
            "email": "partial@example.com",
            "password": "partialpass"
        }
        
        create_response = client.post("/users", json=user_data)
        user_id = create_response.json()["id"]
        
        # Update only the email
        update_data = {"email": "updatedemail@example.com"}
        
        response = client.put(f"/users/{user_id}", json=update_data)
        assert response.status_code == 200
        
        updated_user = response.json()
        assert updated_user["email"] == update_data["email"]
        assert updated_user["name"] == user_data["name"]  # Unchanged
        assert updated_user["password"] == user_data["password"]  # Unchanged


if __name__ == "__main__":
    pytest.main([__file__])
