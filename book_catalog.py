from fastapi import FastAPI, HTTPException, Response, status
from book import Book

# Instantiates the FastAPI 
app = FastAPI()

# The place where the fake Mockup Data will be Stored
books_catalog = []

# GET -> Return ALL books
@app.get('/catalog/books')
def get_books():
    return books_catalog

# GET -> Returns the Book with a Specific Book ID
@app.get('/catalog/books/{book_id}')
def get_book(book_id: int):
    for book in books_catalog:
        if book.identifier == book_id:
            return book
    # In case the Book_ID does not exist    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')

# POST -> Add a new book to the inventory
@app.post('/catalog/books')
def add_book(book: Book, response: Response):
    # Generates the ID
    identifier = len(books_catalog)

    book.identifier=identifier
    book.quantity=5 # Initiates with a quantity of 5 (could be anything)

    books_catalog.append(book)
    
    # The Response 
    response.status_code = status.HTTP_201_CREATED

    return book

# PUT -> Updates a certain Book
@app.put('/catalog/books/{book_id}')
def update_book(book_id: int, updated_book: Book):
    # I made in such a way that as long as the ID is Valid, the user can update anything he wishes
    for book in books_catalog:
        if book.identifier == book_id:
            book.title = updated_book.title if updated_book.title else book.title
            book.author = updated_book.author if updated_book.author else book.author
            book.year = updated_book.year if updated_book.year else book.year
            book.quantity = updated_book.quantity if updated_book.quantity else book.quantity

            return book
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')

@app.delete('/catalog/books/{book_id}')
def delete_book(book_id: int):
    for book in books_catalog:
        if book.identifier == book_id:
            books_catalog.remove(book)
            
            return {'message': 'Book deleted'}
    # In Case the Book ID does not exist    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')

# Equivalent to the MAIN of Java
if __name__ == '__main__':
    # Runs the Server
    import uvicorn # The Library for the Server I use with FastAPI
    uvicorn.run('book_catalog:app', port=3001, reload=False)