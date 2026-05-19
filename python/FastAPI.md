# FastAPI — Quick Reference

Modern Python web framework for building APIs. Fast, type-driven, async-first.

```
FastAPI   →  Python web framework for APIs
           →  built on Starlette (web) + Pydantic (validation)
           →  type hints DRIVE the framework
           →  automatic OpenAPI / Swagger docs
           →  async-friendly
```

---

## Why FastAPI

```
✓ Fast — comparable to Node.js / Go (Starlette + Pydantic)
✓ Less code — type hints replace boilerplate
✓ Auto docs — Swagger UI + ReDoc at /docs and /redoc
✓ Validation — input/output validated automatically
✓ Async support — async def routes work natively
✓ IDE-friendly — full type completion
✓ Modern Python (3.7+) — uses type hints, async/await
```

Compared to alternatives:

| | FastAPI | Flask | Django REST |
|-|---------|-------|-------------|
| Speed | Fast | Slower | Slower |
| Async | Native | Bolted on | Limited |
| Type hints | Required | Optional | Optional |
| Auto docs | Yes | Manual | Manual |
| Use case | Modern APIs | Anything | Full-stack web apps |

---

## Installation

```bash
pip install fastapi uvicorn
```

- `fastapi` — the framework
- `uvicorn` — ASGI server to run it

---

## Hello World

```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello, FastAPI!"}
```

Run:

```bash
uvicorn main:app --reload
```

- `main` = filename (`main.py`)
- `app` = the FastAPI instance
- `--reload` = restart on file change (dev only)

Visit:
- `http://localhost:8000` — the endpoint
- `http://localhost:8000/docs` — interactive Swagger UI
- `http://localhost:8000/redoc` — alternative docs

---

## Path Parameters

```python
@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}
```

```
GET /items/5     → {"item_id": 5}
GET /items/abc   → 422 Unprocessable Entity (not an int)
```

The type hint **drives validation**. `int` makes FastAPI validate and convert automatically.

---

## Query Parameters

```python
@app.get("/items/")
def list_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

```
GET /items/?skip=20&limit=50     → {"skip": 20, "limit": 50}
GET /items/                       → {"skip": 0, "limit": 10}  (defaults)
```

Function parameters not in the path become **query parameters**.

### Optional query params

```python
from typing import Optional

@app.get("/search")
def search(q: Optional[str] = None, category: str = "all"):
    return {"q": q, "category": category}
```

---

## Request Body — Pydantic Models

For POST/PUT data, define a Pydantic model:

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    is_available: bool = True
    description: Optional[str] = None

@app.post("/items/")
def create_item(item: Item):
    return {"created": item}
```

Send JSON:

```bash
curl -X POST http://localhost:8000/items/ \
     -H "Content-Type: application/json" \
     -d '{"name": "Widget", "price": 9.99}'
```

```
✓ Auto-validates JSON against the model
✓ Returns 422 with details if invalid
✓ Auto-generates docs based on the model
✓ IDE autocomplete inside the function
```

---

## All HTTP Methods

```python
@app.get("/items/")
@app.post("/items/")
@app.put("/items/{id}")
@app.patch("/items/{id}")
@app.delete("/items/{id}")
@app.head("/items/")
@app.options("/items/")
```

Standard REST mapping:

```
GET    → read
POST   → create
PUT    → replace
PATCH  → update partial
DELETE → remove
```

---

## Status Codes

```python
@app.post("/items/", status_code=201)
def create_item(item: Item):
    return item
```

Or using the `status` module:

```python
from fastapi import status

@app.post("/items/", status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    return item
```

---

## Error Handling

```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id > 1000:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id}
```

`HTTPException` returns the proper JSON error response automatically.

### Custom exception handlers

```python
from fastapi import Request
from fastapi.responses import JSONResponse

class CustomError(Exception):
    def __init__(self, message: str):
        self.message = message

@app.exception_handler(CustomError)
async def custom_handler(request: Request, exc: CustomError):
    return JSONResponse(
        status_code=400,
        content={"error": exc.message}
    )
```

---

## Response Model

Specify the shape of responses (validates AND filters output):

```python
class ItemResponse(BaseModel):
    name: str
    price: float

class ItemDB(BaseModel):
    name: str
    price: float
    secret_internal_field: str

@app.get("/items/{id}", response_model=ItemResponse)
def get_item(id: int) -> ItemDB:
    return ItemDB(name="Widget", price=9.99, secret_internal_field="hidden")
    # Response will NOT include secret_internal_field
```

Useful for hiding internal fields like passwords or DB IDs.

---

