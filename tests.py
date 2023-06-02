import unittest
import requests

# I HAVE MADE THIS FILE in such a way that you just have to run it as 'python tests.py'

# The Class defined for the UNIT TESTS
class Tests(unittest.TestCase):

    # Order desired for the Unit Tests
    test_order = [
        'test_catalog_create',
        'test_catalog_read',
        'test_catalog_update',
        'test_catalog_delete',
        'test_inventory_get',
        'test_inventory_get_single',
        'test_inventory_update',
        'test_order_get',
        'test_order_create',
    ]

    # The Base path for the Gateway URL
    BASE_URL = 'http://localhost:3000/'

    # Complement for the BASE Gateway URL
    CATALOG_PATH = 'catalog/books'
    INVENTORY_PATH = 'inventory/books'
    ORDER_PATH = 'orders/books'

    # Basically Maps the Order we have defined into the Methods for testing
    @classmethod
    def get_sorted_test_cases(cls):
        loader = unittest.TestLoader()
        test_cases = loader.loadTestsFromTestCase(cls)
        sorted_test_cases = sorted(test_cases, key=lambda x: cls.test_order.index(x._testMethodName))
        
        return unittest.TestSuite(sorted_test_cases)

    # Generates the URL for each Test
    def get_url(self, base, path):
        return base + path

    # TEST FOR: CATALOG CREATE
    def test_catalog_create(self):
        print('Executing test_catalog_create')

        # Generates the URL for the request
        create_url = self.get_url(self.BASE_URL, self.CATALOG_PATH)
        # Generates a Sample Book
        response = requests.post(create_url, json={
            'title': 'The Hobbit',
            'author': 'J. R. R. Tolkien',
            'year': 1937
        })

        # TODO test the book entity returned for the correct values
        # Cheks if there was no problem with the Request
        self.assertEqual(response.status_code, 201)

        # I decided to Generate another Sample Book
        response = requests.post(create_url, json={
            'title': 'The Lord of the Rings',
            'author': 'J. R. R. Tolkien',
            'year': 1954
        })

        # TODO test the book entity returned for the correct values
        # Cheks if there was no problem with the Request
        self.assertEqual(response.status_code, 201)

    # TEST FOR: CATALOG READ
    def test_catalog_read(self):
        print('Executing test_catalog_read')

        # Generates the URL for the Request
        read_url = self.get_url(self.BASE_URL, self.CATALOG_PATH)
        # Makes the Request
        response = requests.get(read_url)

        # TODO test the book entities returned for the correct values (2 books above)

        # Checks if there was not an error in the Server
        self.assertEqual(response.status_code, 200)

    # TEST FOR: CATALOG UPDATE
    def test_catalog_update(self):
        print('Executing test_catalog_update')

        # Defines the URL
        update_url = self.get_url(self.BASE_URL, self.CATALOG_PATH + '/0')

        # Makes the Request for the Udapte
        response = requests.put(update_url, json={
            'title': 'The Hobbit',
            'author': 'J.R.R. Tolkien',
            'year': 1937
        })

        # TODO test the book entity returned for the correct values (new author)

        # Tests if there was no Error in the Server
        self.assertEqual(response.status_code, 200)

    # TEST FOR: DELETE CATALOG
    def test_catalog_delete(self):
        print('Executing test_catalog_delete')

        # Defines the URL
        delete_url = self.get_url(self.BASE_URL, self.CATALOG_PATH + '/0')
        # Makes the Request
        response = requests.delete(delete_url)

        # TODO get new catalog and test that the book was deleted
        # Checks if there was no Mistakes in the Server
        self.assertEqual(response.status_code, 200)

    

    # TEST FOR: INVENTORY GET ALL
    def test_inventory_get(self):
        print('Executing test_inventory_get')

        # Defines the URL
        get_url_ = self.get_url(self.BASE_URL, self.INVENTORY_PATH)
        # Makes the Request
        response = requests.get(get_url_)

        # TODO check books that left in inventory and their quantities

        # Checks if the Operation was successful, in the Server
        self.assertEqual(response.status_code, 200)

    # TEST FOR: INVENTORY GET SINGLE
    def test_inventory_get_single(self):
        print('Executing test_inventory_get_single')

        # Defines the URL
        get_single_url = self.get_url(self.BASE_URL, self.INVENTORY_PATH + '/1')
        # Makes the Request
        response = requests.get(get_single_url)

        # TODO check if that's the book we expect (Lord of the Rings)

        # Checks if the Operatiuon was succesful in the Server
        self.assertEqual(response.status_code, 200)

    # TEST FOR: UPDATE INVENTORY
    def test_inventory_update(self):
        print('Executing test_inventory_update')

        # Defines the URL
        update_url = self.get_url(self.BASE_URL, self.INVENTORY_PATH + '/1')
        # Makes the Request
        response = requests.put(update_url, json={
            'quantity': 20,
        })

        # TODO check if the quantity was updated by getting the inventory again

        # Checks if the Operatiuon was succesful in the Server
        self.assertEqual(response.status_code, 200)

    # TEST FOR: GET ORDERS
    def test_order_get(self):
        print('Executing test_order_get')

        # Defines the URL
        get_url_ = self.get_url(self.BASE_URL, self.ORDER_PATH)
        # Makes the Request
        response = requests.get(get_url_)

        # TODO check if the order is empty
        # Checks if the Operatiuon was succesful in the Server
        self.assertEqual(response.status_code, 200)

    # TEST FOR: CREATE ORDERS
    def test_order_create(self):
        print('Executing test_order_create')

        # Defines the URL
        update_url = self.get_url(self.BASE_URL, self.ORDER_PATH + '/1')
        # Makes the Request
        response = requests.post(update_url, json={
            'quantity': 1,
        })

        # TODO check if the order was created by getting the order again
        # Checks if the Operatiuon was succesful in the Server
        self.assertEqual(response.status_code, 200)

# Makes the Tests in such a way that we can just run it as another Python Code, instead of using specific commands in the Terminal
if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(Tests.get_sorted_test_cases())
    unittest.TextTestRunner().run(suite)