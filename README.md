# Backend Take-Home: Orders API

Welcome! This is a small, scoped exercise meant to take **30-60 minutes**. We're not
looking for a polished production system — we're looking at how you think about
APIs, data validation, and working with a database.

## The scenario

You're building a tiny service that accepts orders, stores them, and lets you query
them back out.

## Step 1: Fork this repo

Click the **Fork** button in the top-right corner to create your own copy.

## Step 2: Set up your environment

You'll need **Python 3.10+**. SQLite is built into Python — nothing extra to install.

```bash
# Clone your fork
git clone <your-fork-url>
cd bp-recruitment-26-backend

# Add upstream remote
git remote add upstream https://github.com/tmublueprint/bp-recruitment-26-backend.git

# (Optional) create a virtual environment
python -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows
```

## Step 3: Implement the endpoints

Open `app.py` — it has a starter file with four endpoints to fill in.
Use Python's built-in [`http.server`](https://docs.python.org/3/library/http.server.html)
module (already imported). No frameworks needed.

Your server must listen on **port 3000**.

### What to build

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/orders` | Create a new order |
| `GET` | `/orders` | List all orders (optional `?status=` filter) |
| `GET` | `/orders/<id>` | Get a single order by ID |
| `PATCH` | `/orders/<id>` | Update an order's status |

<details>
<summary><strong>POST /orders — details</strong></summary>

Request body:
```json
{
  "customer_email": "person@example.com",
  "amount": 42.50,
  "status": "pending"
}
```

- `customer_email` (string, required)
- `amount` (positive number, required)
- `status` (string, optional — defaults to `"pending"`)

**201** response:
```json
{
  "id": 1,
  "customer_email": "person@example.com",
  "amount": 42.50,
  "status": "pending",
  "created_at": "2026-07-13T12:00:00"
}
```

**400** response for invalid payloads: `{ "error": "..." }`

</details>

<details>
<summary><strong>GET /orders — details</strong></summary>

- Returns a JSON array of all orders
- Supports optional `?status=pending` query param to filter
- Always returns **200** (empty array `[]` if nothing matches)

</details>

<details>
<summary><strong>GET /orders/&lt;id&gt; — details</strong></summary>

- **200** with the order if found
- **404** with `{ "error": "not found" }` if not

</details>

<details>
<summary><strong>PATCH /orders/&lt;id&gt; — details</strong></summary>

Request body:
```json
{
  "status": "shipped"
}
```

- `status` is the only field that can be updated
- **200** with the updated order
- **400** with `{ "error": "..." }` if `status` is missing or invalid
- **404** with `{ "error": "not found" }` if the order doesn't exist

</details>

## Step 4: Set up your database

Use **SQLite** via `sqlite3` from the standard library.
The `get_db()` function in `app.py` already creates the table for you — just call it.

Your `orders` table should have at minimum:

| Column | Type | Notes |
|--------|------|-------|
| `id` | integer | primary key, auto-increment |
| `customer_email` | text | not null |
| `amount` | real | not null |
| `status` | text | not null, default `"pending"` |
| `created_at` | text | not null |

## Step 5: Test locally

Start your server and test with curl:

```bash
# Start your server (in a separate terminal)
python app.py

# Create an order
curl -X POST http://localhost:3000/orders \
  -H "Content-Type: application/json" \
  -d '{"customer_email": "test@example.com", "amount": 25}'

# Get all orders
curl http://localhost:3000/orders

# Get a single order
curl http://localhost:3000/orders/1

# Update an order's status
curl -X PATCH http://localhost:3000/orders/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "shipped"}'
```

## Step 6: Submit

1. Commit and push your changes to your fork
2. Open a pull request back to this repo
3. Look at the **Checks** tab on your PR — a **"🧪 Test Score"** check will show your score
4. The score is also summarized in the **Action Summary** at the bottom of the workflow run

The full test suite runs automatically — don't report your score manually.

---

**Note:** The test score is computed from the output of the private test suite. A passing score means all tests passed. If any test fails, you'll see which ones in the check details.

---

## What we're looking for

- Does it work? (test suite passing is the baseline)
- Is the validation sensible and not just hacked to pass specific tests?
- Is the code readable — would a teammate understand it?