## Validation with Pydantic

Pydantic does heavy lifting:

```python
from pydantic import BaseModel, Field, EmailStr, validator

class User(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr
    age: int = Field(gt=0, lt=150)
    password: str = Field(min_length=8)
    
    @validator('username')
    def no_spaces(cls, v):
        if ' ' in v:
            raise ValueError('Username cannot contain spaces')
        return v
```

Invalid inputs are rejected with detailed errors before reaching your function.

---

## Async Support

FastAPI is async-native. Use `async def` for I/O-bound endpoints:

```python
import httpx

@app.get("/external-data")
async def fetch():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
        return response.json()
```

```
async def  →  for I/O-bound work (DB, HTTP, file I/O)
def        →  for CPU-bound work or sync libraries

FastAPI handles BOTH styles correctly — async runs in event loop,
sync runs in thread pool to avoid blocking.
```

---

## Dependency Injection

Reusable logic injected into endpoints:

```python
from fastapi import Depends

def get_token(token: str = ""):
    if not token:
        raise HTTPException(401, "Token required")
    return token

@app.get("/protected/")
def protected(token: str = Depends(get_token)):
    return {"valid": True, "token": token}
```

```
Depends(some_function)  →  FastAPI calls some_function and passes the result
                          →  used for auth, DB sessions, config, etc.
```

### Class-based dependencies

```python
class Pagination:
    def __init__(self, skip: int = 0, limit: int = 10):
        self.skip = skip
        self.limit = limit

@app.get("/items/")
def list_items(p: Pagination = Depends()):
    return {"skip": p.skip, "limit": p.limit}
```

Cleaner for grouped params.

### Database session pattern

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/{user_id}")
def get_user(user_id: int, db = Depends(get_db)):
    return db.query(User).filter(User.id == user_id).first()
```

`yield` lets the dependency clean up after the request.

---

## Middleware

Run code before/after every request:

```python
from fastapi import Request
import time

