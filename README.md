# Smart Canteen Sales & Inventory API

## Quick Start

```bash
# 1. Setup
python -m venv venv
source venv/bin/activate  # or: venv\\Scripts\\activate (Windows)
pip install -r requirements.txt

# 2. Database
docker run --name canteen_db \
  -e POSTGRES_DB=smart_canteen_db \
  -e POSTGRES_USER=canteen_user \
  -e POSTGRES_PASSWORD=canteen_password \
  -p 5432:5432 -d postgres:15-alpine

# 3. Run
uvicorn app.main:app --reload --port 8000

# 4. Visit
http://localhost:8000/docs
```

## API Endpoints

### Customers (5)
- `POST /customers` - Create
- `GET /customers` - List
- `GET /customers/{id}` - Get one
- `PUT /customers/{id}` - Update
- `DELETE /customers/{id}` - Delete

### Products (7)
- `POST /products` - Create
- `GET /products` - List
- `GET /products/{id}` - Get one
- `GET /products/low-stock/alerts` - Alerts
- `PUT /products/{id}` - Update
- `PATCH /products/{id}/stock` - Update stock
- `DELETE /products/{id}` - Delete

### Sales (6) + Reports (2)
- `POST /sales` - Record sale
- `GET /sales` - List sales
- `GET /sales/{id}` - Get one
- `GET /sales/invoice/{number}` - By invoice
- `GET /sales/customer/{id}` - By customer
- `PUT /sales/{id}` - Update status
- `GET /sales/reports/monthly/{year}/{month}` - Monthly report
- `GET /sales/reports/top-products` - Top products by sale 

## Project Structure

```
smart-canteen-api/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/ (Customer, Product, Sale)
│   ├── schemas/ (validation)
│   ├── crud/ (database ops)
│   └── api/endpoints/ (routes)
├── requirements.txt
├── .env
└── README.md
```
