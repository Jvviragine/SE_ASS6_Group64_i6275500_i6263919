from fastapi import FastAPI, HTTPException, status
import requests
# Imports the Class of Book I created
from book import Book

# Instantiates the FastAPI
app = FastAPI()

# IMPORTANT: As Tom required, ALL the communication, even when between Microservices, passes throught the Gateway 
CATALOG_URL = 'http://localhost:3000/catalog/books' # It would also work if I pass the port 3001, but it would nopt go through the API

# GET -> Return ALL the Inventory
@app.get('/inventory/books')
def get_inventory():
    # Has to get the list of Books from Catalog
    books = requests.get(CATALOG_URL).json()
    return books

# GET -> A specific Book gigven its Book_ID
@app.get('/inventory/books/{book_id}')
def get_inventory(book_id: int):
    # Requests the List of Book from Catalog
    books = requests.get(CATALOG_URL).json()
    # Casts the Response that is in JSON to the Type 'Book'
    books = [Book(**book) for book in books]

    # Goes through the Books
    for book in books:
        # Makes sure the ID Matches
        if book.identifier == book_id:
            return book.quantity
    # In case there is a book in which the ID does not Match
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')

# PUT -> Updates a book in the Inventory
@app.put('/inventory/books/{book_id}')
def update_inventory(book_id: int, updated_book: Book):
    # Requests the Book from the Catalog
    books = requests.get(CATALOG_URL).json()

    # Checks if the ID of the Book does not match
    if book_id not in [book['identifier'] for book in books]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')
    
    # In case the ID Matches, then we can perform the IUpdate in the Quantity
    response = requests.put(CATALOG_URL + '/' + str(book_id), json={
        'quantity': updated_book.quantity
    })
    if response.status_code == 200:
        return {'message': 'Inventory updated'}
    
    raise HTTPException(status_code=response.status_code, detail=response.text)

# Equialent to the MAIN in Java - Runs the Server
if __name__ == '__main__':
    import uvicorn 
    uvicorn.run('book_inventory:app', port=3002, reload=False)
