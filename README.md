# 🛡️ StockGuard

### Inventory Management & Stock Reservation API

**StockGuard** is an inventory management and stock reservation application built to manage product data, monitor stock levels, and maintain accurate inventory movements.

The project focuses on backend engineering practices, data integrity, and reliable stock management using a modern Python-based technology stack.

---

## 🚀 Project Overview

StockGuard provides an API-driven inventory management system with a web-based frontend.

Its main objective is to ensure that stock quantities remain consistent while supporting stock adjustments and future reservation workflows.

## ✨ Features

### Product Management
- [x] Create new products
- [x] Retrieve product list
- [x] Retrieve product details
- [x] View product inventory information
- [x] Update product information
- [x] Soft delete products using `is_active`

### Inventory Management
- [x] Automatic inventory initialization when creating a product
- [x] Stock increase
- [x] Stock decrease
- [x] Available stock calculation
- [x] Reserved stock validation
- [x] Stock movement history
- [x] Database row locking using `SELECT FOR UPDATE`

### Data Validation & Integrity
- [x] Duplicate SKU prevention
- [x] Non-negative stock validation
- [x] Reserved quantity cannot exceed on-hand quantity
- [x] Insufficient stock protection
- [x] Database constraints
- [x] Transaction handling

### Frontend
- [x] Dashboard
- [x] Product listing
- [x] Product creation
- [x] Latest stock movement overview

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| ORM | SQLAlchemy 2.0 |
| Database | PostgreSQL |
| Migration | Alembic |
| Validation | Pydantic |
| Frontend | React |
| Build Tool | Vite |
| Styling | Tailwind CSS |
| HTTP Client | Fetch API / Axios (migration in progress) |
| API Documentation | Swagger UI |

---

## 🏗️ Architecture

StockGuard follows a layered backend architecture to separate HTTP handling, business logic, and database operations.

```text
              CLIENT
                |
                v
        React + Vite Frontend
                |
                v
           HTTP Request
                |
                v
          FastAPI Router
                |
                v
          Service Layer
                |
                v
       SQLAlchemy ORM Layer
                |
                v
           PostgreSQL
```

### Backend Responsibilities

| Layer | Responsibility |
|---|---|
| Router | HTTP endpoints and response handling |
| Schema | Request validation and response serialization |
| Service | Business logic and transaction handling |
| Model | Database structure and relationships |
| Database | Persistent data storage |

---

## 📦 Core Data Concepts

### Product

Stores product information such as:

- Product ID
- SKU
- Product name
- Description
- Unit price
- Active status

### Inventory

Maintains the current stock position of each product.

| Field | Description |
|---|---|
| `on_hand` | Physical stock quantity |
| `reserved_qty` | Quantity reserved for transactions |
| `available_qty` | Stock available for new reservations |

Available stock is calculated using:

```python
available_qty = on_hand - reserved_qty
```

### StockMovement

Records inventory changes, including:

- Movement type (`INCREASE` / `DECREASE`)
- Quantity
- Previous stock
- New stock
- Reason for adjustment

---

## 🔌 API Overview

Base URL:

```text
http://localhost:8000/api/v1
```

### Product Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/products` | Create product |
| GET | `/products` | Retrieve active products |
| GET | `/products/{product_id}` | Retrieve product details and inventory |
| PUT | `/products/{product_id}` | Update product information |
| DELETE | `/products/{product_id}` | Deactivate product (soft delete) |

### Stock Adjustment

Stock adjustments support two movement types:

| Movement | Description |
|---|---|
| `INCREASE` | Add stock quantity |
| `DECREASE` | Reduce stock quantity |

Stock adjustments are validated against available inventory to prevent invalid stock operations.

---

## 🔐 Data Integrity & Concurrency

StockGuard uses database-level constraints and transaction handling to protect inventory consistency.

One important implementation is row-level locking:

```python
select(Inventory).where(
    Inventory.product_id == product_id
).with_for_update()
```

This helps prevent concurrent stock operations from modifying the same inventory record without proper synchronization.

The system also validates that:

```text
on_hand >= 0
reserved_qty >= 0
reserved_qty <= on_hand
```

---

## 🖥️ Running the Application

### Backend

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure your environment variables in `.env` according to your database configuration.

Run database migrations:

```bash
alembic upgrade head
```

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Backend API:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

### Frontend

Navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

## 🗺️ Roadmap

- [x] Initial backend setup
- [x] PostgreSQL integration
- [x] Product CRUD
- [x] Inventory initialization
- [x] Stock adjustment
- [x] Stock movement tracking
- [x] Dashboard
- [x] Product management frontend
- [ ] Product detail frontend
- [ ] Product update and deactivation frontend
- [ ] Stock adjustment frontend
- [ ] Stock reservation workflow
- [ ] Booking management
- [ ] Authentication and authorization
- [ ] Automated integration testing

---

## 🎯 Project Goals

StockGuard is also a practical engineering project focused on:

- RESTful API design
- Clean separation of concerns
- Database transaction management
- Concurrency control
- Inventory consistency
- Backend and frontend integration
- Scalable application architecture

---

## 📌 Project Status

**Active Development**

StockGuard is currently under development. Features and architecture may evolve as new modules are implemented.

---

*Built with Python, FastAPI, PostgreSQL, and React.*
