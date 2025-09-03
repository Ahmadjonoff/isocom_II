# ISOCOM II API Documentation

This document provides comprehensive documentation for all APIs available in the ISOCOM II project.

## Authentication

The API uses JWT (JSON Web Token) authentication. You need to obtain a token before accessing protected endpoints.

### Authentication Endpoints

#### 1. Obtain Token

```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password"
  }'
```

Response:
```json
{
    "access": "your.access.token",
    "refresh": "your.refresh.token"
}
```

#### 2. Refresh Token

```bash
curl -X POST http://localhost:8000/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "your.refresh.token"
  }'
```

Response:
```json
{
    "access": "new.access.token"
}
```

#### 3. Verify Token

```bash
curl -X POST http://localhost:8000/api/auth/token/verify/ \
  -H "Content-Type: application/json" \
  -d '{
    "token": "your.access.token"
  }'
```

## API Documentation

For interactive API documentation, you can visit:
- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/
- OpenAPI Schema: http://localhost:8000/api/schema/

## User API

All user endpoints require authentication. Include the access token in the Authorization header:
```
Authorization: Bearer your.access.token
```

### List Users

```bash
curl -X GET http://localhost:8000/api/users/ \
  -H "Authorization: Bearer your.access.token"
```

Query Parameters:
- `role`: Filter by user role
- `is_active`: Filter by active status
- `shift`: Filter by shift
- `search`: Search in username, first_name, last_name, email, phone_number
- `ordering`: Order by id, username, first_name, last_name

### Get Single User

```bash
curl -X GET http://localhost:8000/api/users/{id}/ \
  -H "Authorization: Bearer your.access.token"
```

### Create User

```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "password": "userpassword",
    "first_name": "First",
    "last_name": "Last",
    "email": "user@example.com",
    "phone_number": "+1234567890",
    "role": "worker",
    "shift": "day"
  }'
```

### Update User

```bash
curl -X PUT http://localhost:8000/api/users/{id}/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "updateduser",
    "first_name": "Updated",
    "last_name": "Name",
    "email": "updated@example.com",
    "phone_number": "+1234567890",
    "role": "worker",
    "shift": "night"
  }'
```

### Partial Update User

```bash
curl -X PATCH http://localhost:8000/api/users/{id}/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "shift": "night"
  }'
```

### Delete User

```bash
curl -X DELETE http://localhost:8000/api/users/{id}/ \
  -H "Authorization: Bearer your.access.token"
```

## Workcenter API

All workcenter endpoints require authentication.

### List Workcenters

```bash
curl -X GET http://localhost:8000/api/workcenters/ \
  -H "Authorization: Bearer your.access.token"
```

Query Parameters:
- `type`: Filter by workcenter type
- `is_active`: Filter by active status
- `search`: Search in name, description, location
- `ordering`: Order by id, name, last_maintenance_date

### Get Single Workcenter

```bash
curl -X GET http://localhost:8000/api/workcenters/{id}/ \
  -H "Authorization: Bearer your.access.token"
```

### Create Workcenter

```bash
curl -X POST http://localhost:8000/api/workcenters/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Assembly Line 1",
    "description": "Main assembly line",
    "type": "assembly",
    "location": "Building A",
    "is_active": true,
    "last_maintenance_date": "2024-03-20"
  }'
```

### Update Workcenter

```bash
curl -X PUT http://localhost:8000/api/workcenters/{id}/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Assembly Line 1",
    "description": "Updated assembly line",
    "type": "assembly",
    "location": "Building B",
    "is_active": true,
    "last_maintenance_date": "2024-03-21"
  }'
```

### Partial Update Workcenter

```bash
curl -X PATCH http://localhost:8000/api/workcenters/{id}/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "location": "Building C"
  }'
```

### Delete Workcenter

```bash
curl -X DELETE http://localhost:8000/api/workcenters/{id}/ \
  -H "Authorization: Bearer your.access.token"
```

## Material API

All material endpoints require authentication.

### List Materials

```bash
curl -X GET http://localhost:8000/api/materials/ \
  -H "Authorization: Bearer your.access.token"
```

Query Parameters:
- `type`: Filter by material type
- `unit_of_measure`: Filter by unit of measure
- `is_active`: Filter by active status
- `price`: Filter by price
- `search`: Search in name, code, slug, description, price
- `ordering`: Order by id, name, code, updated_at, price

