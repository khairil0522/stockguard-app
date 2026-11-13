# 🛡️ StockGuard

### Inventory Management & Stock Reservation API

**StockGuard** is an inventory management, stock reservation, and booking platform built to manage product data, monitor stock levels, maintain accurate inventory movements, and support reservation workflows.

The project focuses on backend engineering practices, data integrity, transaction management, concurrency control, and reliable stock management using a modern Python-based technology stack.

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
- [x] Reactivate inactive products

### Product Image Storage

- [x] Upload product image to private AWS S3 bucket
- [x] Image validation (JPEG, PNG, WebP, Max size 5MB)
- [x] Store S3 object key in PostgreSQL
- [x] Generate temporary presigned URL
- [x] Delete product image without deleting product

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
- [x] Customer profile model (`UserCustomer`)
- [x] ORM relationships using SQLAlchemy
- [x] Initial Alembic migration generated and reviewed
- [x] UserCustomer Alembic migration applied
- [x] User registration
- [x] User authentication
- [x] User creation
- [x] User retrieval
- [x] User update
- [x] User soft deactivation
- [x] Backend permission enforcement
- [x] Role and permission assignment workflows
- [ ] User blocking

### Role Management

- [x] Role listing
- [x] Role detail
- [x] Custom role creation
- [x] Role update
- [x] Role activation/deactivation
- [x] Protected system role handling

### Role-Permission Management

- [x] Retrieve all permissions for a role
- [x] Show permission assignment status
- [x] Assign permissions to a role
- [x] Bulk permission assignment
- [x] Remove permissions from a role
- [x] Prevent duplicate role-permission assignments
- [x] Return `assigned=true/false` state for frontend dual-list UI
- [x] Role management API
- [x] User role assignment API
- [x] Role-permission management API
- [x] Permission assignment/removal

### Data Validation & Integrity

- [x] Duplicate SKU prevention
- [x] Non-negative stock validation
- [x] Reserved quantity cannot exceed on-hand quantity
- [x] Insufficient stock protection
- [x] Database constraints
- [x] Transaction handling
- [x] Row-level locking for concurrent stock adjustments

### Reservation & Booking

- [x] Booking creation
- [x] Stock reservation during booking
- [x] Booking item management
- [x] Booking expiration timestamp
- [x] Booking confirmation
- [x] Booking cancellation
- [x] Booking expiration logic
- [x] Customer booking ownership filtering
- [x] Admin booking overview
- [x] Booking retrieval with items

### Frontend

- [x] Dashboard
- [x] Product listing
- [x] Product creation
- [x] Product detail
- [x] Product information
- [x] Product update
- [x] Product deactivation (soft delete)
- [x] Product reactivation
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
| Storage | AWS S3 |
| AWS SDK | Boto3 |

---

## 🏗️ Architecture

StockGuard follows a layered backend architecture with asynchronous database access to separate HTTP handling, business logic, and database operations.

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
                    FastAPI Application
                           |
                           v
                  API Router Aggregator
                    /api/v1/router.py
                           |
                           v
                    Feature Router
                           |
                           v
                    Service Layer
                           |
                           v
              SQLAlchemy Async ORM Layer
                           |
                           v
                      PostgreSQL
```

### Request Flow

```text
Client
  ↓
React + Vite
  ↓
HTTP Request
  ↓
FastAPI Router
  ↓
Feature Router
  ↓
Service Layer
  ↓
Async SQLAlchemy
  ↓
PostgreSQL
  ↓
Response
```

### Product Image Request Flow

```
React
  ↓
FastAPI Router
  ↓
ProductService
  ↓
StorageService
  ↓
AWS S3
```

### Product Image metadata

```
ProductService
  ↓
PostgreSQL
  ↓
image_key
```

### Booking Business Logic

Booking access rules are handled in the service layer rather than the router.

The booking service determines the booking scope based on the authenticated user's role:

```text
Request
  ↓
Booking Router
  ↓
BookingService
  ↓
Check user roles
  ├── CUSTOMER
  │     ↓
  │   Filter by user_id
  │
  └── ADMIN / other authorized roles
        ↓
      Retrieve all bookings
