# Advanced Web Application

## Purpose

A simple catalog application allowing users to create, view, and delete items organized by categories. Demonstrates both relational database interactions and dynamic front-end updates via AJAX, JSON-based seeding, and user authentication.

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Ensure initial_data.json is present in the project root (used for seeding).
3. To reset the database and re‐seed from JSON, delete the SQLite file: rm app.db
4. Set the Flask app environment: `export FLASK_APP=app.py`
5. Run the application: `flask run`

## Navigation

- Home (`/`)
  - Lists all items in `<ul id="items-list">`
  - Add-item form (`<form id="add-item-form">`) at bottom uses AJAX to submit to `/api/items/add` and updates list in-place.
- View Items (`/view`)
  - Displays items in a table with created_at timestamps
- Categories (`/categories`)
  - Lists categories in a table.
  - Form to add new categories and links to delete via full page reload.
- Register (`/register`)
  - Create a new user account
- Login (`/login`) / Logout (`/logout`)
  - Authenticate to access protected routes

## Important URLs

- `http://127.0.0.1:5000/` — Main items page
- `http://127.0.0.1:5000/view` — Table view of items
- `http://127.0.0.1:5000/categories` — Categories page
- `http://127.0.0.1:5000/register` — User registration
- `http://127.0.0.1:5000/login` — User login
- `POST http://127.0.0.1:5000/api/items/add` — JSON API endpoint for adding items

## Database Tables

- Category (`category` table)
  - `id` (Integer, PK)
  - `name` (String, not null, unique)
  - `description` (String)
  - Relationship: `Category.items → Item.category_id`
- Item (`item` table)
  - `id` (Integer, PK)
  - `name` (String, not null)
  - `description` (String)
  - `created_at` (DateTime, defaults to now)
  - `category_id` (Integer, FK to `category.id`)
- User (`user` table)
  - `id` (Integer, PK)
  - `username` (String, not null, unique)
  - `pw_hash` (String)

## Additional Requirements Completed

1. Additional Database Interactions

   - Created a second table `Category` alongside `Item`.
   - Implemented insert & delete routes for both models.
   - See:
     - `models.py` for `Category` class
     - `app.py` routes `/categories`, `/categories/add`, `/categories/delete`
     - Template `templates/categories.html`

2. AJAX Support

   - Built JSON API endpoint `POST /api/items/add` in `app.py`.
   - Front-end JS in `static/js/main.js` intercepts `<form id="add-item-form">`, sends JSON, and appends new `<li>` to `<ul id="items-list">` without reloading.
   - See:
     - `app.py` function `api_add_item`
     - `static/js/main.js`
     - `templates/index.html` form and list element IDs

3. JSON Parsing

   - On first request, the app reads initial_data.json and seeds the database.
   - See:
     - initial_data.json file in project root
     - init_db_and_load_data() in app.py

4. User Authentication
   - Registration (/register), login (/login), logout (/logout), and protected routes via @login_required.
   - See:
     - app.py routes register(), login(), logout()
     - templates/register.html and templates/login.html
     - @login_required on index and view_items routes