### Get Single Material

```bash
curl -X GET http://localhost:8000/api/materials/{id}/ \
  -H "Authorization: Bearer your.access.token"
```

### Create Material

```bash
curl -X POST http://localhost:8000/api/materials/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Steel Sheet",
    "code": "STL-001",
    "slug": "steel-sheet",
    "description": "High-quality steel sheet",
    "type": "raw",
    "unit_of_measure": "kg",
    "price": 100.00,
    "is_active": true
  }'
```

### Update Material

```bash
curl -X PUT http://localhost:8000/api/materials/{id}/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Steel Sheet",
    "code": "STL-001",
    "slug": "steel-sheet",
    "description": "Updated steel sheet description",
    "type": "raw",
    "unit_of_measure": "kg",
    "price": 120.00,
    "is_active": true
  }'
```

### Partial Update Material

```bash
curl -X PATCH http://localhost:8000/api/materials/{id}/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "price": 130.00
  }'
```

### Delete Material

```bash
curl -X DELETE http://localhost:8000/api/materials/{id}/ \
  -H "Authorization: Bearer your.access.token"
```

## Product API

All product endpoints require authentication.

### List Products

```bash
curl -X GET http://localhost:8000/api/products/ \
  -H "Authorization: Bearer your.access.token"
```

Query Parameters:
- `type`: Filter by product type
- `is_active`: Filter by active status
- `price`: Filter by price
- `search`: Search in name, code, slug, description, price
- `ordering`: Order by id, name, code, updated_at, price

### Get Single Product

```bash
curl -X GET http://localhost:8000/api/products/{id}/ \
  -H "Authorization: Bearer your.access.token"
```

### Create Product

```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Final Product",
    "code": "FP-001",
    "slug": "final-product",
    "description": "Complete product description",
    "type": "finished",
    "price": 500.00,
    "is_active": true
  }'
```

### Update Product

```bash
curl -X PUT http://localhost:8000/api/products/{id}/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Final Product",
    "code": "FP-001",
    "slug": "final-product",
    "description": "Updated product description",
    "type": "finished",
    "price": 550.00,
    "is_active": true
  }'
```

### Partial Update Product

```bash
curl -X PATCH http://localhost:8000/api/products/{id}/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "price": 600.00
  }'
```

### Delete Product

```bash
curl -X DELETE http://localhost:8000/api/products/{id}/ \
  -H "Authorization: Bearer your.access.token"
```

### Product Components API

The Product Components API manages relationships between finished products and their semi-finished components.

### List Product Components

```bash
curl -X GET http://localhost:8000/api/product-components/ \
  -H "Authorization: Bearer your.access.token"
```

Query Parameters:
- `finished_product`: Filter by finished product ID
- `semi_finished_product`: Filter by semi-finished product ID
- `search`: Search in finished_product name, semi_finished_product name
- `ordering`: Order by id, finished_product, semi_finished_product, updated_at

### Get Single Product Component

```bash
curl -X GET http://localhost:8000/api/product-components/{id}/ \
  -H "Authorization: Bearer your.access.token"
```

### Create Product Component

```bash
curl -X POST http://localhost:8000/api/product-components/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "finished_product": 1,
    "semi_finished_product": 2,
    "quantity": 2
  }'
```

### Update Product Component

```bash
curl -X PUT http://localhost:8000/api/product-components/{id}/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "finished_product": 1,
    "semi_finished_product": 2,
    "quantity": 3
  }'
```

### Partial Update Product Component

```bash
curl -X PATCH http://localhost:8000/api/product-components/{id}/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "quantity": 4
  }'
```

### Delete Product Component

```bash
curl -X DELETE http://localhost:8000/api/product-components/{id}/ \
  -H "Authorization: Bearer your.access.token"
```

## Warehouse API

All warehouse endpoints require authentication.

### List Warehouses

```bash
curl -X GET http://localhost:8000/api/warehouses/ \
  -H "Authorization: Bearer your.access.token"
```

Query Parameters:
- `is_active`: Filter by active status
- `search`: Search in name, description
- `ordering`: Order by id, name, updated_at

### Get Single Warehouse