```

The router is responsible for request routing and passing the authenticated user's ID to the service. Business rules remain inside the service layer.

### Backend Responsibilities

| Layer | Responsibility |
|---|---|
| Main Application | FastAPI application setup, middleware, and router registration |
| Router Aggregator | Combines versioned API routers under `/api/v1` |
| Feature Router | Handles HTTP endpoints and response mapping |
| Schema | Request validation and response serialization |
| Service | Business logic, transactions, and database operations |
| Model | Database structure and relationships |
| Database | Persistent data storage |
| Errors | List of Error when the application catch Exceptions |
| Storage Service | Handles object storage operations such as upload, delete, and presigned URL generation |

### Async Database Architecture

StockGuard uses SQLAlchemy 2.0 with `AsyncSession` for asynchronous database access.

The database session is provided through FastAPI dependency injection:

```python
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as db:
        yield db
```

Database I/O operations use `await`, while SQLAlchemy query construction remains synchronous. 

Examples:

```python
result = await db.scalars(statement)
items = result.all()
```

and:

```python
inventory = await db.scalar(
    select(Inventory)
    .where(Inventory.product_id == product_id)
    .with_for_update()
)
```

#### Transaction Handling Convention

StockGuard uses explicit transaction handling for service-layer write operations.

For protected CRUD endpoints that use `require_permission(...)`, avoid opening a new transaction with `async with db.begin()` because the authorization dependency may already perform database queries using the same `AsyncSession`.

For simple write operations, use:

```python
db.add(entity)
await db.commit()
await db.refresh(entity)

For read-only operations, no explicit transaction management is required.

async with db.begin() should be reserved for operations that require multiple database changes to succeed or fail atomically as a single transaction.



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
- Image key

Products use soft deactivation through the `is_active` field.

Product status is managed through:

```text
PATCH /products/{product_id}/status
```

with an explicit status value:

```json
{
  "is_active": false
}
```

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
- Available stock
- Reason for adjustment

### Booking

A `Booking` represents a customer reservation for one or more products.

Each booking contains:

- `booking_code`
- `booking_status`
- `user_id`
- `expired_at`
- `created_at`
- `updated_at`

Booking statuses:

```text
PENDING
CONFIRMED
CANCELLED
EXPIRED
```

A booking can contain multiple BookingItem records.

Each booking item stores:
- product_id
- qty
- unit_price

The unit_price is stored at booking time to preserve the price used for the transaction.

Booking & Inventory Reservation
When a booking is created:

Booking
   ↓
Lock Inventory Row
   ↓
Check Available Stock
   ↓
Increase reserved_qty
   ↓
Create BookingItem

Available stock is calculated as:
available_qty = on_hand - reserved_qty

When a booking is confirmed:
reserved_qty -= qty
on_hand      -= qty

When a booking is cancelled or expired:
reserved_qty -= qty

This prevents reserved inventory from being consumed or released incorrectly during the booking lifecycle.

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

## Authentication & Authorization

StockGuard uses JWT-based authentication and backend-enforced authorization.

### Authentication

- `POST /api/v1/auth/login` — authenticate user and obtain JWT access token.
- `GET /api/v1/auth/me` — retrieve the currently authenticated user.
- `GET /api/v1/auth/roles` — retrieve roles assigned to the authenticated user.
- `GET /api/v1/auth/permissions` — retrieve permissions available to the authenticated user.
- `POST /api/v1/auth/register` — register new user for customer role on purpose.

Authentication uses the HTTP Bearer token scheme.

### Authorization

Authorization is enforced at the backend using role-based permissions.

The `require_permission()` dependency checks whether the authenticated user has the required permission before the endpoint executes.

Examples:

- `dashboard.read`

A valid JWT without the required permission results in HTTP `403 Forbidden`.

Invalid, expired, malformed, or inactive-user authentication attempts result in HTTP `401 Unauthorized`.

A user with the `*` permission is treated as having full permission access.

### Customer Profile

`UserCustomer` stores customer-specific profile information separately from the common `User` identity.

This keeps common identity and authentication-related data in `User`, while customer-specific information is maintained in a dedicated profile.

Current customer profile fields include:

- `phone_number`
- `address`
- `company_name`

