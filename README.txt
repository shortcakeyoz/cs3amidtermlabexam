Library Inventory REST API

1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Install the packages:
   pip install -r requirements.txt
4. Start the API:
   uvicorn main:app --reload
5. Open http://127.0.0.1:8000/docs to test the endpoints.

Endpoints:
POST /categories/
GET /categories/
POST /books/
GET /books/
GET /books/{book_id}
PUT /books/{book_id}
DELETE /books/{book_id}

Use POST /categories/ first, then use its returned id as category_id when creating a book.
The SQLite database is created automatically as library.db.
