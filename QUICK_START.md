# Quick Start - Smart Canteen API

## Step 1: Environment Setup

```bash
cd smart-canteen-api

python -m venv venv

# macOS/Linux:
source venv/bin/activate

# Windows:
venv\\Scripts\\activate

pip install -r requirements.txt
```

## Step 2: Database Setup

```bash
docker run --name canteen_db \
  -e POSTGRES_DB=smart_canteen_db \
  -e POSTGRES_USER=canteen_user \
  -e POSTGRES_PASSWORD=canteen_password \
  -p 5432:5432 \
  -d postgres:15-alpine
```

## Step 3: Run Application

```bash
uvicorn app.main:app --reload --port 8000
```

✅ **Visit:** http://localhost:8000/docs

## Test the API

### 1. Create Customer
```bash
curl -X POST http://localhost:8000/customers \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "TechCorp",
    "contact_person": "John",
    "email": "john@tech.com"
  }'
```

### 2. Create Product
```bash
curl -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Chai",
    "sku": "TEA-001",
    "price": 40.00,
    "stock_quantity": 100
  }'
```

### 3. Record Sale
```bash
curl -X POST http://localhost:8000/sales \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "<ID_FROM_STEP_1>",
    "items": [
      {
        "product_id": "<ID_FROM_STEP_2>",
        "quantity": 5,
        "unit_price": 40.00
      }
    ],
    "tax_amount": 20,
    "discount_amount": 0
  }'
```

### 4. Check Reports
```bash
curl http://localhost:8000/sales/reports/monthly/2025/12

curl http://localhost:8000/products/low-stock/alerts
```