A customer profile belongs to one `User`, while each `User` can have zero or one `UserCustomer` profile.

---

## 🔌 API Overview

Base URL:

```text
http://localhost:8000/api/v1
```

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/login` | Authenticate user and obtain JWT access token |
| POST | `/api/v1/auth/register` | Register new customer |
| GET | `/api/v1/auth/me` | Get authenticated user information |
| GET | `/api/v1/auth/roles` | Get authenticated user's roles |
| GET | `/api/v1/auth/permissions` | Get authenticated user's permissions

### Role Management

| Method | Endpoint | Permission | Description |
|---|---|---|---|
| GET | `/roles/` | `role.read` | Retrieve roles |
| GET | `/roles/{role_id}` | `role.read` | Retrieve role |
| POST | `/roles/` | `role.create` | Create custom role |
| PATCH | `/roles/{role_id}` | `role.update` | Update role |
| PATCH | `/roles/{role_id}/status` | `role.status` | Activate/deactivate role |

### Role-Permission Management

| Method | Endpoint | Permission | Description |
|---|---|---|---|
| GET | `/roles/{role_id}/permissions` | `permission.manage` | Retrieve permissions and assignment status |
| POST | `/roles/{role_id}/permissions` | `permission.manage` | Assign permissions |
| DELETE | `/roles/{role_id}/permissions` | `permission.manage` | Remove permissions |

### Product Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/products` | Create product |
| GET | `/products` | Retrieve active products |
| GET | `/products/{product_id}` | Retrieve product details and inventory |
| PUT | `/products/{product_id}` | Update product information |
| PATCH | `/products/{product_id}/status` | Activate or deactivate product |

Product deactivation is implemented as a soft delete using `is_active`.

### Product Image Endpoints
| Method | Endpoint | Description |
|---|---|---|
| POST | `/products/{product_id}/image` | Upload/replace product image |
| GET | `/products/{product_id}/image` | Generate temporary presigned URL |
| DELETE | `/products/{product_id}/image` | Remove product image |


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
| GET | `/stocks/` | Retrieve latest stock movements |
| GET | `/stocks/{product_id}` | Retrieve stock movements by product |

Stock adjustments are validated against inventory state to prevent invalid stock operations.

### Booking

| Method | Endpoint | Description |
|---|---|---|
| POST | `/bookings` | Create a new booking |
| GET | `/bookings` | Retrieve bookings based on user role |
| POST | `/bookings/{booking_id}/confirm` | Confirm a pending booking |
| POST | `/bookings/{booking_id}/cancel` | Cancel a pending booking |
| POST | `/bookings/{booking_id}/expire` | Expire a pending booking |

Booking behavior:

- `CUSTOMER` can only retrieve their own bookings.
- `ADMIN` and higher-level roles can retrieve all bookings.
- Booking creation automatically reserves inventory.
- Booking confirmation converts reserved stock into consumed stock.
- Booking cancellation releases reserved stock.
- Booking expiration releases reserved stock.

### User Management

| Method | Endpoint | Permission | Description |
|---|---|---|---|
| GET | `/users` | `user.read` | Retrieve users |
| GET | `/users/{user_id}` | `user.read` | Retrieve user details |
| POST | `/users` | `user.create` | Create user |
| PATCH | `/users/{user_id}` | `user.update` | Update user profile |
| PATCH | `/users/{user_id}/role` | `user.assign` | Assign user role |
| DELETE | `/users/{user_id}` | `user.status` | Soft deactivate user |

### Role Assignment Rules

- `SUPERADMIN` cannot create or assign `SUPERADMIN`.
- `ADMIN` cannot create or assign `ADMIN`.
- `ADMIN` cannot create or assign `SUPERADMIN`.
- `ADMIN` can manage `CUSTOMER` and custom roles.
- `SUPERADMIN` can manage `ADMIN`, `CUSTOMER`, and custom roles.
- `SUPERADMIN` is treated as a protected system-level role.

---

## 🔐 Data Integrity & Concurrency

StockGuard uses database-level constraints, transaction handling, and row-level locking to protect inventory consistency.

One important implementation is row-level locking:

```python
select(Inventory).where(
    Inventory.product_id == product_id
).with_for_update()
```

