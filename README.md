# b2b-commerce-api

This project is a FastAPI application designed for B2B commerce, providing endpoints for price retrieval and pricing calculations.

## Features

- **Pricing Endpoint**: Accepts a list of products and returns their pricing information
- **PostgreSQL Database**: Stores price records using SQLAlchemy
- **Docker Support**: Containerized application and database
- **Customer-specific Pricing**: Support for customer and customer group specific prices

## Project Structure

```
b2b-commerce-api
├── src
│   ├── main.py                # Entry point of the FastAPI application
│   ├── config.py              # Configuration settings
│   ├── database               # Contains database models and connection setup
│   ├── routers                # Contains API route definitions
│   ├── schemas                # Contains Pydantic schemas
│   └── services               # Contains business logic for pricing
├── Dockerfile                 # Docker configuration for the API
├── docker-compose.yml         # Docker compose configuration
├── init.sql                   # Database initialization script
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

## Setup Instructions

### Using Docker (Recommended)

1. Clone the repository and navigate to the project directory
2. Create a `.env` file with your database configuration:
   ```
   DATABASE_USERNAME=postgres
   DATABASE_PASSWORD=postgres
   DATABASE_HOST=db
   DATABASE_PORT=5432
   DATABASE_NAME=prices_db
   ```
3. Start the application:
   ```bash
   docker-compose up -d
   ```

### Manual Setup

1. Install PostgreSQL and create a database
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```
3. Update `.env` with your database configuration
4. Run the application:
   ```bash
   uvicorn src.main:app --reload
   ```

## API Endpoints

### Pricing Endpoint
- **URL**: `/pricing`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "currency": "USD",
    "customer_id": "optional-customer-id",
    "customer_group_id": "optional-group-id",
    "request_date": "2024-01-01T00:00:00",
    "products": [
      { "product_id": "product1" }
    ]
  }
  ```
- **Response**: List of prices with customer-specific and generic pricing