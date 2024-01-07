# E-commerce API

This E-commerce API is a comprehensive solution for managing an online store. It's built using Django and Django Rest Framework, following RESTful principles.

## Features

### 1. User Authentication

- Endpoints for user registration, login, and logout.
- Token-based authentication for access control.
- Password reset functionality with an email link (simulated using Mailtrap).
- Simple JWT for Token Authentication.

### 2. Product Management

- Retrieve all products and individual product details.
- Products include name, description, price, and stock quantity.
- Read-only access for clients.
- Pagination to display a subset of products on pages.
- Filtering by name, category, min and max price using Django filter.

### 3. Order Management

- Authenticated users can place orders and view their own orders.
- Admin users can view all orders, update order information, or delete orders.
- Orders consist of multiple order items linked to products.
- Checks for product stock availability before placing an order.
- Updates stock quantity after an order is placed.

### 4. Admin Features

- Admin users have additional privileges.
- They can view all orders, while regular users can only view their own orders.
- Controlled by permission classes in API views.

### 5. Error Handling

- Graceful error handling with meaningful error messages and status codes.
- For example, when a user tries to order an out-of-stock product.

### 6. Documentation

- Well-documented API endpoints with details such as HTTP method, URL, required parameters, and example requests.
- Comprehensive Postman collection for interactive documentation: [Postman Collection](https://documenter.getpostman.com/view/26828971/2s9YsJAryg).

## Project Details

This E-commerce API is a robust and flexible solution designed for ease of use by developers, providing a smooth and secure experience for end-users.

## Getting Started

Follow these steps to get started with the E-commerce API:

1. Clone the repository.
2. Set up the virtual environment.
3. Install the required dependencies.
4. Apply database migrations.
5. Run the development server.

For more instructions, refer to the [documentation](link-to-your-documentation).