This helps prevent concurrent stock operations from modifying the same inventory record without proper synchronization.

Database transactions are used for stock adjustments and other operations that require atomicity:

```python
async with db.begin():
    ...
```
> **Transaction convention:** Simple protected CRUD operations use explicit `commit()` and `refresh()` after database writes. `async with db.begin()` is reserved for operations that require an explicit atomic transaction boundary, such as multi-step inventory operations.

The system also validates that:

```text
on_hand >= 0
reserved_qty >= 0
reserved_qty <= on_hand
```

For stock decreases, the system prevents the operation when the resulting stock would fall below the reserved quantity.

### Booking Concurrency Control

Booking creation also uses row-level locking on the related inventory record.

```python
select(Inventory).where(
    Inventory.product_id == product_id
).with_for_update()
```

The inventory row is locked before checking and updating reserved_qty.

This ensures that concurrent booking requests cannot reserve the same available stock incorrectly.

Booking creation and reservation updates are handled atomically so that a failed booking does not leave partial reservation data behind.

---

## 🖥️ Running the Application

### Backend

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure your environment variables in `.env` according to your database configuration and AWS S3 policy.

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

### Foundation

- [x] Initial backend setup
- [x] PostgreSQL integration
- [x] SQLAlchemy 2.0 integration
- [x] Async database session refactor
- [x] Alembic migration setup

### Product & Inventory

- [x] Product CRUD
- [x] Inventory initialization
- [x] Stock adjustment
- [x] Stock movement tracking
- [x] Dashboard
- [x] Product management frontend
- [x] Product detail frontend
- [x] Product update and deactivation frontend
- [x] Product reactivation frontend
- [x] Stock adjustment frontend

### Product Image Storage

- [x] Upload product image to private AWS S3 bucket
- [x] Image validation (JPEG, PNG, WebP, Max size 5MB)
- [x] Store S3 object key in PostgreSQL
- [x] Generate temporary presigned URL
- [x] Delete product image without deleting product

### User Management & RBAC

- [x] User Management database models
- [x] Role database model
- [x] Permission database model
- [x] User-role association
- [x] Role-permission association
- [x] UserCustomer profile model
- [x] Initial User Management and RBAC migration
- [x] UserCustomer migration
- [x] User registration
- [x] User authentication
- [x] User retrieval
- [x] User creation
- [x] User update
- [x] User soft deactivation
- [x] Backend authorization enforcement
- [x] Role and permission management workflows
- [x] Role management API
- [x] User role assignment API
- [x] Role-permission management API
- [x] Permission assignment/removal
- [ ] User blocking 

### Reservation & Booking

- [x] Stock reservation workflow
- [x] Booking creation
- [x] Booking item management
- [x] Booking confirmation
- [x] Booking cancellation
- [x] Booking expiration logic
- [x] Customer booking ownership enforcement
- [x] Admin booking overview
- [x] Booking retrieval with items
- [ ] Automatic booking expiration scheduler
- [ ] Booking lifecycle refinement

### Testing

- [x] Unit testing for stock adjustment logic
- [x] Validation and error handling tests
- [ ] Booking integration testing
- [ ] Automated integration testing

---

## 🎯 Project Goals

StockGuard is also a practical engineering project focused on:

- RESTful API design
- Clean separation of concerns
- Database transaction management
- Asynchronous database access
- Concurrency control
- Inventory consistency
- Role-Based Access Control (RBAC)
- Backend and frontend integration
- Scalable application architecture
- Object storage integration (AWS S3)
- Secure temporary file access

---

## 📌 Project Status

**Active Development**

StockGuard currently has the core Product Management, Inventory Management, Stock Adjustment, Reservation & Booking, Dashboard, User Management, Role Management, and RBAC modules implemented.

The Booking module supports stock reservation, booking creation, confirmation, cancellation, expiration logic, customer ownership filtering, and role-based booking retrieval.

JWT authentication and backend authorization enforcement have been implemented, including user role assignment and role-permission management.

AWS S3 product image storage has been implemented, including private bucket storage, image validation, object key persistence, presigned URL access, and product image deletion.

---

*Built with Python, FastAPI, PostgreSQL, AWS S3, Boto3 and React.*