```bash
curl -X GET http://localhost:8000/api/warehouses/{id}/ \
  -H "Authorization: Bearer your.access.token"
```

### Create Warehouse

```bash
curl -X POST http://localhost:8000/api/warehouses/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Main Warehouse",
    "description": "Main storage facility",
    "is_active": true
  }'
```

### Update Warehouse

```bash
curl -X PUT http://localhost:8000/api/warehouses/{id}/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Main Warehouse",
    "description": "Updated storage facility description",
    "is_active": true
  }'
```

### Partial Update Warehouse

```bash
curl -X PATCH http://localhost:8000/api/warehouses/{id}/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "New description"
  }'
```

### Delete Warehouse

```bash
curl -X DELETE http://localhost:8000/api/warehouses/{id}/ \
  -H "Authorization: Bearer your.access.token"
```

### Location API

The Location API manages storage locations within warehouses and work centers.

### List Locations

```bash
curl -X GET http://localhost:8000/api/locations/ \
  -H "Authorization: Bearer your.access.token"
```

Query Parameters:
- `location_type`: Filter by location type
- `warehouse`: Filter by warehouse ID
- `work_center`: Filter by work center ID
- `is_active`: Filter by active status
- `search`: Search in name
- `ordering`: Order by id, name, updated_at

### Get Single Location

```bash
curl -X GET http://localhost:8000/api/locations/{id}/ \
  -H "Authorization: Bearer your.access.token"
```

### Create Location

```bash
curl -X POST http://localhost:8000/api/locations/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Rack A1",
    "location_type": "storage",
    "warehouse": 1,
    "work_center": null,
    "is_active": true
  }'
```

### Update Location

```bash
curl -X PUT http://localhost:8000/api/locations/{id}/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Rack A1",
    "location_type": "storage",
    "warehouse": 1,
    "work_center": null,
    "is_active": true
  }'
```

### Partial Update Location

```bash
curl -X PATCH http://localhost:8000/api/locations/{id}/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Rack A2"
  }'
```

### Delete Location

```bash
curl -X DELETE http://localhost:8000/api/locations/{id}/ \
  -H "Authorization: Bearer your.access.token"
```

## Stock API

All stock endpoints require authentication.

### Stock Level API

The Stock Level API manages current inventory levels of materials in different locations.

### List Stock Levels

```bash
curl -X GET http://localhost:8000/api/stock-levels/ \
  -H "Authorization: Bearer your.access.token"
```

Query Parameters:
- `material`: Filter by material ID
- `location`: Filter by location ID
- `ordering`: Order by id, quantity

### Get Single Stock Level

```bash
curl -X GET http://localhost:8000/api/stock-levels/{id}/ \
  -H "Authorization: Bearer your.access.token"
```

### Create Stock Level

```bash
curl -X POST http://localhost:8000/api/stock-levels/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "material": 1,
    "location": 1,
    "quantity": 100
  }'
```

### Update Stock Level

```bash
curl -X PUT http://localhost:8000/api/stock-levels/{id}/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "material": 1,
    "location": 1,
    "quantity": 150
  }'
```

### Partial Update Stock Level

```bash
curl -X PATCH http://localhost:8000/api/stock-levels/{id}/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "quantity": 200
  }'
```

### Delete Stock Level

```bash
curl -X DELETE http://localhost:8000/api/stock-levels/{id}/ \
  -H "Authorization: Bearer your.access.token"
```

### Inventory Movement Log API

The Inventory Movement Log API tracks all movements of materials between locations.

### List Inventory Movements

```bash
curl -X GET http://localhost:8000/api/inventory-movement-logs/ \
  -H "Authorization: Bearer your.access.token"
```

Query Parameters:
- `material`: Filter by material ID
- `from_location`: Filter by source location ID
- `to_location`: Filter by destination location ID
- `ordering`: Order by id, created_at, quantity

### Get Single Inventory Movement

```bash
curl -X GET http://localhost:8000/api/inventory-movement-logs/{id}/ \
  -H "Authorization: Bearer your.access.token"
```

### Create Inventory Movement

```bash
curl -X POST http://localhost:8000/api/inventory-movement-logs/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "material": 1,
    "from_location": 1,
    "to_location": 2,
    "quantity": 50,
    "unit_of_measure": "kg"
  }'
```

