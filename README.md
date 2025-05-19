# E-Commerce Admin API

A backend API using FastAPI and MySQL to manage products, inventory, sales tracking, and revenue reporting.

Built fully async using SQLAlchemy. It’s simple, clean, and ready to test.

---

## Features

- Add and search products
- Manage stock inventory
- Record sales (auto stock reduce)
- Get revenue by day/month/year
- Stats summary (top-selling product, total revenue)
- Seed script included for demo data

---

## Tech Stack

- FastAPI (web framework)
- SQLAlchemy (async ORM)
- MySQL (database)
- aiomysql (MySQL async driver)
- Uvicorn (ASGI server)
- Swagger UI (API testing)
- Pydantic (data validation)

---

##  Setup Instructions

### 1. Clone project

```bash
git clone <your-repo-url>
cd e-commerce
```

### 2. Setup virtual environment

```bash
python -m venv venv
.env\Scriptsctivate
pip install -r requirements.txt
```

### 3. Create MySQL database

```sql
CREATE DATABASE ecommercedb;
```

### 4. Update DB URL

Edit `app/db/database.py`:
```python
DATABASE_URL = "mysql+aiomysql://root:<your_password>@localhost/ecommercedb"
```

### 5. Run project

```bash
python init_db.py      # create tables
python seed.py         # add sample data
uvicorn main:app --reload
```

Go to Swagger UI:  
 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📡 API Endpoints

| Method | Endpoint                  | Description              |
|--------|---------------------------|--------------------------|
| POST   | `/products`               | Add new product          |
| GET    | `/products`               | List products            |
| GET    | `/products/search`        | Search products          |
| PUT    | `/inventory/{product_id}` | Update product stock     |
| GET    | `/inventory`              | View inventory           |
| POST   | `/sales`                  | Record a sale            |
| GET    | `/sales`                  | Filter sales             |
| GET    | `/revenue`                | Get revenue by period    |
| GET    | `/stats/overview`         | Business summary         |

---

##  Demo Data (via `seed.py`)

- Adds 5 sample products
- Sets stock: 5–20 units per product
- Creates 10 random sales (past 30 days)
- No manual input needed to test anything

---

##  Notes

- Fully async system using FastAPI + SQLAlchemy
- Swagger UI auto-generated
- Built for backend coding task
- Simple to test, extend, or integrate