# 🛡️ StockGuard

### Inventory Management & Stock Reservation API

**StockGuard** is an inventory management, stock reservation, and booking platform built to manage product data, monitor stock levels, maintain accurate inventory movements, and support reservation workflows.

The project focuses on backend engineering practices, data integrity, transaction management, and reliable stock management using a modern Python-based technology stack.

---

## 🚀 Project Overview

StockGuard provides an API-driven inventory management system with a web-based frontend.

Its main objectives are:
- Maintain consistent inventory quantities.
- Support stock adjustments and reservation workflows.
- Manage users, roles, and permissions.
- Provide secure and structured access control.
- Maintain data integrity through database constraints and transaction handling.

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

### User Management & RBAC
- [x] User model
- [x] Role model
- [x] Permission model
- [x] User-role association model
- [x] Role-permission association model
- [x] ORM relationships using SQLAlchemy
- [x] Initial Alembic migration generated and reviewed
- [ ] Customer-specific profile (`UserCustomer`)
- [ ] User registration
- [ ] User authentication
- [ ] Role and permission assignment workflows
- [ ] Backend permission enforcement

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
- [x] Product detail
- [x] Product information
- [x] Product update
- [x] Product deactivation (soft delete)
- [x] Inventory overview
- [x] Inventory detail
- [x] Product-specific stock movement history
- [x] Stock adjustment form
- [x] Product selection for stock adjustment
- [x] INCREASE / DECREASE selection
- [x] Stock adjustment submission
- [x] Submission loading state and double-submit prevention
- [x] Success and error notifications
- [x] Form reset after successful adjustment

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
| HTTP Client | Axios |
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

### User Management & RBAC

StockGuard uses a Role-Based Access Control (RBAC) foundation.

The current design separates user identity, role assignment, and permission definitions.

| Model | Responsibility |
|---|---|
| `User` | Stores user identity and authentication-related data |
| `Role` | Defines user roles such as ADMIN, STAFF, and CUSTOMER |
| `Permission` | Defines application permissions |
| `UserRole` | Associates users with roles |
| `RolePermission` | Associates roles with permissions |

The association tables use composite primary keys to prevent duplicate assignments.

The `UserRole` model also records:

- `assigned_by`: User who assigned the role
- `assigned_at`: Role assignment timestamp

The current ORM relationships use SQLAlchemy `relationship()` and `back_populates` to support bidirectional object navigation.

### Customer Profile

A separate `UserCustomer` profile is planned for customer-specific information.

This keeps common identity and authentication data in `User`, while optional customer information is maintained separately.

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

| Method | Endpoint | Description |
|---|---|---|
| POST | `/stocks/products/{product_id}/stock-adjustments` | Create a stock adjustment |

Supported movement types:

| Movement | Description |
|---|---|
| `INCREASE` | Add stock quantity |
| `DECREASE` | Reduce stock quantity |

### Stock Movement

| Method | Endpoint | Description |
|---|---|---|
| GET | `/stocks` | Retrieve latest stock movements |
| GET | `/stocks/{product_id}` | Retrieve stock movements by product |

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
- [x] Product detail frontend
- [x] Product update and deactivation frontend
- [x] Stock adjustment frontend
- [x] User Management and RBAC database models
- [x] Initial User Management and RBAC migration generation
- [ ] Customer profile model (`UserCustomer`)
- [ ] User registration and authentication
- [ ] Role and permission management workflows
- [ ] Backend authorization enforcement
- [ ] Stock reservation workflow
- [ ] Booking management
- [ ] Automated integration testing

---

## 🎯 Project Goals

StockGuard is also a practical engineering project focused on:

- RESTful API design
- Clean separation of concerns
- Database transaction management
- Concurrency control
- Inventory consistency
- Role-Based Access Control (RBAC)
- Backend and frontend integration
- Scalable application architecture

---

## 📌 Project Status

**Active Development**

StockGuard is currently under development. Product Management, Inventory Management, and Stock Adjustment features have been implemented. User Management and RBAC database models have been defined, with their initial migration generated and reviewed.

Authentication, authorization enforcement, customer profiles, and stock reservation workflows remain under development.

---

*Built with Python, FastAPI, PostgreSQL, and React.*
