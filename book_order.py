from fastapi import FastAPI, HTTPException, Response, status
import requests
# The Book Data Type that I have defined
from book import Book

# Instantiates the API
app = FastAPI()

# Like for the Inventory, in order to communicate with the other Microservcies, it does through the Gateway
INVENTORY_URL = 'http://localhost:3000/inventory/books'

# Will Store the List of Orders
book_orders = []

# GET -> Get the List of Orders performed
@app.get('/orders/books')
def get_orders():
    return book_orders

# POST -> Place an Order
@app.post('/orders/books/{book_id}')
def place_order(book_id: int, ordered_book: Book, response: Response):
    # Defines the URL that will be used for the Request for the Inventory of Books
    get_single_url = INVENTORY_URL + '/' + str(book_id)
    print(get_single_url)

    # Requests the Inventory
    response = requests.get(get_single_url)
    # Extracts the Quantity
    quantity = ordered_book.quantity
    print(response.json())
    
    # Casts the Quantity that was in JSON to Int (So we can see if the Order is even possible)
    inventory_quantity = int(response.json())
    
    # Inncase the Order is Impossible
    if inventory_quantity < quantity:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': 'Book not available'}
    
    # In case the Order is Possible
    response_inventory = requests.put(INVENTORY_URL + '/' + str(book_id), json={
        # Sends the Request to the Update with the new Quantity Updated
        'quantity': (inventory_quantity - quantity)
    })

    # In case the Update was sucessful
    if response_inventory.status_code == 200:
        order = {
            'book_id': book_id,
            'quantity': quantity
        }
        # Adds to the List of Orders
        book_orders.append(order)
        return {'message': 'Order placed'}
    else:
        raise HTTPException(status_code=response_inventory.status_code, detail=response_inventory.text)

# Equivalent to the MAIN in Java -> Runs the Server using the 'uvicorn'
if __name__ == '__main__':
    import uvicorn
    uvicorn.run('book_order:app', port=3003, reload=False)