### Update Inventory Movement

```bash
curl -X PUT http://localhost:8000/api/inventory-movement-logs/{id}/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "material": 1,
    "from_location": 1,
    "to_location": 2,
    "quantity": 75,
    "unit_of_measure": "kg"
  }'
```

### Partial Update Inventory Movement

```bash
curl -X PATCH http://localhost:8000/api/inventory-movement-logs/{id}/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "quantity": 100
  }'
```

### Delete Inventory Movement

```bash
curl -X DELETE http://localhost:8000/api/inventory-movement-logs/{id}/ \
  -H "Authorization: Bearer your.access.token"
```

## Production API

All production endpoints require authentication.

### Production Order API

The Production Order API manages production orders for manufacturing products.

### List Orders

```bash
curl -X GET http://localhost:8000/api/orders/ \
  -H "Authorization: Bearer your.access.token"
```

Query Parameters:
- `status`: Filter by order status
- `produced_product`: Filter by product being produced
- `unit_of_measure`: Filter by unit of measure
- `operators`: Filter by assigned operators
- `search`: Search in description, produced_product name
- `ordering`: Order by id, created_at, produced_quantity, start_date, completion_date

### Get Single Order

```bash
curl -X GET http://localhost:8000/api/orders/{id}/ \
  -H "Authorization: Bearer your.access.token"
```

### Create Order

```bash
curl -X POST http://localhost:8000/api/orders/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "produced_product": 1,
    "description": "Production order for Product A",
    "status": "planned",
    "produced_quantity": 100,
    "unit_of_measure": "pcs",
    "start_date": "2024-03-20",
    "operators": [1, 2]
  }'
```

### Update Order

```bash
curl -X PUT http://localhost:8000/api/orders/{id}/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "produced_product": 1,
    "description": "Updated production order",
    "status": "in_progress",
    "produced_quantity": 150,
    "unit_of_measure": "pcs",
    "start_date": "2024-03-20",
    "operators": [1, 2, 3]
  }'
```

### Partial Update Order

```bash
curl -X PATCH http://localhost:8000/api/orders/{id}/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed",
    "completion_date": "2024-03-21"
  }'
```

### Delete Order

```bash
curl -X DELETE http://localhost:8000/api/orders/{id}/ \
  -H "Authorization: Bearer your.access.token"
```

### Used Material API

The Used Material API tracks materials used in production orders.

### List Used Materials

```bash
curl -X GET http://localhost:8000/api/used-materials/ \
  -H "Authorization: Bearer your.access.token"
```

Query Parameters:
- `order`: Filter by order ID
- `material`: Filter by material ID
- `step_execution`: Filter by step execution ID
- `search`: Search in material name
- `ordering`: Order by id, quantity

### Get Single Used Material

```bash
curl -X GET http://localhost:8000/api/used-materials/{id}/ \
  -H "Authorization: Bearer your.access.token"
```

### Create Used Material

```bash
curl -X POST http://localhost:8000/api/used-materials/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "order": 1,
    "material": 1,
    "step_execution": 1,
    "quantity": 50,
    "unit_of_measure": "kg"
  }'
```

### Update Used Material

```bash
curl -X PUT http://localhost:8000/api/used-materials/{id}/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "order": 1,
    "material": 1,
    "step_execution": 1,
    "quantity": 75,
    "unit_of_measure": "kg"
  }'
```

### Partial Update Used Material

```bash
curl -X PATCH http://localhost:8000/api/used-materials/{id}/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "quantity": 100
  }'
```

### Delete Used Material

```bash
curl -X DELETE http://localhost:8000/api/used-materials/{id}/ \
  -H "Authorization: Bearer your.access.token"
```

### Production Step API

The Production Step API manages the steps involved in production processes.

### List Production Steps

```bash
curl -X GET http://localhost:8000/api/production-steps/ \
  -H "Authorization: Bearer your.access.token"
```

Query Parameters:
- `step_type`: Filter by step type
- `is_required`: Filter by required status
- `search`: Search in name, description
- `ordering`: Order by id, order_sequence, duration_hours

### Get Single Production Step

```bash
curl -X GET http://localhost:8000/api/production-steps/{id}/ \
  -H "Authorization: Bearer your.access.token"
```