@app.middleware("http")
async def log_time(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    response.headers["X-Process-Time"] = str(time.time() - start)
    return response
```

---

## CORS

For browser clients on different origins:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Authentication — OAuth2 with JWT

Standard pattern using JWT tokens:

```python
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
def login(username: str, password: str):
    if username != "admin":
        raise HTTPException(401, "Bad credentials")
    token = jwt.encode({"sub": username}, "secret", algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}

@app.get("/me")
def me(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, "secret", algorithms=["HS256"])
    return {"user": payload["sub"]}
```

Install dependencies:

```bash
pip install python-jose[cryptography] passlib[bcrypt]
```

---

## File Uploads

```python
from fastapi import File, UploadFile

@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    contents = await file.read()
    return {"filename": file.filename, "size": len(contents)}
```

For form data:

```python
from fastapi import Form

@app.post("/form/")
def receive(username: str = Form(...), password: str = Form(...)):
    return {"username": username}
```

---

## Background Tasks

Run something after sending response:

```python
from fastapi import BackgroundTasks

def write_log(message: str):
    with open("log.txt", "a") as f:
        f.write(message + "\n")

@app.post("/items/")
def create(item: Item, background: BackgroundTasks):
    background.add_task(write_log, f"Created {item.name}")
    return {"status": "created"}
```

Useful for emails, logs, cleanups — without blocking the client.

---

## WebSockets

```python
from fastapi import WebSocket

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Echo: {data}")
```

---

## Testing

Use `TestClient` for synchronous tests:

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, FastAPI!"}

def test_create_item():
    response = client.post("/items/", json={"name": "Widget", "price": 9.99})
    assert response.status_code == 200
    assert response.json()["created"]["name"] == "Widget"
```

For async tests, use `httpx.AsyncClient`.

---

## Project Structure

For larger apps:

```
myapp/
├── main.py              # FastAPI app instance + setup
├── api/
│   ├── __init__.py
│   ├── users.py         # /users routes
│   └── items.py         # /items routes
├── models/
│   ├── __init__.py
│   └── user.py          # Pydantic models
├── db/
│   ├── __init__.py
│   └── session.py       # DB connection setup
├── core/
│   ├── config.py        # Settings
│   └── security.py      # Auth helpers
└── tests/
```

### Routers — split routes across files

```python
# api/users.py
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def list_users():
    return [{"name": "Alice"}]

# main.py
from fastapi import FastAPI
from api import users

app = FastAPI()
app.include_router(users.router)
```

```
prefix → adds /users to all endpoints in this router
tags    → groups endpoints in the docs UI
```

---

## Configuration

Use Pydantic settings:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "MyApp"
    database_url: str
    secret_key: str
    
    class Config:
        env_file = ".env"

settings = Settings()
```

Loads from environment variables or `.env` file. Type-safe config.

---

## Deployment

### Production server

```bash
# Don't use --reload in production
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

`--workers` runs multiple processes for parallelism.

### With Gunicorn (Linux)

```bash
gunicorn -k uvicorn.workers.UvicornWorker -w 4 main:app
```

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Behind Nginx / load balancer

```
Client → Nginx → FastAPI workers → DB
```

Nginx handles TLS, static files, rate limiting. FastAPI handles API logic.

---

## Common Patterns

### CRUD endpoints

```python
from typing import List

@app.get("/items/", response_model=List[Item])
def list_items():
    return db.fetch_all()

@app.get("/items/{id}", response_model=Item)
def get_item(id: int):
    item = db.fetch_one(id)
    if not item:
        raise HTTPException(404)
    return item

@app.post("/items/", response_model=Item, status_code=201)
def create_item(item: Item):
    return db.insert(item)

@app.put("/items/{id}", response_model=Item)
def update_item(id: int, item: Item):
    return db.update(id, item)

@app.delete("/items/{id}", status_code=204)
def delete_item(id: int):
    db.delete(id)
```

### Pagination

```python
@app.get("/items/")
def list_items(skip: int = 0, limit: int = 100):
    return {
        "total": db.count(),
        "items": db.fetch(skip, limit)
    }
```

### Sorting & filtering

```python
from typing import Optional
from enum import Enum

class SortBy(str, Enum):
    name = "name"
    price = "price"
    date = "date"

@app.get("/items/")
def list_items(
    sort: SortBy = SortBy.name,
    min_price: Optional[float] = None
):
    return db.query(sort=sort, min_price=min_price)
```

`Enum` values get nice dropdown in Swagger UI.

---

## Quick Reference Cheat Sheet

| Task | Code |
|------|------|
| Create app | `app = FastAPI()` |
| GET route | `@app.get("/path")` |
| POST route | `@app.post("/path")` |
| Path param | `def f(id: int)` with `/path/{id}` |
| Query param | `def f(q: str = None)` |
| Body | `def f(item: ItemModel)` |
| Response model | `@app.get("/", response_model=ItemModel)` |
| Status code | `@app.post("/", status_code=201)` |
| Raise error | `raise HTTPException(404, "Not found")` |
| Dependency | `def f(x = Depends(dep_func))` |
| Async | `async def f(): await ...` |
| Test | `TestClient(app).get("/")` |
| Run dev | `uvicorn main:app --reload` |
| Run prod | `uvicorn main:app --workers 4` |

---

## Auto-Generated Docs

After running, visit:

```
http://localhost:8000/docs     →  Swagger UI (interactive)
http://localhost:8000/redoc    →  ReDoc (cleaner reading)
http://localhost:8000/openapi.json → raw OpenAPI schema
```

No setup required. Driven by your type hints and Pydantic models.

---

## Common Pitfalls

```
✗ Forgetting to start uvicorn with --reload in development
   → manual restart on every change

✗ Using sync code in async endpoint
   → blocks the event loop
   → use sync def OR convert to async

✗ Not specifying response_model
   → may leak internal fields in JSON response
   → use response_model to filter output

✗ Catching exceptions and returning dicts
   → returns 200 with error in body
   → raise HTTPException instead

✗ Defining routes in wrong order
   → /items/all matches /items/{id} → id="all" → unexpected behaviour
   → put static routes BEFORE dynamic ones

✗ Forgetting CORS for browser clients
   → 401/403/CORS errors in browser console
```

---

## Summary

```
FastAPI = type-driven Python web framework for APIs

Core ideas:
   ✓ Type hints DRIVE validation, docs, and IDE support
   ✓ Pydantic models define request/response shapes
   ✓ Auto-generated Swagger UI at /docs
   ✓ Async-first, sync also supported
   ✓ Dependencies for clean reusable logic
   ✓ Fast (Starlette + Pydantic)

Stack:
   FastAPI       →  framework
   Pydantic      →  validation
   Starlette     →  ASGI / web layer
   Uvicorn       →  ASGI server
   SQLAlchemy / Tortoise  →  DB (optional)

Use it for:
   ✓ Modern REST APIs
   ✓ Microservices
   ✓ ML model serving
   ✓ Real-time APIs (WebSockets)
   ✓ Anything that needs fast async APIs
```

> FastAPI = **Flask's ease + Django's structure + modern Python's typing + async + speed**. The default choice for new Python APIs in 2024+.
