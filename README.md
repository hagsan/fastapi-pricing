# b2b-commerce-api

This project is a FastAPI application designed for B2B commerce, providing endpoints for price retrieval and cart calculations.

## Features

- **Price Management**: GET and POST endpoints for price retrieval and creation
- **Cart Calculations**: Shopping cart total calculation with customer-specific pricing
- **SQLite/PostgreSQL Support**: Flexible database backend using SQLAlchemy
- **Customer-specific Pricing**: Support for customer and customer group specific prices

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs with Python
- **SQLAlchemy**: SQL toolkit and ORM for database operations
- **Pydantic**: Data validation using Python type annotations
- **PostgreSQL/SQLite**: Database backends
- **Docker**: Containerization and deployment
- **uvicorn**: ASGI server for running the FastAPI application

## API Endpoints

### Price Endpoints
- **GET** `/prices`
  ```json
  {
    "currency": "EUR",
    "customer_id": "optional",
    "customer_group_id": "optional",
    "request_date": "2024-01-01T00:00:00",
    "products": [
      { "product_id": "PROD1" }
    ]
  }
  ```

- **POST** `/prices`
  ```json
  {
    "product_id": "PROD1",
    "amount": 99.99,
    "currency": "EUR",
    "customer_id": "optional",
    "customer_group_id": "optional",
    "valid_from": "2024-01-01T00:00:00",
    "valid_to": "2024-12-31T23:59:59"
  }
  ```

### Cart Endpoint
- **POST** `/cart/calculate`
  ```json
  {
    "items": [
      {
        "product_id": "PROD1",
        "quantity": 2
      }
    ],
    "currency": "EUR",
    "customer_id": "optional",
    "customer_group_id": "optional",
    "request_date": "2024-01-01T00:00:00"
  }
  ```

## Setup Instructions

### Database Configuration

Create a `.env` file in the project root:
```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/prices_db
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_NAME=prices_db
```

### Development Setup
1. Create a virtual environment:
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

2. Install dependencies:
   pip install -r requirements.txt

3. Run the application:
   uvicorn src.main:app --reload

## Development with Docker

1. Start the development environment:
   docker-compose up -d

2. View logs:
   docker-compose logs -f api

3. Run tests in container:
   docker-compose exec api pytest tests/ -v

4. Access the API:
   - API: http://localhost:8080
   - Swagger UI: http://localhost:8080/docs