### Create Production Step

```bash
curl -X POST http://localhost:8000/api/production-steps/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Assembly",
    "description": "Product assembly step",
    "step_type": "assembly",
    "order_sequence": 1,
    "duration_hours": 2,
    "is_required": true
  }'
```

### Update Production Step

```bash
curl -X PUT http://localhost:8000/api/production-steps/{id}/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Assembly",
    "description": "Updated assembly step",
    "step_type": "assembly",
    "order_sequence": 1,
    "duration_hours": 3,
    "is_required": true
  }'
```

### Partial Update Production Step

```bash
curl -X PATCH http://localhost:8000/api/production-steps/{id}/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "duration_hours": 4
  }'
```

### Delete Production Step

```bash
curl -X DELETE http://localhost:8000/api/production-steps/{id}/ \
  -H "Authorization: Bearer your.access.token"
```

### Production Step Execution API

The Production Step Execution API tracks the execution of production steps.

### List Step Executions

```bash
curl -X GET http://localhost:8000/api/step-executions/ \
  -H "Authorization: Bearer your.access.token"
```

Query Parameters:
- `order`: Filter by order ID
- `production_step`: Filter by production step ID
- `status`: Filter by execution status
- `assigned_operator`: Filter by operator ID
- `work_center`: Filter by work center ID
- `search`: Search in notes, quality_notes
- `ordering`: Order by id, start_time, end_time, actual_duration_hours

### Get Single Step Execution

```bash
curl -X GET http://localhost:8000/api/step-executions/{id}/ \
  -H "Authorization: Bearer your.access.token"
```

### Create Step Execution

```bash
curl -X POST http://localhost:8000/api/step-executions/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "order": 1,
    "production_step": 1,
    "status": "planned",
    "assigned_operator": 1,
    "work_center": 1,
    "start_time": "2024-03-20T10:00:00Z"
  }'
```

### Update Step Execution

```bash
curl -X PUT http://localhost:8000/api/step-executions/{id}/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "order": 1,
    "production_step": 1,
    "status": "in_progress",
    "assigned_operator": 1,
    "work_center": 1,
    "start_time": "2024-03-20T10:00:00Z",
    "notes": "Step execution in progress"
  }'
```

### Partial Update Step Execution

```bash
curl -X PATCH http://localhost:8000/api/step-executions/{id}/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed",
    "end_time": "2024-03-20T12:00:00Z"
  }'
```

### Delete Step Execution

```bash
curl -X DELETE http://localhost:8000/api/step-executions/{id}/ \
  -H "Authorization: Bearer your.access.token"
```

### Production Output API

The Production Output API manages the outputs produced during production steps.

### List Production Outputs

```bash
curl -X GET http://localhost:8000/api/production-outputs/ \
  -H "Authorization: Bearer your.access.token"
```

Query Parameters:
- `step_execution`: Filter by step execution ID
- `product`: Filter by product ID
- `quality_status`: Filter by quality status
- `search`: Search in product name, notes
- `ordering`: Order by id, quantity

### Get Single Production Output

```bash
curl -X GET http://localhost:8000/api/production-outputs/{id}/ \
  -H "Authorization: Bearer your.access.token"
```

### Create Production Output

```bash
curl -X POST http://localhost:8000/api/production-outputs/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "step_execution": 1,
    "product": 1,
    "quantity": 50,
    "unit_of_measure": "pcs",
    "quality_status": "good",
    "notes": "Production output notes"
  }'
```

### Update Production Output

```bash
curl -X PUT http://localhost:8000/api/production-outputs/{id}/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "step_execution": 1,
    "product": 1,
    "quantity": 75,
    "unit_of_measure": "pcs",
    "quality_status": "good",
    "notes": "Updated production output notes"
  }'
```

### Partial Update Production Output

```bash
curl -X PATCH http://localhost:8000/api/production-outputs/{id}/ \
  -H "Authorization: Bearer your.access.token" \
  -H "Content-Type: application/json" \
  -d '{
    "quantity": 100
  }'
```

### Delete Production Output

```bash
curl -X DELETE http://localhost:8000/api/production-outputs/{id}/ \
  -H "Authorization: Bearer your.access.token"
```
